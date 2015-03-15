#!/usr/bin/env python
# http://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/

#import os
#from Crypto.Cipher import DES3
from Crypto import Random

iv = Random.get_random_bytes(8)
key = Random.get_random_bytes(16)

with open('des3iv.txt', 'w') as f1:
	f1.write(iv)
	#print 'to_enc.txt: %s' % f.read()

with open('des3key.txt', 'w') as f2:
	f2.write(key)


