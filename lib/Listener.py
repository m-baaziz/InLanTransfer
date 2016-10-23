from socket import *
import threading

DATAGRAM_NAME_POS = 0
DATAGRAM_ACTION_POS = 1

class Listener(threading.Thread):

	def __init__(self, broadcastIp, port, users):
		print "Listener Thread initalizing"
		self.broadcastIp = broadcastIp
		self.port = port
		self.users = users
		threading.Thread.__init__(self)

	def run(self):
		so = socket(AF_INET, SOCK_DGRAM)
		try:
			so.bind((self.broadcastIp, self.port))
		except Exception as e:
			print "Binding error (address already in use ?)"
		else:
			print "Listening ... "
			while 1:
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