import sqlite3
import sys
import time
"""
This class talks with a simple sqlite database and can select a free host 
when one is needed.
The layout of the database is:
    TABLE host:
        name <hostname> status <status_code> book_start <Unix timestamp> book_end <Unix timestamp>
    status_codes:
    0 - idle
    1 - deploying
    2 - deployed, in use
    3 - expired, ready to be reset
"""
class HostDataBase:

    def __init__(self,path):
        self.database = sqlite3.connect(path)
        self.cursor = self.database.cursor()


    #THIS METHOD SHOULD BE USED WITH CAUTION
    #IT WILL WIPE CLEAN THE DATABASE
    def resetHosts(self,hosts):
        try:
            self.cursor.execute("DROP TABLE hosts")
            self.createTable()
        except:
            pass
        
        hostNames = []
        for host in hosts:
            self.addHost(host)
    
    #This method will create the hosts table expected in the rest of the methods
    def createTable(self):
        self.cursor.execute("CREATE TABLE hosts (name text, status integer)")
        self.database.commit()


    def addHost(self,name):
        host = (name,)
        self.cursor.execute("INSERT INTO hosts VALUES (?,0) ",host)
        self.database.commit()
    
    def getHost(self,requested=None):
        self.cursor.execute("SELECT name FROM hosts WHERE status = 0")
        hostList = self.cursor.fetchall()
        if len(hostList) < 1:
            #throw and exception
            sys.exit(1)
        host = None
        if requested != None:
            if (requested,) in hostList and self.hostIsIdle(requested):
                host = requested #If a specific host is requested, it exists, and it is idle, return it
            else:
                #print "requested host "+requested+" is not available."
                #throw an exception
                sys.exit(1)
        else:
            host = hostList[0][0]
        self.makeHostBusy(host)
        return host

    def makeHostBusy(self,name):
        host = (name,)
        self.cursor.execute("UPDATE hosts SET status = 1 WHERE name=?",host)
        self.database.commit()

    def makeHostDeployed(self,name):
        host = (name,)
        self.cursor.execute("UPDATE hosts SET status = 2 WHERE name=?",host)
        self.database.commit()
    
    def makeHostExpired(self,name):
        host = (name,)
        self.cursor.execute("UPDATE hosts SET status = 3 WHERE name=?",host)
        self.database.commit()

    def getExpiredHosts(self):
        self.cursor.execute("SELECT name FROM hosts where status = 3")
        host_tuples = self.cursor.fetchall()
        hosts = []
        for host in host_tuples:
            hosts.append(host[0])
        return hosts #returns a list of strings, rather than tuples
    
    def hostIsBusy(self,name):
        host = (name,)
        self.cursor.execute("SELECT status FROM hosts WHERE name=?",host)
        stat = self.cursor.fetchone()[0]
        if stat < 1:
            return False
        return True
    
    def hostIsIdle(self,name):
        return not self.hostIsBusy(name)

    def getAllHosts(self):
        self.cursor.execute("SELECT * FROM hosts")
        return self.cursor.fetchall()
     
    def close(self):
        self.database.commit()
        self.database.close()

"""
Database to hold all active bookings for our servers.
Database contains table bookings
bookings contains a field for every json key from the pharos dashboard, plus a "status" integer which is either 
0   -   waiting to start
1   -   started
2   -   booking over
"""
class BookingDataBase:
    
    def __init__(self,path):
        self.database = sqlite3.connect(path)
        self.cursor = self.database.cursor()

    def createTable(self):
        try:
            self.cursor.execute("DROP TABLE bookings")
        except:
            pass
        self.cursor.execute("""CREATE TABLE bookings 
        (id integer, resource_id integer,start double, end double, installer_name text,scenario_name text,purpose text, status integer)""")
        self.database.commit()

    def checkAddBooking(self,booking):
        #first, check if booking is already expired
        if time.time() > booking['end']:
            return
        #check if booking is in database already
        b_id = (booking['id'],)
        self.cursor.execute("SELECT * FROM bookings WHERE id=?",b_id)
        if len(self.cursor.fetchall()) > 0: #if a task with the given id already in the db
            return
        data = (booking['id'],booking['resource_id'],booking['start'],booking['end'],booking['installer_name'],
                booking['scenario_name'],booking['purpose'],0)
        self.cursor.execute("INSERT INTO bookings VALUES (?,?,?,?,?,?,?,?)",data)
        self.database.commit()

    def removeBooking(self,idNum):
        booking_id = (idNum,)
        self.cursor.execute("DELETE FROM bookings WHERE id=?",booking_id)
    
    def getBookings(self):
        bookings = []
        self.cursor.execute("SELECT * FROM bookings")
        return self.cursor.fetchall()

    def setStatus(self,booking_id,status):
        data = (status,booking_id)
        self.cursor.execute("UPDATE bookings SET status=? WHERE id=?",data)
        self.database.commit()

    def close(self):
        self.database.commit()
        self.database.close()


