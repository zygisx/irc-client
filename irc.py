#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  irc.py

import wx
import threading
import socket
from client import  IRCClient

URL = 'chat.freenode.net'
PORT = 6667
NICK = 'zeeegis'
FULL_NAME = 'Zygimantas'
CHANNEL = '#ubuntu'

DATA_RECEIVED_EVENT = wx.NewId()
DATA_SEND_EVENT = wx.NewId()

class DataReceivedEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(DATA_RECEIVED_EVENT)
        self.data = data

class DataSendEvent(wx.PyEvent):
    def __init__(self, target, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(DATA_SEND_EVENT)
        self.target = target
        self.data = data

class ConnectionInfo():
    """ class for grouping connection information in one structure
    """
    server = URL
    port = PORT
    password = ''
    nick = NICK
    fullname = FULL_NAME

class Worker(threading.Thread):

    def __init__(self, notify_window, client):
        """Init Worker Thread Class."""
        threading.Thread.__init__(self)
        self._notify_window = notify_window
        self._client = client
        self.start()

		
    def run(self):

        while 1:
            data = self._client.receiveData()
            wx.PostEvent(self._notify_window, DataReceivedEvent(data))

class ChatFrame(wx.Frame):
    """ window for chatting in one channel
    """
    def __init__(self, parent, title):
        wx.Frame.__init__(self, parent, -1, title)
        panel = wx.Panel(self, -1)
        self.__received  = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY, size=(500, 600))
        wx.Frame.Connect(self, -1, -1, DATA_RECEIVED_EVENT, self.onDataReceived)

        label =  wx.StaticText(panel, wx.ID_ANY, 'Text: ')
        self.__input = wx.TextCtrl(panel, size=(400, 20))
        self.__button = wx.Button(panel, -1, "Send")
        self.Bind(wx.EVT_BUTTON, self.onSend, self.__button)


        main_sizer = wx.BoxSizer(wx.VERTICAL)
        input_sizer = wx.BoxSizer(wx.HORIZONTAL)



        input_sizer.Add(label, 0, wx.ALL, 5)
        input_sizer.Add(self.__input, 0, wx.ALL, 5)
        input_sizer.Add(self.__button, 0, wx.ALL, 5)
        input_sizer.Fit(panel)

        main_sizer.Add(self.__received,  0, wx.ALL, 5)
        main_sizer.Add(input_sizer, 0, wx.ALL, 5)
        panel.SetSizer(main_sizer)
        main_sizer.Fit(self)

        #self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)

        self.Show()
		
    def onDataReceived(self, event):
        text = "%s: %s\n" %  (event.data['nick'], event.data['message'])

        self.__received.AppendText(text.decode('utf-8'))

    def onSend(self, event):
        """ send button handler. Notify parent frame about send operation
        """
        wx.PostEvent(self.GetParent(), DataSendEvent(self.GetTitle(), self.__input.GetValue() + '\n'))
        self.__received.AppendText("{0}: {1}\n".format(self.GetParent().getClient().nick, self.__input.GetValue()))
        self.__input.Clear()


