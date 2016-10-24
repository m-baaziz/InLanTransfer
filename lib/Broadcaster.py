from socket import *
from StoppableThread import StoppableThread
import threading
import time

BROADCAST_INTERVAL = 2

class Broadcaster(StoppableThread):
	"""Broadcast in the local network to be known by the other clients"""
	def __init__(self, sender):
		print "Broadcaster Thread initalizing"
		StoppableThread.__init__(self)
		self.sender = sender


	def run(self):
		while not self.isStopped():
			time.sleep(BROADCAST_INTERVAL)
			# print "Sending broadcast message"
			self.sender.ping()
		self.sender.end()
		exit(1)
		