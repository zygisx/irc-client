from reportlab.pdfbase.pdfutils import _fusc

__author__ = 'zee'

class IRCClient():

    def __init__(self, server, nick, fullname, port=6667):

        self.server = server
        self.nick = nick
        self.fullname = fullname
        self.port = port
        self.socket = None

    def connect(self):
        pass

    def receiveData(self):
        pass

    def sendMessage(self):
        pass

    def getUsersInChannel(self):
        pass


