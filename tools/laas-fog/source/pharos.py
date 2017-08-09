#!/usr/bin/python

import requests
import time
import calendar
import subprocess
import sys
import json
import os
import logging
import threading
from utilities import Utilities
from pod_manager import Pod_Manager
from database import BookingDataBase
"""
This class will interface with the pharos dashboard. It should work all in the background. 
"""
class Pharos_api:
    
    def __init__(self,config):
        self.conf = config
        self.servers = json.loads(open(config['fog_conf']).read())['hosts']
        self.log = self.createLogger("pharos_api")
        self.polling = 60 / int(config['polling'])
        self.log.info("polling the dashboard once every %d seconds",self.polling)
        self.dashboard = config['dashboard']
        self.log.info("connecting to dashboard at %s",self.dashboard)
        self.token = config['token']
        self.updateHeader()
        self.database = BookingDataBase(config['database'])
        self.log.info("using database at %s",self.conf['database'])
        self.deploy_path = os.path.join(os.path.dirname(os.path.realpath(__file__)),"deploy.py")
        if not os.path.isfile(self.deploy_path):
            self.log.error("Cannot find the deployment script at %s",self.deploy_path)
        

    def setToken(self,token):
        self.token = token
        self.updateHeader()

    def setTokenFromFile(self,path):
        self.setToken(open(path).read())

    def updateHeader(self):
        self.header = {"Authorization":"Token " + self.token}
    
    
    """
    this method will continuously poll the pharos dashboard. If a booking is found on our server,
    we will start a deployment in the background with the proper config file for the requested
    installer and scenario.
    """
    def listen(self):
        self.log.info("%s","Beginning polling of dashboard")
        try:
            while True:
                time.sleep(self.polling)
                self.log.info('%s',"polling the dashboard")
                bookings = requests.get(self.dashboard+"/api/bookings/",headers=self.header).json()
                for booking in bookings:
                    if booking['resource_id'] in self.servers.keys():
                        self.convertTimes(booking)
                        self.database.checkAddBooking(booking)
                self.checkBookings()
        except Exception as e:
            self.log.exception('%s',"failed to connect to dashboard")
            
            self.listen()


                
    #this method will take the time reported by Pharos in the format yyyy-mm-ddThh:mm:ssZ
    #and convert it into seconds since the epoch, for easier management
    def convertTimes(self,booking):
        #%Y-%m-%dT%H:%M:%SZ
        booking['start'] = self.pharosToEpoch(booking['start'])
        booking['end'] = self.pharosToEpoch(booking['end'])

    def pharosToEpoch(self,timeStr):
        time_struct = time.strptime(timeStr,'%Y-%m-%dT%H:%M:%SZ')
        epoch_time = calendar.timegm(time_struct)
        return epoch_time

    def checkBookings(self):
        #first, get all active bookings from database into a usable form
        bookings = self.database.getBookings()
        for booking in bookings:
            #first, check if booking is over
            if time.time() > booking[3]:
                self.log.info("ending the booking with id %i",booking[0])
                self.endBooking(booking)
            elif time.time() > booking[2] and booking[7] < 1:
                self.log.info("starting the booking with id %i",booking[0])
                self.startBooking(booking)
            #check if ending time has past and the host is not idle


    def startBooking(self,booking):
        try:
            host = self.servers[booking[1]]
            self.log.info("Detected a new booking started for host %s",host)
            config_file = self.conf['default_configs']["None"]
            try:
                config_file = self.conf['default_configs'][booking[4]]
            except KeyError:
                self.log.warning("No installer detected in the booking request.")
            self.log.info("New booking started for host %s",host)
            self.database.setStatus(booking[0],1) #marks the booking as started
            if not os.path.isfile(self.deploy_path):
                self.log.error("Cannot find the deployment script at %s",self.deploy_path)
            subprocess.Popen(['/usr/bin/python',self.deploy_path,'--config',config_file,'--host',host])
        except Exception:
            self.log.exception("Failed to start booking for %s",host)

    def endBooking(self,booking):
        try:
            config_file = self.conf['default_configs']["None"]
            try:
                config_file = self.conf['default_configs'][booking[4]]
            except KeyError:
                self.log.warning("No installer detected in the booking request.")
            host = self.servers[booking[1]]
            log = logging.getLogger(host)
            log.info('%s','Lease expired. Resetting host')
            self.database.setStatus(booking[0],3)
            
            config = json.loads(open(config_file).read())
            manager_args = (config,host,True)
            if not os.path.isfile(self.deploy_path):
                self.log.error("Cannot find the deployment script at %s",self.deploy_path)
            subprocess.Popen(['/usr/bin/python',self.deploy_path,'--config',config_file,'--host',host,'--reset'])
            self.database.removeBooking(booking[0])
        except Exception:
            self.log.exception("Failed to end booking for %s",host)


    def createLogger(self,name):
        return Utilities.createLogger(name,self.conf['logging_dir'])
        

if __name__ == "__main__":
    if not "--config" in sys.argv:
        print "Specify config file with --config option"
        sys.exit(1)
    config = None
    try:
        config_file = sys.argv[1+sys.argv.index('--config')]
        config = json.loads(open(config_file).read())
    except Exception:
        sys.exit(1)
    api = Pharos_api(config)
    api.listen()
