from StoppableThread import StoppableThread
import threading
from socket import *

DATAGRAM_NAME_POS = 0
DATAGRAM_ACTION_POS = 1

class Listener(StoppableThread):

	def __init__(self, broadcastIp, localIp, port, users):
		print "Listener Thread initalizing"
		StoppableThread.__init__(self)
		self.broadcastIp = broadcastIp
		self.localIp = localIp
		self.port = port
		self.users = users

	def listen(self, ip):
		so = socket(AF_INET, SOCK_DGRAM)
		try:
			so.bind((ip, self.port))
		except Exception as e:
			print "Binding error (address already in use ?)"
		else:
			print "Listening on " + ip + " ... "
			while 1 and not self.isStopped():
				msg = so.recvfrom(50)
				data = msg[0].split(':')
				name = data[DATAGRAM_NAME_POS]
				action = data[DATAGRAM_ACTION_POS]
				ip = msg[1][0]
				print name
				print action
				if action == "PING":
					self.users.add((name, ip))
				elif action == "END":
					self.users.remove((name, ip))
				elif action == "REQUEST":
					print "Received a Request !!"
		finally:
			print "closing client socket"
			so.close()

	def run(self):
		# frist, we duplicate a thread to listen to incoming targeted messages
		th = threading.Thread(target= lambda: self.listen(self.localIp))
		th.deamon = True
		th.start()

		# then we listen to broadcasts
		self.listen(self.broadcastIp)
