import threading
class AIID:
	def __init__(self, start=0):
		self.lock = threading.Lock()
		self.next_id = start
	def next(self):
		self.lock.acquire()
		id = self.next_id
		self.next_id = self.next_id + 1
		self.lock.release()
		return id
