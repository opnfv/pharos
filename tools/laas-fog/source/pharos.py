#!/usr/bin/python
"""
#############################################################################
#Copyright 2017 Parker Berberian and others                                 #
#                                                                           #
#Licensed under the Apache License, Version 2.0 (the "License");            #
#you may not use this file except in compliance with the License.           #
#You may obtain a copy of the License at                                    #
#                                                                           #
#    http://www.apache.org/licenses/LICENSE-2.0                             #
#                                                                           #
#Unless required by applicable law or agreed to in writing, software        #
#distributed under the License is distributed on an "AS IS" BASIS,          #
#WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.   #
#See the License for the specific language governing permissions and        #
#limitations under the License.                                             #
#############################################################################
"""

import requests
import time
import calendar
import subprocess
import sys
import yaml
import os
import logging
from utilities import Utilities
from database import BookingDataBase


class Pharos_api:
    """
    This class listens to the dashboard and starts/stops bookings accordingly.
    This class should run in the background indefinitely.
    Do not execute this file directly - run ./listen.py instead
    """
    def __init__(self, config):
        """
        init function.
        config is the already-parsed config file
        """
        self.conf = config
        self.servers = yaml.safe_load(open(config['inventory']))
        self.log = self.createLogger("pharos_api")
        self.polling = 60 / int(config['polling'])
        self.log.info(
                "polling the dashboard once every %d seconds", self.polling)
        self.dashboard = config['dashboard']
        self.log.info("connecting to dashboard at %s", self.dashboard)
        if os.path.isfile(config['token']):
            self.token = open(config['token']).read()
        else:
            self.token = config['token']
        self.updateHeader()
        self.database = BookingDataBase(config['database'])
        self.log.info("using database at %s", self.conf['database'])
        self.deploy_path = os.path.join(
                os.path.dirname(os.path.realpath(__file__)), "deploy.py")
        if not os.path.isfile(self.deploy_path):
            self.log.error(
                "Cannot find the deployment script at %s", self.deploy_path)

    def setToken(self, token):
        """
        Sets authentication token. Not yet needed.
        """
        self.token = token
        self.updateHeader()

    def setTokenFromFile(self, path):
        """
        reads auth token from a file. Not yet needed.
        """
        self.setToken(open(path).read())

    def updateHeader(self):
        """
        updates the http header used when talking to the dashboard
        """
        self.header = {"Authorization": "Token " + self.token}

    def listen(self):
        """
        this method will continuously poll the pharos dashboard.
        If a booking is found on our server,
        we will start a deployment in the background with the
        proper config file for the requested
        installer and scenario.
        """
        self.log.info("%s", "Beginning polling of dashboard")
        try:
            while True:
                time.sleep(self.polling)
                url = self.dashboard+"/api/bookings/"
                bookings = requests.get(url, headers=self.header).json()
                for booking in bookings:
                    if booking['resource_id'] in self.servers.keys():
                        self.convertTimes(booking)
                        self.database.checkAddBooking(booking)
                self.checkBookings()
        except Exception:
            self.log.exception('%s', "failed to connect to dashboard")

            self.listen()

    def convertTimes(self, booking):
        """
        this method will take the time reported by Pharos in the
        format yyyy-mm-ddThh:mm:ssZ
        and convert it into seconds since the epoch,
        for easier management
        """
        booking['start'] = self.pharosToEpoch(booking['start'])
        booking['end'] = self.pharosToEpoch(booking['end'])

    def pharosToEpoch(self, timeStr):
        """
        Converts the dates from the dashboard to epoch time.
        """
        time_struct = time.strptime(timeStr, '%Y-%m-%dT%H:%M:%SZ')
        epoch_time = calendar.timegm(time_struct)
        return epoch_time

    def checkBookings(self):
        """
        This method checks all the bookings in our database to see if any
        action is required.
        """
        # get all active bookings from database into a usable form
        bookings = self.database.getBookings()
        for booking in bookings:
            # first, check if booking is over
            if time.time() > booking[3]:
                self.log.info("ending the booking with id %i", booking[0])
                self.endBooking(booking)
            # Then check if booking has begun and the host is still idle
            elif time.time() > booking[2] and booking[7] < 1:
                self.log.info("starting the booking with id %i", booking[0])
                self.startBooking(booking)

    def startBooking(self, booking):
        """
        Starts the scheduled booking on the requested host with
        the correct config file.
        The provisioning process gets spun up in a subproccess,
        so the api listener is not interupted.
        """
        try:
            host = self.servers[booking[1]]
            self.log.info("Detected a new booking started for host %s", host)
            config_file = self.conf['default_configs']["None"]
            try:
                config_file = self.conf['default_configs'][booking[4]]
            except KeyError:
                self.log.warning(
                        "No installer detected in the booking request.")
            self.log.info("New booking started for host %s", host)
            self.database.setStatus(booking[0], 1)  # mark booking started
            if not os.path.isfile(self.deploy_path):
                error = "Cannot find the deploment script at %s"
                self.log.error(error, self.deploy_path)
            subprocess.Popen([
                '/usr/bin/python',
                self.deploy_path,
                '--config', config_file,
                '--host', host
                ])
        except Exception:
            self.log.exception("Failed to start booking for %s", host)

    def endBooking(self, booking):
        """
        Resets a host once its booking has ended.
        """
        try:
            try:
                config_file = self.conf['default_configs'][booking[4]]
            except KeyError:
                warn = "No installer detected in booking request"
                self.log.warning("%s", warn)
                config_file = self.conf['default_configs']["None"]

            host = self.servers[booking[1]]
            log = logging.getLogger(host)
            log.info('Lease expired. Resetting host %s', host)
            self.database.setStatus(booking[0], 3)
            if not os.path.isfile(self.deploy_path):
                err = "Cannot find deployment script at %s"
                self.log.error(err, self.deploy_path)
            subprocess.Popen([
                '/usr/bin/python',
                self.deploy_path,
                '--config', config_file,
                '--host', host,
                '--reset'
                ])
            self.database.removeBooking(booking[0])
        except Exception:
            self.log.exception("Failed to end booking for %s", host)

    def createLogger(self, name):
        return Utilities.createLogger(name, self.conf['logging_dir'])


if __name__ == "__main__":
    if "--config" not in sys.argv:
        print "Specify config file with --config option"
        sys.exit(1)
    config = None
    try:
        config_file = sys.argv[1+sys.argv.index('--config')]
        config = yaml.safe_load(open(config_file))
    except Exception:
        sys.exit(1)
    api = Pharos_api(config)
    api.listen()
