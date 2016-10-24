from socket import *

class Sender:
	def __init__(self, name, broadcastIp, port):
		self.name = name
		self.port = port
		self.broadcastIp = broadcastIp
		self.so = socket(AF_INET, SOCK_DGRAM)
		self.so.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

	def send(self, msg, ip):
		if ip == self.broadcastIp:
			self.so.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		try:
			self.so.sendto(msg, (ip, self.port))
		except Exception as e:
			print e
			raise
		if ip == self.broadcastIp:
			self.so.setsockopt(SOL_SOCKET, SO_BROADCAST, 0)

	def ping(self):
		msg = self.name + ":PING:"
		self.send(msg, self.broadcastIp)

	def request(self, ip, filename, size):
		msg = self.name + ":REQUEST:" + filename + ":" + str(size)
		self.send(msg, ip)

	def end(self):
		msg = self.name + ":END:"
		self.send(msg, self.broadcastIp)

	def accept(self, ip, filename):
		msg = self.name + ":ACCEPT:" + filename
		self.send(msg, ip)

	def refuse(self, ip, filename):
		msg = self.name + ":REFUSE:" + filename
		self.send(msg, ip)

	def data(self, ip, filename, filesize, datasize, data):
		msg = self.name + ":DATA:" + filename + ":" + str(filesize) + ":" + str(datasize) + ":" + data
		self.send(msg, ip)

	def ack(self, ip, filename, filesize, datasize):
		msg = self.name + ":ACK:" + filename + ":" + str(filesize) + ":" + str(datasize)
		self.send(msg, ip)

	def eof(self, ip, filename):
		msg = self.name + ":EOF:" + filename
		self.send(msg, ip)