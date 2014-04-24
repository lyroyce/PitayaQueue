#!/usr/bin/python
import sys
import PitayaServer

if len(sys.argv) < 2:
	print 'Usage: server.py [port] [maxInProgressJobAge] [maxDonJobAge] [debug]';
	sys.exit(2)

PitayaServer.start(*sys.argv[1:])

