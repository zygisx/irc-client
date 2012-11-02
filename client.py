__author__ = 'Zygimantas Gatelis'

import socket

class IRCClient():

    def __init__(self, connectionInfo):

        self.server = connectionInfo.server
        self.nick = connectionInfo.nick
        self.fullname = connectionInfo.fullname
        self.port = connectionInfo.port
        self.channels = []
        self.socket = None

    def connect(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect((self.server, self.port))

        self.socket.send('NICK {0}\r\n'.format(self.nick))
        self.socket.send('USER {0} 8 * :{1}\r\n'.format(self.nick, self.fullname))

    def disconnect(self):
        """ Send QUIT messages to all channels
        """
        pass

    def joinChannel(self, channel):
        self.socket.send('JOIN {0}\r\n'.format(channel))
        self.channels.append(channel)

    def receiveData(self):
        
        data = self.socket.recv(1024)
        if data.find('PING') != -1:
            self.socket.send('PONG ' + data.split() [1] + '\r\n')
        return data
        

    def sendMessage(self, message):
        message = self.__makeMessage(message)
        self.socket.send(message)


        pass

    def __makeMessage(self, message):
        """ make message to appropriate irc format
        """
        return message

    def getUsersInChannel(self):
        pass

    def getChannel(self):
        return self.channel

    def setChannel(self, channel):
        self.channel = channel

    channel = property(getChannel, setChannel, doc="current channel")


