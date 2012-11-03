__author__ = 'Zygimantas Gatelis'

import socket
import re

class IRCClient():

    def __init__(self, connectionInfo):

        self.server = connectionInfo.server
        self.nick = connectionInfo.nick
        self.fullname = connectionInfo.fullname
        self.port = connectionInfo.port
        self.channels = []
        self.socket = None

        self.generalSysRegex = re.compile(r':[\w\.]+ \d{3} %s :?' % self.nick) # regex for system message

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
        
        data = self.socket.recv(1024*16)
        if data.find('PING') != -1:
            self.socket.send('PONG ' + data.split() [1] + '\r\n')
        return self.__parseMessage(data)

    def sendMessage(self,target, message):
        message = self.__makeMessage(message)
        self.socket.send('PRIVMSG {0} :{1}\r\n'.format(target, message))
        print 'PRIVMSG {0} :{1}\r\n'.format(target, message), "ZINUTE"

    def __makeMessage(self, message):
        """ make message to appropriate irc format
        """
        return message

    def __parseMessage(self, message):
        """ message format:
            :zeeegis!Zygimantas@427C27D7.5F26B8D7.81E3A2C9.IP PRIVMSG #hackforums :hi Fallen
            :jenrzzz!~jenrzzz@108-197-33-53.lightspeed.sndgca.sbcglobal.net JOIN #python-unregistered
            :schlaftier!~daniel@145.107.17.79.surfnet.utelisys.net QUIT :Ping timeout: 265 seconds


            sys message format:
            :lindbohm.freenode.net 372 zeeegis :- freenode runs an open proxy scanner. Your use of the network
            :holmes.freenode.net 451 * :You have not registered
            :verne.freenode.net 372 zeeegis :- [http://geeknic.org]

            :hitchcock.freenode.net 372 zeeegis :- many techniques in film-making.
        """
        print  "%s\n" % message

        if message.split(' ')[1] == 'NOTICE' or self.generalSysRegex.search(message):
            print 'SYS\n'
            lines = ':'.join(message.split(":")[2:]).split('\n')
            text = ''
            for line in ':'.join(message.split(":")[2:]).split('\n'):
                #text += ':'.join(line.split(":")[2:]) + '\n'
                text += self.generalSysRegex.sub("", line)

            return  {
                'message'  : text,
                'nick'     : 'sys',
                'username' : '',
                'host'     : '',
                'channel'  : 'all',
            }
        elif message.find(':') != -1 and message.split(':')[1].find('PRIVMSG')  != -1:
            print "zinute", ' '.join(message.split(" ")[3:])
            return {
                'nick'     : message.split(":")[1].split( "!" )[ 0 ],
                'username' : message.split("!")[1].split( "@" )[ 0 ],
                'host'     : message.split(" ")[0].split( "@" )[ 1 ],
                'channel'  : message.split(" ")[2],
                'message'  : ' '.join(message.split(" ")[3:])[1:],
            }
        #elif message.find()
        else:
            return  {
                'message'  : message,
                'nick'     : '',
                'username' : '',
                'host'     : '',
                'channel'  : '',
            }



    def getUsersInChannel(self):
        pass

    def getChannel(self):
        return self.channel

    def setChannel(self, channel):
        self.channel = channel

    def getNick(self):
        return self.nick

    channel = property(getChannel, setChannel, doc="current channel")
    nick = property(getNick, None, doc="Client nickname")


