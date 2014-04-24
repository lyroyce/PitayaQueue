import ThreadSafe

class GlobalOptions:
	def __init__(self):
		self.aiid = ThreadSafe.AIID(10000)	# ID generator
		self.maxInProgressJobAge = 600		# in seconds, in progress jobs above this age will be requeued
		self.maxDoneJobAge = 600		# in seconds, done jobs above this age will be forgotten
		self.debug = True			# debug flag
	def printOptions(self):
		print 'maxInProgressJobAge = ' + str(self.maxInProgressJobAge)
		print 'maxDoneJobAge       = ' + str(self.maxDoneJobAge)
		print 'debug               = ' + str(self.debug)


