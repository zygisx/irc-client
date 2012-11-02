__author__ = 'Zygimantas Gatelis'

import socket

class IRCClient():

    def __init__(self, server, nick, fullname, port=6667):

        self.server = server
        self.nick = nick
        self.fullname = fullname
        self.port = port
        self.channels = {}
        self.socket = None

    def connect(self):
        irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        irc_socket.connect((self.server, self.port))

        irc_socket.send('NICK {0}\r\n'.format(self.nick))
        irc_socket.send('USER {0} 8 * :{1}\r\n'.format(self.nick, self.fullname))

    def joinChannel(self, channel):
        self.socket.send('JOIN {0}\r\n'.format(channel))
        self.channels[channel] = ChannelManager(channel, self.socket)

    def receiveData(self):
        
        data = self.socket.recv(1024)
        if data.find('PING') != -1:
            self.socket.send('PONG ' + data.split() [1] + '\r\n')
        return data
        

    def sendMessage(self, message):
        pass

    def __makeMessage(self, message):
        pass

    def getUsersInChannel(self):
        pass

    def getChannel(self):
        return self.channel

    def setChannel(self, channel):
        self.channel = channel

    channel = property(getChannel, setChannel, doc="current channel")

class ChannelManager():
    pass

