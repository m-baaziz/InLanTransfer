from StoppableThread import StoppableThread
import threading
from socket import *
from select import select

READ_SOCKET_TIMEOUT = 3

DATAGRAM_NAME_POS = 0
DATAGRAM_ACTION_POS = 1

class Listener(StoppableThread):

	def __init__(self, ip, port, users):
		print "Listener Thread initalizing"
		StoppableThread.__init__(self)
		self.ip = ip
		self.port = port
		self.users = users

	def run(self):
		so = socket(AF_INET, SOCK_DGRAM)
		so.setblocking(0)
		try:
			so.bind((self.ip, self.port))
		except Exception as e:
			print "Binding error (address already in use ?)"
		else:
			print "Listening on " + self.ip + " ... "
			while 1 and not self.isStopped():
				ready = select([so], [], [], READ_SOCKET_TIMEOUT)
				if ready[0]:
					msg = so.recvfrom(50)
					data = msg[0].split(':')
					name = data[DATAGRAM_NAME_POS]
					action = data[DATAGRAM_ACTION_POS]
					ip = msg[1][0]
					print name + " : " + action
					if not self.isStopped():
						if action == "PING":
							self.users.add((name, ip))
						elif action == "END":
							self.users.remove((name, ip))
						elif action == "REQUEST":
							print "Received a Request !!"
		finally:
			print "closing client socket ("+self.ip+")"
			so.close()
			exit(1)