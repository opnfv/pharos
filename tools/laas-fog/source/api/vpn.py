from abc import ABCMeta, abstractmethod
import ldap
import os
import random
from base64 import b64encode
from database import BookingDataBase


class VPN_BaseClass:
    """
    the vpn handler abstract class / interface

    """
    __metaclass__ = ABCMeta

    @abstractmethod
    def __init__(self, config):
        """
        config is the parsed vpn.yaml file
        """
        pass

    @abstractmethod
    def makeNewUser(self, user=None):
        """
        This method is called when a vpn user is needed.
        This method should create a vpn user in whatever
        runs the vpn in our infrastructure. returns the
        credentials for the vpn user and some uid
        that will be associated with the booking in the
        database. This uid is used to track the vpn user and
        to delete the user when there are no bookings associated
        with that uid.
        """
        user = "username"
        passwd = "password"
        uid = "some way for you to identify this user in the database"
        return user, passwd, uid

    @abstractmethod
    def removeOldUsers(self):
        """
        checks the list of all vpn users against a list of
        vpn users associated with active bookings and removes
        users who dont have an active booking

        If you want your vpn accounts to be persistent,
        you can just ignore this
        """
        pass


names = [
    'frodo baggins', 'samwise gamgee', 'peregrin took', 'meriadoc brandybuck',
    'bilbo baggins', 'gandalf grey', 'aragorn dunadan', 'arwen evenstar',
    'saruman white', 'pippin took', 'merry brandybuck', 'legolas greenleaf',
    'gimli gloin', 'anakin skywalker', 'padme amidala', 'han solo',
    'jabba hut', 'mace windu', 'sount dooku', 'qui-gon jinn',
    'admiral ackbar', 'emperor palpatine'
]


class VPN:
    """
    This class communicates with the ldap server to manage vpn users.
    This class extends the above ABC, and implements the makeNewUser,
    removeOldUser, and __init__ abstract functions you must override to
    extend the VPN_BaseClass
    """

    def __init__(self, config):
        """
        init takes the parsed vpn config file as an arguement.
        automatically connects and authenticates on the ldap server
        based on the configuration file
        """
        self.config = config
        server = config['server']
        self.uri = "ldap://"+server

        self.conn = None
        user = config['authentication']['user']
        pswd = config['authentication']['pass']
        if os.path.isfile(pswd):
            pswd = open(pswd).read()
        self.connect(user, pswd)

    def connect(self, root_dn, root_pass):
        """
        Opens a connection to the server in the config file
        and authenticates as the given user
        """
        self.conn = ldap.initialize(self.uri)
        self.conn.simple_bind_s(root_dn, root_pass)

    def addUser(self, full_name, passwd):
        """
        Adds a user to the ldap server. Creates the new user with the classes
        and in the directory given in the config file.
        full_name should be two tokens seperated by a space. The first token
        will become the username
        private helper function for the makeNewUser()
        """
        first = full_name.split(' ')[0]
        last = full_name.split(' ')[1]
        user_dir = self.config['directory']['user']
        user_dir += ','+self.config['directory']['root']
        dn = "uid=" + first + ',' + user_dir
        record = [
                ('objectclass', ['top', 'inetOrgPerson']),
                ('uid', first),
                ('cn', full_name),
                ('sn', last),
                ('userpassword', passwd),
                ('ou', self.config['directory']['user'].split('=')[1])
                ]
        self.conn.add_s(dn, record)
        return dn

    def makeNewUser(self, name=None):
        """
        creates a new user in the ldap database, with the given name
        if supplied. If no name is given, we will try to select from the
        pre-written list above, and will resort to generating a random string
        as a username if the preconfigured names are all taken.
        Returns the username and password the user needs to authenticate, and
        the dn that we can use to manage the user.
        """
        if name is None:
            i = 0
            while not self.checkName(name):
                i += 1
                if i == 20:
                    name = self.randoString(8)
                    name += ' '+self.randoString(8)
                    break  # generates a random name to prevent infinite loop
                name = self.genUserName()
        passwd = self.randoString(15)
        dn = self.addUser(name, passwd)
        return name, passwd, dn

    def checkName(self, name):
        """
        returns true if the name is available
        """
        if name is None:
            return False
        uid = name.split(' ')[0]
        base = self.config['directory']['user'] + ','
        base += self.config['directory']['root']
        filtr = '(uid=' + uid + ')'
        timeout = 5
        ans = self.conn.search_st(
                base,
                ldap.SCOPE_SUBTREE,
                filtr,
                timeout=timeout
                )
        return len(ans) < 1

    @staticmethod
    def randoString(n):
        """
        uses /dev/urandom to generate a random string of length n
        """
        n = int(n)
        # defines valid characters
        alpha = 'abcdefghijklmnopqrstuvwxyz'
        alpha_num = alpha
        alpha_num += alpha.upper()
        alpha_num += "0123456789"

        # generates random string from /dev/urandom
        rnd = b64encode(os.urandom(3*n)).decode('utf-8')
        random_string = ''
        for char in rnd:
            if char in alpha_num:
                random_string += char
        return str(random_string[:n])

    def genUserName(self):
        """
        grabs a random name from the list above
        """
        i = random.randint(0, len(names) - 1)
        return names[i]

    def deleteUser(self, dn):
        self.conn.delete(dn)

    def getAllUsers(self):
        """
        returns all the user dn's in the ldap database in a list
        """
        base = self.config['directory']['user'] + ','
        base += self.config['directory']['root']
        filtr = '(objectclass='+self.config['user']['objects'][-1]+')'
        timeout = 10
        ans = self.conn.search_st(
                base,
                ldap.SCOPE_SUBTREE,
                filtr,
                timeout=timeout
                )
        users = []
        for user in ans:
            users.append(user[0])  # adds the dn of each user
        return users

    def removeOldUsers(self):
        """
        removes users from the ldap server who dont have any active bookings.
        will not delete a user if their uid's are named in the config
        file as permanent users.
        """
        db = self.config['database']
        # the dn of all users who have an active booking
        active_users = BookingDataBase(db).getVPN()
        all_users = self.getAllUsers()
        for user in all_users:
            # checks if they are a permanent user
            if self.is_permanent_user(user):
                continue
            # deletes the user if they dont have an active booking
            if user not in active_users:
                self.deleteUser(user)

    def is_permanent_user(self, dn):
        for user in self.config['permanent_users']:
            if (user in dn) or (dn in user):
                return True
        return False


VPN_BaseClass.register(VPN)
