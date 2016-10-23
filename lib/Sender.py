from socket import *

class Sender:
	def __init__(self, name, broadcastingIp, port):
		self.name = name
		self.port = port
		self.broadcastingIp = broadcastingIp
		self.so = socket(AF_INET, SOCK_DGRAM)
		self.so.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)

	def send(self, msg, ip):
		if ip == self.broadcastingIp:
			self.so.setsockopt(SOL_SOCKET, SO_BROADCAST, 1)
		self.so.sendto(msg, (ip, self.port))
		if ip == self.broadcastingIp:
			self.so.setsockopt(SOL_SOCKET, SO_BROADCAST, 0)

	def ping(self):
		msg = self.name + ":PING:"
		self.send(msg, self.broadcastingIp)

	def request(self, ip):
		msg = self.name + ":REQUEST:"
		self.send(msg, ip)

	def end(self):
		msg = self.name + ":END:"
		self.send(msg, self.broadcastingIp)