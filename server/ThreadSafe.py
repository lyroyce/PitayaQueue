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

class Dict:
	def __init__(self):
		self.dict = {}
		self.lock = threading.Lock()

	def put(self, key, value):
		try:
			self.lock.acquire()
			self.dict[key] = value
		finally:
			self.lock.release()

	def get(self, key, default = False):
		try:
			return self.dict[key]
		except KeyError:
			return default

	def has(self, key):
		found = False
		try:
			self.lock.acquire()
			if key in self.dict:
				found = True
		finally:
			self.lock.release()
		return found

	def remove(self, key):
		value = False
		try:
			self.lock.acquire()
			if key in self.dict:
				value = self.dict[key]
				del self.dict[key]
		finally:
			self.lock.release()
		return value

	def delete(self, key):
		try:
			self.lock.acquire()
			if key in self.dict:
				del self.dict[key]
		finally:
			self.lock.release()

	def items(self):
		return self.dict.items()
	def values(self):
		return self.dict.values()

	def keys(self):
		return self.dict.keys()

	def count(self):
		return len(self.dict)

	def clear(self):
		try:
			self.lock.acquire()		
			self.dict = {}
		finally:
			self.lock.release()
