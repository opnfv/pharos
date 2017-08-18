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
import sqlite3
import sys
import time


class HostDataBase:
    """
    This class talks with a simple sqlite database and can select a free host
    when one is needed.
    The layout of the database is:
        TABLE host:
            name <hostname> status <status_code> book_start
                <Unix timestamp> book_end <Unix timestamp>
        status_codes:
        0 - idle
        1 - deploying
        2 - deployed, in use
        3 - expired, ready to be reset
    """

    def __init__(self, path):
        """
        init function. Will create the file at the end of path
        if it doesnt already exist
        """
        self.database = sqlite3.connect(path)
        self.cursor = self.database.cursor()

    def resetHosts(self, hosts):
        """
        Recreates the host table in the database.
        WILL ERASE ALL DATA. USE WITH CAUTION.
        """
        try:
            self.cursor.execute("DROP TABLE hosts")
            self.createTable()
        except:
            pass

        for host in hosts:
            self.addHost(host)

    def createTable(self):
        """
        This method creates the table hosts with
        a name and status field
        """
        self.cursor.execute("CREATE TABLE hosts (name text, status integer)")
        self.database.commit()

    def addHost(self, name):
        """
        Adds a host with name to the available hosts.
        When first added, the host is assumed to be idle.
        """
        host = (name, )
        self.cursor.execute("INSERT INTO hosts VALUES (?, 0) ", host)
        self.database.commit()

    def getHost(self, requested=None):
        """
        Returns the name of an available host.
        If a host is specifically requested,
        that host is returned.
        If the requested host is not available,
        this method will throw an error.
        If no host is specificaly requested,
        the next available host is returned.
        """
        self.cursor.execute("SELECT name FROM hosts WHERE status = 0")
        hostList = self.cursor.fetchall()
        if len(hostList) < 1:
            # throw and exception
            sys.exit(1)
        host = None
        if requested is not None:
            if (requested, ) in hostList and self.hostIsIdle(requested):
                host = requested  # If requested, exists, and idle, return it
            else:
                sys.exit(1)
        else:
            host = hostList[0][0]
        self.makeHostBusy(host)
        return host

    def makeHostBusy(self, name):
        """
        makes the status of host 'name' equal 1,
        making it 'busy'
        """
        host = (name, )
        self.cursor.execute("UPDATE hosts SET status = 1 WHERE name=?", host)
        self.database.commit()

    def makeHostDeployed(self, name):
        """
        makes the status of host 'name' equal 2,
        making it 'deployed' and/or in use
        """
        host = (name, )
        self.cursor.execute("UPDATE hosts SET status = 2 WHERE name=?", host)
        self.database.commit()

    def makeHostExpired(self, name):
        """
        makes the status of host 'name' equal 3,
        meaning its booking has ended and needs to be cleaned.
        """
        host = (name, )
        self.cursor.execute("UPDATE hosts SET status = 3 WHERE name=?", host)
        self.database.commit()

    def getExpiredHosts(self):
        """
        returns a list of all hosts with an expired booking that
        need to be cleaned.
        """
        self.cursor.execute("SELECT name FROM hosts where status = 3")
        host_tuples = self.cursor.fetchall()
        hosts = []
        for host in host_tuples:
            hosts.append(host[0])
        return hosts  # returns list of strings, not tuples

    def hostIsBusy(self, name):
        """
        returns True if the host is not idle
        """
        host = (name, )
        self.cursor.execute("SELECT status FROM hosts WHERE name=?", host)
        stat = self.cursor.fetchone()[0]
        if stat < 1:
            return False
        return True

    def hostIsIdle(self, name):
        """
        returns True if the host is idle.
        """
        return not self.hostIsBusy(name)

    def getAllHosts(self):
        """
        returns the whole host database.
        """
        self.cursor.execute("SELECT * FROM hosts")
        return self.cursor.fetchall()

    def close(self):
        """
        commits and closes connection to the database file.
        """
        self.database.commit()
        self.database.close()


class BookingDataBase:
    """
    Database to hold all active bookings for our servers.
    Database contains table bookings - can be same or different
    db file as the host database
    bookings contains a field for every json key from the pharos dashboard,
    plus a "status" integer which is either
    0   -   waiting to start
    1   -   started
    2   -   booking over

    As written, the pharos listener will immediately store all bookings that
    are both for your dev pods and not
    yet over, regardless of when the booking starts. Once the booking ends
    and the dev pod is cleaned, the booking is deleted to save space and cpu.
    """

    def __init__(self, path):
        """
        creates a BookingDataBase object with the database located
        at path. if path does not yet exist, it will be created.
        """
        self.database = sqlite3.connect(path)
        self.cursor = self.database.cursor()

    def createTable(self):
        """
        Creates table in the database to store booking information
        """
        try:
            self.cursor.execute("DROP TABLE bookings")
        except:
            pass
        self.cursor.execute("""CREATE TABLE bookings
        (id integer, resource_id integer, start double, end double,
            installer_name text, scenario_name text,
            purpose text, status integer, vpn text)""")
        self.database.commit()

    def checkAddBooking(self, booking):
        """
        This method accepts a JSON booking definition from the dashboard
        api and adds it to the database if it does not already exist.
        """
        # first, check if booking is already expired
        if time.time() > booking['end']:
            return
        # check if booking is in database already
        b_id = (booking['id'], )
        self.cursor.execute("SELECT * FROM bookings WHERE id=?", b_id)
        if len(self.cursor.fetchall()) > 0:  # booking already in the db
            return
        tup = (
                booking['id'],
                booking['resource_id'],
                booking['start'],
                booking['end'],
                booking['installer_name'],
                booking['scenario_name'],
                booking['purpose'],
                0,
                ''
                )
        self.cursor.execute(
                "INSERT INTO bookings VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)", tup)
        self.database.commit()

    def removeBooking(self, idNum):
        """
        deletes booking with given id from the database.
        """
        booking_id = (idNum, )
        self.cursor.execute("DELETE FROM bookings WHERE id=?", booking_id)

    def getBookings(self):
        """
        returns a list of all bookings.
        """
        self.cursor.execute("SELECT * FROM bookings")
        return self.cursor.fetchall()

    def setStatus(self, booking_id, status):
        """
        sets the status of the booking with booking id booking_id.
        as noted above, the status codes are:
        0 - not yet started
        1 - started, but not yet over
        2 - over, expired
        """
        data = (status, booking_id)
        self.cursor.execute("UPDATE bookings SET status=? WHERE id=?", data)
        self.database.commit()

    def setVPN(self, resource, uid):
        data = (uid, resource, 1)
        self.cursor.execute(
                "UPDATE bookings SET vpn=? WHERE resource_id=? AND status=?",
                data
            )
        self.database.commit()

    def getVPN(self):
        """
        returns a list of all vpn users associated with current
        bookings.
        """
        self.cursor.execute("SELECT vpn FROM bookings WHERE status=1")
        users_messy = self.cursor.fetchall()
        users = []
        for user in users_messy:
            user = user[0]  # get string rather than tuple
            user = user.strip()
            if len(user) < 1:
                continue
            users.append(user)  # a list of non-empty strings
        return users

    def close(self):
        """
        commits changes and closes connection to db file.
        """
        self.database.commit()
        self.database.close()
