__author__ = 'Zygimantas Gatelis'

import socket
import re

class IRCClient():

    def __init__(self, connectionInfo):

        self.server = connectionInfo.server
        self.__nick = connectionInfo.nick
        self.fullname = connectionInfo.fullname
        self.port = connectionInfo.port
        self.channels = []
        self.socket = None

        self.generalSysRegex = re.compile(r':[\w\.]+ \d{3} %s :?' % self.nick) # regex for system messages
        self.channelSysRegex = re.compile(r':[\w\.]+ \d{3} %s =?\s*([&#]{1,2}[\w-]+) :?' % self.nick) # regex for channel sys messages

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

         #TODO implement message parsing by line not by whole message
#        message = ''
#        for line in data.split('\n'):
#            message += "%s\n" % self.__parseMessage(line)
#        return message
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

            :vector!~vector@host-1-185-230-24.midco.net JOIN #ubuntu
            :tankdriver!~quassel@193.170.133.31 QUIT :Remote host closed the connection
            :profiler1982!~wladimir@net66-0-245-109.mbb.telenor.rs PART #ubuntu


            sys message format:
            :lindbohm.freenode.net 372 zeeegis :- freenode runs an open proxy scanner. Your use of the network
            :holmes.freenode.net 451 * :You have not registered
            :verne.freenode.net 372 zeeegis :- [http://geeknic.org]

            :hitchcock.freenode.net 372 zeeegis :- many techniques in film-making.

            channel sys
            :adams.freenode.net 332 zeeegis #test :Welcome to freenode's test cha
            :adams.freenode.net 333 zeeegis #test sysdef!sysdef@debiancenter/foun
            :adams.freenode.net 353 zeeegis @ #test :zeeegis +kaffee +coon +[UCF]


        """
        #TODO PART
        print  "%s\n" % message

        match = self.channelSysRegex.search(message)
        if match:
            print match.group(1), 'Founded channel'

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
                'channel'  : match.group(1),
            }
        elif message.split(' ')[1] == 'NOTICE' or self.generalSysRegex.search(message):
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
                'channel'  : message.split(" ")[2].rstrip('\r\n'),
                'message'  : ' '.join(message.split(" ")[3:])[1:],
            }
        elif message.find(':') != -1 and message.split(':')[1].find('QUIT')  != -1:
            return {
                'nick'     : message.split(":")[1].split( "!" )[ 0 ],
                'username' : message.split("!")[1].split( "@" )[ 0 ],
                'host'     : message.split(" ")[0].split( "@" )[ 1 ],
                'channel'  : 'all',
                'message'  : "QUIT - {0}".format(' '.join(message.split(" ")[2:])[1:]),
            }
        elif message.find(':') != -1 and message.split(':')[1].find('JOIN')  != -1:
            return {
                'nick'     : message.split(":")[1].split( "!" )[ 0 ],
                'username' : message.split("!")[1].split( "@" )[ 0 ],
                'host'     : message.split(" ")[0].split( "@" )[ 1 ],
                'channel'  : message.split(" ")[2].rstrip('\r\n'),
                'message'  : "JOINED {0} ".format(message.split(" ")[2])
            }
        elif message.find(':') != -1 and message.split(':')[1].find('PART')  != -1:
            return {
                'nick'     : message.split(":")[1].split( "!" )[ 0 ],
                'username' : message.split("!")[1].split( "@" )[ 0 ],
                'host'     : message.split(" ")[0].split( "@" )[ 1 ],
                'channel'  : message.split(" ")[2].rstrip('\r\n'),
                'message'  : "LEFT {0} ".format(message.split(" ")[2])
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

    def __getChannel(self):
        return self.channel

    def __setChannel(self, channel):
        self.channel = channel

    def __getNick(self):
        return self.__nick
    def __setNick(self, value):
        self.__nick = value

    channel = property(__getChannel, __setChannel, doc="current channel")
    nick = property(__getNick, __setNick, doc="Client nickname")


