import os
import threading
import time
import Queue
import ThreadSafe
from Options import GlobalOptions
from pitaya.ttypes import * 
from pitaya import Pitaya

from thrift.transport import TSocket
from thrift.transport import TTransport
from thrift.protocol import TBinaryProtocol
from thrift.server import TServer

# global variables
g=GlobalOptions()

# entry point
def start(port, maxInProgressJobAge=None, maxDoneJobAge=None, debug=None):
	if maxInProgressJobAge is not None: 	g.maxInProgressJobAge = int(maxInProgressJobAge)
	if maxDoneJobAge is not None: 		g.maxDoneJobAge = int(maxDoneJobAge)
	if debug is not None: 			g.debug = bool(int(debug))
	g.printOptions()

	processor = Processor()
	try:
		transport = TSocket.TServerSocket(port=port)
		tfactory = TTransport.TFramedTransportFactory()
		pfactory = TBinaryProtocol.TBinaryProtocolFactory()
		server = TServer.TThreadPoolServer(Pitaya.Processor(processor), transport, tfactory, pfactory)
		if g.debug: print 'starting server on port '+port+' ...'
		server.serve()
	except KeyboardInterrupt:
		processor.shutdown()
	except Exception as err:
		print str(err)
		processor.shutdown()

# server-side interface implementation
class Processor:
	def __init__(self):
		self.manager = Manager() 
	def queue(self, payload):
		return self.manager.receive(payload) 
	def query(self, jobId):
		return self.manager.query(jobId)
	def take(self, timeout):
		return self.manager.take(timeout)
	def done(self, jobId, result):
		self.manager.done(jobId, result)
	def shutdown(self):
		self.manager.stop()
		os.system("kill "+str(os.getpid()))

# queue manager
class Manager:
	def __init__(self):
		self.alive = True
		self.queue = Queue.Queue() 
		self.jobs = ThreadSafe.Dict()
		self.jobChecker = threading.Thread(target=self.checkJob)
		self.jobChecker.start()
		self.lastDebugInfo = None
	def receive(self, payload):
		job = ServerJob(payload)
		self.jobs.put(job.id, job)
		self.enqueue(job)
		self.debug('Job ' + str(job.id) + ' is queued: ' + job.payload)
		return job
	def enqueue(self, job):
		job.enqueue()
		self.queue.put(job.id)
	def take(self, timeout):
		try:
			jobId = self.queue.get(True, timeout)
			job = self.jobs.get(jobId)
			job.inprogress()
			self.debug('Job ' + str(job.id) +' is taken: '+ job.payload)
			return job
		except Queue.Empty:
			return  NoJob()	
	def done(self, jobId, result):
		job = self.jobs.get(jobId)
		if job and not job.isDone():
			job.done(result)
			self.queue.task_done()
			self.debug('Job ' + str(jobId) + ' is done: ' + job.payload)
		else:
			self.debug('Job ' + str(jobId) + ' not found')
	def query(self, jobId):
		job = self.jobs.get(jobId)
		if job:
			if job.message.status == Status.DONE:
				self.forget(job)
				self.debug('Job ' + str(job.id) + ' is retrieved: ' + job.payload)
			return job.message
		else:
			return Message(Status.NOT_FOUND)
	def forget(self, job):
		self.jobs.delete(job.id)
	def size(self):
		return self.queue.qsize()
	def stop(self):
		self.alive = False
	def checkJob(self):
		while self.alive:
			try:
				self.checkInProgressJob()
				self.checkDoneJob()	
				self.debug()
			finally:
				time.sleep(1)
	def checkInProgressJob(self):
		oldInProgressJobs = (job for job in self.jobs.values() if job.isInProgress() and job.timeSinceInProgress() > g.maxInProgressJobAge)
		for job in oldInProgressJobs:
			self.enqueue(job)
			self.debug('Job ' + str(job.id) + ' is requeued')
	def checkDoneJob(self):
		oldDoneJobs = (job for job in self.jobs.values() if job.isDone() and job.timeSinceDone() > g.maxDoneJobAge)
		for job in oldDoneJobs:
			self.forget(job)	
			self.debug('Job ' + str(job.id) + ' is forgotten')
	def debug(self, message=False):
		if g.debug:
			if message:
				print message
			else:
				map = lambda m: {Status.QUEUED:'=',Status.DONE:'D',Status.IN_PROGRESS:'.'}[m]
				jobs_info = ''.join([map(job.message.status) for job in self.jobs.values()])
				debugInfo = 'Q=' + str(self.size()) + '\t[' + jobs_info + ']'	
				if debugInfo != self.lastDebugInfo:
					self.lastDebugInfo = debugInfo
					print debugInfo

class ServerJob(Job):
	def __init__(self, payload):
		jobId = g.aiid.next()
		Job.__init__(self, jobId, payload)	
		self.message = Message()
	def isInProgress(self):
		return True if self.startTime and not self.endTime else False
	def isDone(self):
		return True if self.endTime else False
	def enqueue(self):
		self.message.status = Status.QUEUED
		self.queueTime = self.time()
		self.startTime = None
		self.endTime = None
	def inprogress(self):
		self.message.status = Status.IN_PROGRESS
		self.startTime = self.time()
	def done(self, result):
		self.message.status = Status.DONE
		self.endTime = self.time()
		self.message.result = result
	def time(self):
        	return int(time.time())
	def timeSinceInProgress(self):
		return self.time()-self.startTime
	def timeSinceDone(self):
		return self.time()-self.endTime

class NoJob(Job):
	pass
	
