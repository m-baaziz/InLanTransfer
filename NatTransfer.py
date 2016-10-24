from lib.Broadcaster import Broadcaster
from lib.Listener import Listener
from lib.Users import Users
from lib.Sender import Sender
from lib.ErrorDisplayer import ErrorDisplayer
import signal, sys, time, os, humanize
import Tkinter, Tkconstants, tkFileDialog
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
		self.localIp = ""
		self.computeLocalIp()
		self.broadcastIp.trace('w', self.computeLocalIp)
		self.name = StringVar(value="John")
		self.name.trace('w', self.parseName)
		self.waitingFilesToSend = {}

		self.threadsStarted = False
		# GUI : users buttons
		self.users = Users(frame, self.sendRequest)


	def parseName(self, *args):
		name = self.name.get().split(':')
		self.name.set(''.join(name))

	def setupNetworking(self):
		self.sender = Sender(self.name.get(), self.broadcastIp.get(), PORT)
		self.broadcaster = Broadcaster(self.sender)
		self.broadcaster.daemon = True
		self.broadcastListener = Listener(self.broadcastIp.get(), PORT, self.users, self.sender, self.waitingFilesToSend)
		self.broadcastListener.daemon = True
		self.localListener = Listener(self.localIp, PORT, self.users, self.sender, self.waitingFilesToSend)
		self.localListener.deamon = True
		self.users.activate()

	def run(self):
		# Threads ans Sender setup
		if self.threadsStarted == True:
			# This happens when we change the broadcast address
			self.endThreads()

		self.setupNetworking()
		self.threadsStarted = True
		try:
			self.broadcaster.start()
		except Exception as e:
			print "Error in Broadcaster Thread"
			raise
		try:
			self.broadcastListener.start()
		except Exception as e:
			print "Error in Broadcast Listener Thread"
			raise
		try:
			self.localListener.start()
		except Exception as e:
			print "Error in Local Listener Thread"
			raise

	def sendRequest(self, ip):
		print "sending REQUEST to " + ip
		filepath = tkFileDialog.askopenfilename()
		filename = filepath.split('/')
		filename = filename[len(filename)-1]
		print filepath
		try:
			size = os.path.getsize(filepath)
		except:
			print "file " + filename + "unreachble"
		else:
			size = humanize.naturalsize(size)
			print size
		self.sender.request(ip, filename+":"+size)
		self.waitingFilesToSend[filename] = filepath

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
		finally:
			s.close()

	# Need broadcast ip
	def computeLocalIp(self, *args):
		s = socket(AF_INET, SOCK_DGRAM)
		try:
			s.connect((self.broadcastIp.get(),80))
		except:
			errorDisplayer.set("Need to know the broadcast ip to compute the local ip")
		else:
			address = s.getsockname()[0]
			self.localIp = address
		finally:
			s.close()

	def endThreads(self):
		print "Waiting for threads to finish"
		self.localListener.stop()
		self.broadcastListener.stop()
		self.broadcaster.stop()
		self.users.terminate()
		self.localListener.join()
		self.broadcaster.join()
		self.broadcastListener.join()


	def terminate(self):
		try:
			self.endThreads()
		except:
			print "Threads were not initialized"
		finally:
			gui.destroy()
		


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

nameFrame = Frame(gui)
nameFrame.pack(side=BOTTOM)
nameLabel = Label(nameFrame, text="Name : ")
nameLabel.pack(side=LEFT)
nameEntry = Entry(nameFrame, textvariable=app.name)
nameEntry.pack(side=LEFT)

gui.protocol("WM_DELETE_WINDOW", app.terminate)
gui.mainloop()