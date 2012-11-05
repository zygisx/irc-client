#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  irc.py

import wx
import threading
import socket

URL = 'chat.freenode.net'
PORT = 6667
NICK = 'zeeegis'
FULL_NAME = 'Zygimantas'
CHANNEL = '#ubuntu'

DATA_RECEIVED_EVENT = wx.NewId()

def EVT_RESULT(win, func):
	"""Define Result Event."""
	win.Connect(-1, -1, DATA_RECEIVED_EVENT, func)

class ResultEvent(wx.PyEvent):

	def __init__(self, data):
		"""Init Result Event."""
		wx.PyEvent.__init__(self)
		self.SetEventType(DATA_RECEIVED_EVENT)
		self.data = data

class Worker(threading.Thread):
	
	def __init__(self, notify_window):
		"""Init Worker Thread Class."""
		threading.Thread.__init__(self)
		self._notify_window = notify_window
		self.start()
		
	def run(self):
		irc_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		irc_socket.connect((URL, PORT))

		irc_socket.send('NICK {0}\r\n'.format(NICK))
		irc_socket.send('USER {0} 8 * :{1}\r\n'.format(NICK, FULL_NAME))
		irc_socket.send('JOIN {0}\r\n'.format(CHANNEL))
		while 1:
			data = irc_socket.recv(1024)
			if data.find('PING') != -1:
				irc_socket.send('PONG ' + data.split() [1] + '\r\n')
			wx.PostEvent(self._notify_window, ResultEvent(data + '\n'))
			print data
			
		self.irc_socket.close()
		



class MainFrame(wx.Frame):

	def __init__(self):
		wx.Frame.__init__(self, None, -1, 'IRC Client')

		#panel = wx.Panel(self, -1)
		self.received  = wx.TextCtrl(self, style=wx.TE_MULTILINE)
		wx.Frame.Connect(self, -1, -1, DATA_RECEIVED_EVENT, self.onDataReceived)
		
		#EVT_RESULT(self,self.onDataReceived)
		
		#self.received  = wx.TextCtrl(panel, pos=(3, 3), size=(250, 150), style=wx.TE_MULTILINE)
		#wx.TextCtrl(panel, pos=(3, 3), size=(250, 150))
		
		self.Bind(wx.EVT_CLOSE, self.OnCloseWindow)
		
		self.worker = Worker(self)
		self.Show()
		
	def onDataReceived(self, event):
		self.received.AppendText(event.data)
		
	def OnCloseWindow(self, event):

		self.Close()

def main():
	ex = wx.App()
	MainFrame()
	ex.MainLoop()    
	return 0

if __name__ == '__main__':
	main()

