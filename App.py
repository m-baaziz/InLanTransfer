from lib.Broadcaster import Broadcaster
from lib.Listener import Listener
from lib.Users import Users
from lib.Sender import Sender
from lib.ErrorDisplayer import ErrorDisplayer
import sys, time, os
import Tkinter, Tkconstants, tkFileDialog
from Tkinter import *
import threading
from socket import *

PORT = 825
DEFAULT_BROADCAST_IP = ""

gui = Tk()

error = StringVar()
errorDisplayer = ErrorDisplayer(error)

class App:
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
		self.listener = Listener('', PORT, self.users, self.sender, self.waitingFilesToSend, progressBarFrame)
		self.listener.deamon = True
		self.users.activate()

	def run(self):
		# Threads and Sender setup
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
			self.listener.start()
		except Exception as e:
			print "Error in Local Listener Thread"
			raise

	def sendRequest(self, ip):
		print "sending REQUEST to " + ip
		filepath = tkFileDialog.askopenfilename().encode('utf-8')
		filename = filepath.split('/')
		filename = filename[len(filename)-1]
		try:
			size = os.path.getsize(filepath)
		except:
			print "file " + filename + "unreachble"
		else:
			self.sender.request(ip, filename, size)
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
		self.listener.stop()
		self.broadcaster.stop()
		self.users.terminate()
		self.listener.join()
		self.broadcaster.join()


	def terminate(self):
		try:
			self.endThreads()
		except:
			print "Threads were not initialized"
		finally:
			gui.destroy()
		


gui.wm_title("InLanTransfer")
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

app = App()


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

progressBarFrame = Frame(gui)
progressBarFrame.pack(side=BOTTOM)

gui.protocol("WM_DELETE_WINDOW", app.terminate)
gui.mainloop()