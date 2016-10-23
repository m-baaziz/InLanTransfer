from socket import *
from StoppableThread import StoppableThread
import threading
import time
import random
import signal
import sys

class Broadcaster(StoppableThread):
	"""Broadcast in the local network to be known by the other clients"""
	def __init__(self, sender):
		print "Broadcaster Thread initalizing"
		StoppableThread.__init__(self)
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
			while 1 and self.isStopped():
				time.sleep(2)
				print "Sending broadcast message"
				self.sender.ping()
		except Exception as e:
			print e
		finally:
			self.sender.end()
		