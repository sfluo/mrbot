#!/usr/bin/env python
#
# Mr.Bot P2P Component
#
# Date: Oct. 26, 2102
# All rights reserved.
#

import socket,sys,time
import SocketServer
import threading,thread
import random
import ccpkt

peerlist={'192.168.1.101:21433':'active', '192.168.1.103:20356':'active'}

class udp_server_handler(SocketServer.BaseRequestHandler):
	'Peer-to-Peer UDP Server handler'
	def handle(self):
		data = self.request[0].strip()
		sock = self.request[1]
		# print "Receiving %s from %s ..." % (data, self.client_address[0])
		msg = ccpkt.get_ack_msg()
		try: 
			sock.settimeout(5)
			sock.sendto(msg, self.client_address)
		except socket.timeout:
			pass
		#sock.close() #FIXME: should I close the socket???

		print "Recv: ", data
		cmd = ccpkt.parsing(data)
		print "Parsing command: ", cmd
		if cmd is 'grp':
			for peer in peerlist.keys():
				print "Contacting ", peer
				if peerlist[peer] is 'active':
					host,port=peer.split(':')
					print "forward to %s:%d " % (host, int(port))
					i = 0
					while i < 3:
						try:
							sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
							sock.settimeout(5)
							sock.sendto(data, (host, int(port))) #FIXME: Should be raw data (encrypted)
							recv = sock.recvfrom(1024)
							sock.close()
						except socket.timeout:
							print "Socket timeout"
							peerlist[peer] = 'dead'
							i += 1
							continue;
						pkt = recv[0].strip()
						cmd = ccpkt.parsing(pkt)
						if cmd == 'ack':
							peerlist[peer] = 'active'
						break

class udp_server(SocketServer.ThreadingMixIn, SocketServer.UDPServer):
	pass

def p2p_init(ip):
	# start udp server
	while True:
		try:
			port = random.randint(1025, 65535)
			print "Try to listening at UDP %d  ..." % port
			server = udp_server((ip, port), udp_server_handler)
			server_thread=threading.Thread(target=server.serve_forever)
			server_thread.daemon=True
			server_thread.start()
			print "Starting listening at %s:%d  ..." % (ip, port)
			break;
		except:
			print "Fail to listen at UDP %d." % port 
	
	# check peer list
	for peer in peerlist.keys():
		i = 0
		host,port=peer.split(':')
		while i < 3:
			try:
				sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
				chmsg = ccpkt.get_checkin_msg(host, int(port))
				sock.settimeout(5)
				sock.sendto(chmsg, (host, int(port)))
				recv = sock.recvfrom(1024)
				sock.close()
			except socket.timeout as te:
				print "Not receive Ack. Make %s dead." % peer
				peerlist[peer]='dead'
				i = i+1
				continue

			pkt = recv[0].strip()
			cmd = ccpkt.parsing(pkt)
			if cmd is 'ack':
				peerlist[peer] = 'active'
			break;
	print peerlist

	while True:
		pass

if __name__ == "__main__":
	p2p_init("192.168.1.104")
