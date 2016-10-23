from lib.Broadcaster import Broadcaster
from lib.Listener import Listener
from lib.Users import Users
from lib.Sender import Sender
from lib.ErrorDisplayer import ErrorDisplayer
import sys
import time
import Tkinter
from Tkinter import *
import threading
from socket import *

PORT = 825
DEFAULT_BROADCAST_IP = "192.168.0.255"

gui = Tk()

error = StringVar()
errorDisplayer = ErrorDisplayer(error)

class NatTransfer:
	def __init__(self):
		self.broadcastIp = StringVar(value=DEFAULT_BROADCAST_IP)
		self.localIp = self.computeLocalIp()
		self.name = StringVar(value="John")

		# Threads ans Sender setup
		self.setupNetworking()
		# GUI : users buttons
		self.users = Users(frame, self.sendRequest)

	def setupNetworking(self):
		self.sender = Sender(self.name.get(), self.broadcastIp.get(), PORT)
		self.broadcaster = Broadcaster(self.sender)
		self.broadcaster.daemon = True
		self.listener = Listener(self.broadcastIp.get(), self.localIp, PORT, self.users)
		self.listener.daemon = True

	def run(self):
		if threadsStarted == True:
			# This happens when we change the broadcast address
			self.broadcaster.stop()
			self.listener.stop()
			self.setupNetworking()
		threadsStarted = True
		try:
			self.broadcaster.start()
		except Exception as e:
			print "Error in Broadcaster Thread"
		try:
			self.listener.start()
		except Exception as e:
			print "Error in Listener Thread"
			raise

	def sendRequest(self, ip):
		print "sending REQUEST to " + ip
		self.sender.request(ip)

	# Need internet connection
	def computeBroadcastIp(self):
		s = socket(AF_INET, SOCK_DGRAM)
		try:
			s.connect(("google.com",80))
		except:
			errorDisplayer.set("Need internet connection")
		else:
			address = s.getsockname()[0].split('.')
			address[3] = "255"
			address = ('.').join(address)
			self.broadcastIp.set(address)
			self.computeLocalIp()
		finally:
			s.close()

	# Need broadcast ip
	def computeLocalIp(self)
		s = socket(AF_INET, SOCK_DGRAM)
		try:
			s.connect((self.broadcastIp,80))
		except:
			errorDisplayer.set("Need to know the broadcast ip to compute the local ip")
		else:
			address = s.getsockname()[0]
			self.localIp = address
		finally:
			s.close()


gui.wm_title("NatTransfer")
errorFrame = Frame(gui)
errorFrame.pack(side=TOP)
errorLabel = Label(errorFrame, textvariable=errorDisplayer.error, fg="red")
errorLabel.pack(side=BOTTOM)
frame = Frame(gui)
frame.pack(side=TOP)
subFrame = Frame(gui)
subFrame.pack(side=BOTTOM)
label = Label(subFrame, text="Broadcast Address : ")
label.pack(side=LEFT)

app = NatTransfer()


entry = Entry(subFrame, textvariable=app.broadcastIp)
entry.pack(side=LEFT)
computeBroadcastBtn = Button(subFrame, text="Calculate", command= app.computeBroadcastIp)
computeBroadcastBtn.pack(side=LEFT)
startBtn = Button(subFrame, text="Start", command= app.run)
startBtn.pack(side=LEFT)

threadsStarted = False


gui.mainloop()