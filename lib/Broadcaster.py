from socket import *
import threading
import time
import random
import signal
import sys

BROADCAST_IP = "192.168.0.255"

class Broadcaster(threading.Thread):
	"""Broadcast in the local network to be known by the other clients"""
	def __init__(self, sender):
		print "Broadcaster Thread initalizing"
		threading.Thread.__init__(self)
		self.sender = sender
		signal.signal(signal.SIGINT, self.interruptSignalHandler)

	def interruptSignalHandler(self, signal, frame):
		try:
			self.sender.end()
			sys.exit(0)
		except Exception as e:
			raise

	def run(self):
		random.seed()
		try:
			while 1:
				time.sleep(2)
				print "Sending broadcast message"
				self.sender.ping()
		except Exception as e:
			print e
		finally:
			self.sender.end()
		