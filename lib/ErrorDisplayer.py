import time
import threading

ERROR_LIFE_TIME = 5

class ErrorDisplayer:
	def __init__(self, error):
		self.error = error

	def set(self, error):
		self.error.set(error)
		th = threading.Thread(target=self.clear)
		th.daemon = True
		th.start()

	def clear(self):
		time.sleep(ERROR_LIFE_TIME)
		self.error.set('')