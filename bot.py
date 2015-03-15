#!/usr/bin/env python
#
# Mr. Bot 
#
# by Shoufu Luo
# Date: Oct. 26, 2102
# All rights reserved.
#

import socket,sys,time
import center
import peers

def check_internet():
	srvlist = ['www.google.com:80', 'www.yahoo.com:80']
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	for srv in srvlist:
		try:
			srvs = srv.split(':')
			print "Trying %s:%d ..." % (srvs[0], int(srvs[1]))
			sock.connect((srvs[0], int(srvs[1])))
			sockinfo = sock.getsockname()
			sock.close()
			return sockinfo[0]
		except:
			print 'Fail. wait another 30s ...'
			time.sleep(30)
	return 'null'
	

if __name__ == "__main__":

	# check Internet
	while True:
		try:
			ip = check_internet()
			if (ip == 'null'):
				raise 'No Internet!'
			break;
		except 'No Internet!':
			time.sleep(3600)

	print 'Current ip address is: ', ip

	# start peer-to-peer 
	peers.p2p_init(ip)

	# check the centralized server
	print 'We are supposed to periodly check central server for commands'
	while True:
		center.synchronize()
		time.sleep(7200)


