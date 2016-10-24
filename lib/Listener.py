from StoppableThread import StoppableThread
import threading
from socket import *
from select import select
import tkMessageBox
import os

READ_SOCKET_TIMEOUT = 3

DATAGRAM_NAME_POS = 0
DATAGRAM_ACTION_POS = 1
DATAGRAM_FILENAME_POS = 2
DATAGRAM_FILESIZE_POS = 3
DATAGRAM_DATASIZE_POS = 4
DATAGRAM_DATA_POS = 5

BLOCKSIZE = 8192

class Listener(StoppableThread):

	def __init__(self, ip, port, users, sender, waitingFilesToSend):
		print "Listener Thread initalizing"
		StoppableThread.__init__(self)
		self.ip = ip
		self.port = port
		self.users = users
		self.sender = sender
		self.waitingFilesToSend = waitingFilesToSend
		self.receivedFilesDescriptors = {}
		self.sentFilesDescriptors = {}
		self.receivedDataSize = {}

	def run(self):
		so = socket(AF_INET, SOCK_DGRAM)
		so.setblocking(0)
		try:
			so.bind((self.ip, self.port))
		except Exception as e:
			print "Binding error (address already in use ?)"
		else:
			print "Listening on " + self.ip + " ... "
			while not self.isStopped():
				ready = select([so], [], [], READ_SOCKET_TIMEOUT)
				if ready[0]:
					msg = so.recvfrom(10000)
					data = msg[0].split(':', DATAGRAM_DATA_POS) # Knowing that data is last, doing this we dont split data content
					name = data[DATAGRAM_NAME_POS]
					action = data[DATAGRAM_ACTION_POS]
					ip = msg[1][0]
					# print name + " : " + action
					if not self.isStopped():
						if action == "PING":
							self.users.add((name, ip))
						elif action == "END":
							self.users.remove((name, ip))
						elif action == "REQUEST":
							filename = data[DATAGRAM_FILENAME_POS]
							size = data[DATAGRAM_FILESIZE_POS]
							message = name + " wants to send you " + filename + " (" + size + ")"
							result = tkMessageBox.askquestion("Receive", message)
							if result == "yes":
								self.sender.accept(ip, filename)
								fd = open(filename, 'a')
								self.receivedDataSize[filename] = 0
								self.receivedFilesDescriptors[filename] = fd
							else:
								self.sender.refuse(ip, filename)
						elif action == "ACCEPT":
							filename = data[DATAGRAM_FILENAME_POS]
							filesize = os.path.getsize(self.waitingFilesToSend[filename])
							if filename in self.waitingFilesToSend and os.path.exists(self.waitingFilesToSend[filename]):
								fd =open(self.waitingFilesToSend[filename], 'rb')
								self.sentFilesDescriptors[filename] = fd
								self.sendNextFileBlock(fd, ip, filename, filesize, 0)
						elif action == "ACK":
							print "Receiving Ack"
							try:
								filename = data[DATAGRAM_FILENAME_POS]
								size = data[DATAGRAM_FILESIZE_POS]
								datasize = data[DATAGRAM_DATASIZE_POS]
								fd = self.sentFilesDescriptors[filename]
								self.sendNextFileBlock(fd, ip, filename, size, int(datasize))
							except Exception as e:
								print e
								raise
						elif action == "REFUSE":
							filename = data[DATAGRAM_FILENAME_POS]
							if filename in self.waitingFilesToSend:
								print "Not Sending the file ... "
								del self.waitingFilesToSend[filename]
						elif action == "DATA":
							filename = data[DATAGRAM_FILENAME_POS]
							filesize = data[DATAGRAM_FILESIZE_POS]
							datasize = data[DATAGRAM_DATASIZE_POS]
							dataContent = data[DATAGRAM_DATA_POS]
							realDataSize = len(dataContent)
							self.receivedDataSize[filename] += realDataSize
							print "Receiving " + str(realDataSize) + " of " + filesize
							fd = self.receivedFilesDescriptors[filename]
							try:
								fd.write(dataContent)
								self.sender.ack(ip, filename, filesize, self.receivedDataSize[filename])
							except Exception as e:
								print e
								raise
						elif action == "EOF":
							print "End Of File !!"
							filename = data[DATAGRAM_FILENAME_POS]
							fd = self.receivedFilesDescriptors[filename]
							fd.close()
							del self.receivedFilesDescriptors[filename]
							del self.receivedDataSize[filename]

		finally:
			print "closing client socket ("+self.ip+")"
			so.close()
			exit(1)

	def sendNextFileBlock(self, fd, ip, filename, filesize, sentDataSize):
		print "Sending the next file block ... "
		try:
			if sentDataSize == filesize:
				fd.close()
				self.sender.eof(ip, filename)
				del self.waitingFilesToSend[filename]
				del self.sentFilesDescriptors[filename]
			else:
				print str(sentDataSize) + " / " + str(filesize)
				fd.seek(sentDataSize)
				packet = fd.read(BLOCKSIZE)
				if packet:
					self.sender.data(ip, filename, str(filesize), str(len(packet)), packet)
		except Exception as e:
			print e 
			raise
