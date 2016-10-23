import threading

class StoppableThread(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)
		self._stop = threading.Event()

	def stop(self):
		self._stop.set()

	def isStopped(self):
		return self._stop.isSet()