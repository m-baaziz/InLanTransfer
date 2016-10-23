from lib.Broadcaster import Broadcaster
from lib.Listener import Listener
from lib.Users import Users
from lib.Sender import Sender
import sys
import time
import Tkinter
from Tkinter import *
import threading

BROADCAST_IP = "192.168.56.255"
PORT = 825

# actions
BROADCAST = 1
LISTEN = 0

#GUI

FRAME_WIDTH = 200
FRAME_HEIGHT = 100

class NatTransfer:
	def __init__(self, action):
		self.action = int(action)
		self.sender = Sender("John", BROADCAST_IP, PORT)
		#Threads
		if self.action == BROADCAST:
			self.broadcaster = Broadcaster(self.sender)
			self.broadcaster.daemon = True
		if self.action == LISTEN:
			# GUI
			self.gui = Tk()
			self.frame = Frame(self.gui, width=FRAME_WIDTH, height=FRAME_HEIGHT)
			self.users = Users(self.frame, self.sendRequest)

			self.listener = Listener(BROADCAST_IP, PORT, self.users)
			self.listener.daemon = True

	def run(self):
		try:
			if self.broadcaster:
				self.broadcaster.start()
		except Exception as e:
			if self.action == 1:
				print "Error in Broadcaster Thread"
		try:
			if self.listener:
				self.listener.start()
				self.display()
		except Exception as e:
			if self.action == 0:
				print "Error in Listener Thread"
				raise
		while 1:
			time.sleep(1)

	def sendRequest(self):
		self.sender.request("192.168.0.13")

	def display(self):
		self.gui.wm_title("NatTransfer")
		self.frame.pack(side = BOTTOM)
		label = Label(self.frame, text="filepath")
		label.pack(side=LEFT)
		entry = Entry(self.frame)
		entry.pack(side=RIGHT)
		self.gui.mainloop()


app = NatTransfer(sys.argv[1])
app.run()