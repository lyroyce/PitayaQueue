PitayaQueue
===========

PitayaQueue is a distributed job queue based on Thrift. 
It contains a job queue server implementation which is written in Python, and a client example in PHP. 

As supported by Thrift, you can use any language you like in the client side to communicate with the job queue server. 
If you don't mind, let's get started with PHP.

Get Started
----------
- Start Server

    Then Run the command below to start the server on current machine. 
    
        # Usage: server.py [port] [maxInProgressJobAge] [maxDonJobAge] [debug]
        $ ./server/server.py 9908 600 600 1

- Add a Worker

    Run the PHP script below to add a worker which handles job when new job comming. Every time you run the script, a new worker is being added. 
      
        $ php example/worker.php
      
    It connects to localhost:9908 by default. Please change it if you need.

- Queue a Job

    Run the PHP script below to queue a job. It exits when the job is done.
    
        $ php example/client.php
      
    It connects to localhost:9908 by default. Please change it if you need.

- Debugging

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

If you are going to use PHP, you may start by modifying `example/client.php` and `example/worker.php`
