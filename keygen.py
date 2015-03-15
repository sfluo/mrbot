#!/usr/bin/env python
#
# Mr. Bot key generator
#
# Date: Nov. 4, 2012
# All rights are reserved.
# 
import sys, base64
from crypto import slowaes
from crypto import rsa

if __name__ == "__main__":
	(pub, pri) = rsa.newkeys(1024)	
	pripem = pri.save_pkcs1('PEM')
	pubpem = pub.save_pkcs1('PEM')
	print pripem
	print "writing to keys/mrbot.pem ..."
	with open('keys/mrbot.pem', 'wb') as prif:
		prif.write(pripem)
	print pubpem
	print "writing to keys/mrpub.pem ..."
	with open('keys/mrpub.pem', 'wb') as pubf:
		pubf.write(pubpem)
	