class MainFrame(wx.Frame):
    """ Parent frame.
    """
    def __init__(self):
        wx.Frame.__init__(self, None, -1, 'IRC Client')
        wx.Frame.Connect(self, -1, -1, DATA_RECEIVED_EVENT, self.onDataReceived)
        wx.Frame.Connect(self, -1, -1, DATA_SEND_EVENT, self.onDataSend)

        self.frames = {}
        self.__client = None

        self.topPanel = wx.Panel(self)
        self.bottomPanel = wx.Panel(self)


        #top panel
        serverLabel = wx.StaticText(self.topPanel, wx.ID_ANY, 'Server: ')
        self.serverInput = wx.TextCtrl(self.topPanel, wx.ID_ANY, '')

        portLabel = wx.StaticText(self.topPanel, wx.ID_ANY, 'Port: ')
        self.portInput = wx.TextCtrl(self.topPanel, wx.ID_ANY, '')

        nickLabel = wx.StaticText(self.topPanel, wx.ID_ANY, 'Nick: ')
        self.nickInput = wx.TextCtrl(self.topPanel, wx.ID_ANY, '')

        nameLabel = wx.StaticText(self.topPanel, wx.ID_ANY, 'Full name: ')
        self.nameInput = wx.TextCtrl(self.topPanel, wx.ID_ANY, '')

        self.connectButton = wx.Button(self.topPanel, wx.ID_ANY, 'Connect')
        self.disconnectButton = wx.Button(self.topPanel, wx.ID_ANY, 'Disconnect')
        self.disconnectButton.Enable(False)
        self.Bind(wx.EVT_BUTTON, self.onConnect, self.connectButton)
        self.Bind(wx.EVT_BUTTON, self.onDisconnect, self.disconnectButton)

        topSizer = wx.BoxSizer(wx.VERTICAL)
        serverSizer = wx.BoxSizer(wx.HORIZONTAL)
        portSizer = wx.BoxSizer(wx.HORIZONTAL)
        nickSizer = wx.BoxSizer(wx.HORIZONTAL)
        fullnameSizer = wx.BoxSizer(wx.HORIZONTAL)
        buttonSizer = wx.BoxSizer(wx.HORIZONTAL)

        serverSizer.Add(serverLabel, 0, wx.ALL, 5)
        serverSizer.Add(self.serverInput, 0, wx.ALL, 5)

        portSizer.Add(portLabel, 0, wx.ALL, 5)
        portSizer.Add(self.portInput, 0, wx.ALL, 5)

        nickSizer.Add(nickLabel, 0, wx.ALL, 5)
        nickSizer.Add(self.nickInput, 0, wx.ALL, 5)

        fullnameSizer.Add(nameLabel, 0, wx.ALL, 5)
        fullnameSizer.Add(self.nameInput, 0, wx.ALL, 5)

        buttonSizer.Add(self.connectButton, 0, wx.ALL, 5)
        buttonSizer.Add(self.disconnectButton, 0, wx.ALL, 5)


        topSizer.Add(serverSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(portSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(nickSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(fullnameSizer, 0, wx.ALL|wx.EXPAND, 5)
        topSizer.Add(buttonSizer, 0, wx.ALL|wx.EXPAND, 5)

        topSizer.Add(wx.StaticLine(self.topPanel), 0, wx.ALL|wx.EXPAND, 5)

        self.topPanel.SetSizerAndFit(topSizer)

        # bottom panel
        bottomSizer = wx.BoxSizer(wx.HORIZONTAL)
        channel_label =  wx.StaticText(self.bottomPanel, wx.ID_ANY, 'Channel: ')
        self.channel = wx.TextCtrl(self.bottomPanel)
        self.button = wx.Button(self.bottomPanel, -1, "Join channel")
        self.Bind(wx.EVT_BUTTON, self.onChannelJoin, self.button)

        bottomSizer.Add(channel_label, 0, wx.ALL, 5)
        bottomSizer.Add(self.channel, 0, wx.ALL, 5)
        bottomSizer.Add(self.button, 0, wx.ALL, 5)

        self.bottomPanel.SetSizerAndFit(bottomSizer)
        self.bottomPanel.Enable(False)

        mainSizer = wx.BoxSizer(wx.VERTICAL)
        mainSizer.Add(self.topPanel, 0, wx.ALL|wx.EXPAND, 5)
        mainSizer.Add(self.bottomPanel, 0, wx.ALL|wx.EXPAND, 5)

        self.SetSizer(mainSizer)
        mainSizer.Fit(self)

        self.Show()

    def onDataReceived(self, event):
        """ parent frame gets data and put them in particular channel frame
        """

        if event.data.has_key('channel') and event.data['channel'] != '' and event.data['channel'] != 'all':
            wx.PostEvent(self.frames[event.data['channel']], DataReceivedEvent(event.data))
        else:
            #TODO add text top main window
            for v in self.frames.itervalues():
                wx.PostEvent(v, DataReceivedEvent(event.data))


    def onDataSend(self, event):
        #TODO send message with PRIVMSG channel_name
        self.__client.sendMessage(event.target, event.data)

    def onChannelJoin(self, event):
        """ when joining new channel we create new ChatFrame for chatting in particular channel
        """
        self.__client.joinChannel(self.channel.GetValue())

        self.frames[self.channel.GetValue()] = ChatFrame(self, self.channel.GetValue())
        self.frames[self.channel.GetValue()].Show()

        self.channel.Clear()

    def onConnect(self, event):
        info = ConnectionInfo()
        if not self.serverInput.IsEmpty(): info.server = self.serverInput.GetValue()
        if not self.portInput.IsEmpty(): info.port = self.portInput.GetValue()
        if not self.nickInput.IsEmpty(): info.nick = self.nickInput.GetValue()
        if not self.nameInput.IsEmpty(): info.fullname = self.nameInput.GetValue()

        self.__client = IRCClient(info)
        self.__client.connect()

        self.worker = Worker(self, self.__client)

        self.connectButton.Enable(False)
        self.disconnectButton.Enable(True)
        self.bottomPanel.Enable(True)

    def onDisconnect(self, event):
        self.__client = None

        self.connectButton.Enable(True)
        self.disconnectButton.Enable(False)
        self.bottomPanel.Enable(False)

    def removeChildFrame(self, channel):
        del self.frames[channel]

    def getClient(self):
        return self.__client


def main():
    ex = wx.App(False)
    MainFrame()
    ex.MainLoop()
    return 0

if __name__ == '__main__':
    main()

