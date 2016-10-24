import threading
from datetime import datetime
import time
from Tkinter import Frame, BOTTOM, TOP, Button

NAME_POSITION = 0
IP_POSITION = 1
LAST_UPDATE_POSITION = 2
MAX_ALIVE_DELAY = 20

class User:
	def __init__(self, name, ip):
		self._name = name
		self._ip = ip
		self._lastUpdate = datetime.now()

	def name(self):
		return self._name
	def ip(self):
		return self._ip
	def lastUpdate(self):
		return self._lastUpdate

class Users:
	# class containing the conected users array
	def __init__(self, mainFrame, sendRequest):
		self.active = False
		self._users = []
		self.mainFrame = mainFrame
		self.sendRequest = sendRequest
		self.frame = Frame(mainFrame)
		self.frame.pack(side = BOTTOM)
		removeOldUsers = threading.Thread(target=self.removeOldUsers)
		removeOldUsers.daemon = True
		removeOldUsers.start()

	def activate(self):
		self.active = True

	def has(self, user):
		for u in self._users:
			if u.name() == user.name() and u.ip() == user.ip():
				return True
		return False

	def add(self, nameIpTuple):
		user = User(nameIpTuple[0], nameIpTuple[1])
		if not self.has(user):
			self._users.append(user)
		self.updateFrame()

	def remove(self, nameIpTuple):
		users = []
		for user in self._users:
			if not (user.name() == nameIpTuple[NAME_POSITION] and user.ip() == nameIpTuple[IP_POSITION]):
				users.append(user)
		self._users = users
		self.updateFrame()

	def terminate(self):
		self.clear()
		self.active = False

	def clear(self):
		self._users = []
		self.updateFrame()

	# the user list should not contain users who didnt ping for the last $(MAX_ALIVE_DELAY) seconds
	def removeOldUsers(self):
		while self.active:
			time.sleep(MAX_ALIVE_DELAY)
			users = []
			for user in self._users:
				if (not self.has(user)) and abs(time.mktime(user.lastUpdate().timetuple()) - time.mktime(datetime.now().timetuple())) < MAX_ALIVE_DELAY:
					users.append(user)
			self._users = users
			self.updateFrame()

	def __str__(self):
		string = ""
		for user in self._users:
			string += str(user.name()) + " : " + str(user.ip()) + "\n"
		return string

	def __len__(self):
		return len(self._users)

	def updateFrame(self):
		if self.active:
			try:
				for child in self.frame.winfo_children():
					child.destroy()
				if len(self._users) > 0:
					for user in self._users:
						userButton = Button(self.frame, text = user.name(), command= lambda: self.sendRequest(user.ip()))
						userButton.pack(side = BOTTOM)
			except:
				pass