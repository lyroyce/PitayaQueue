PitayaQueue
===========

PitayaQueue is a distributed job queue based on Thrift. 
It contains a job queue server implementation which is written in Python, and a client example in PHP. 

As supported by Thrift, you can use any language you like in the client side to communicate with the job queue server. 
If you don't mind, let's get started with PHP.

Start Server
-----------
Run the command below to start the server on current machine. 

  # Usage: server.py [port] [maxInProgressJobAge] [maxDonJobAge] [debug]
  ./server/server.py 9908 600 600 1
  
Configure Client
-----------
Make sure you have thrift installed, or at least have thrift library for your language available. 
Specifically, to run the example PHP script, you need to modify the example scripts and set `THRIFT_ROOT` global variable.
  
  $GLOBALS['THRIFT_ROOT']='/usr/local/thrift/lib/php/lib';

Add a Worker
-----------
Run the php script below to add a worker which handles job when new job comming. 
It connects to localhost:9908 by default. Please change it if you need.
  
  php example/worker.php
  
Queue a Job
-----------
Run the php script below to queue a job. 
It connects to localhost:9908 by default. Please change it if you need.

  php example/client.php
  
Debug
----------
If you start the server with the debug flag set to non-zero, you would see debug information on server-side as below:
  
  maxInProgressJobAge = 600
  maxDoneJobAge       = 600
  debug               = True
  starting server on port 9908 ...
  Q=0     []
  Job 10000 is received: This is a test job from client
  Q=1     [=]
  Job 10000 is taken: This is a test job from client
  Q=0     [.]
  Job 10000 is done: This is a test job from client
  Q=0     [D]

Implement Your Service...
------------
Ok, the demo is over... Now, it's time to write your own service on top of the job queue.
