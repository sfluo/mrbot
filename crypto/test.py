#!/usr/bin/env python

import os, random
import rsa,slowaes
import rsa.randnum
import base64
from rsa import pkcs1

if __name__ == "__main__":
	
	# 1. randomly generate a AES key
	#aes_key = rsa.randnum.read_random_bits(128)
	aes_key=[]
	for i in range(0, 16):
		aes_key.append(random.randint(0, 256))
	#aes_key = os.urandom(16)
	print("key: %r" % aes_key)
	
	# 2. Use this key to encrypt message with AES
	moo = slowaes.AESModeOfOperation()
	cleartext = "$SF$1$1379801$13457982#synfd#192.168.1.104#8080$SF$"
	#aes_key = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
	#print("key: %r" % aes_key)
	iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]
	mode, orig_len, ciph = moo.encrypt(cleartext, moo.modeOfOperation["CBC"], aes_key, moo.aes.keySize["SIZE_128"], iv)
	print 'm=%s, ol=%s (%s), ciph=%s' % (mode, orig_len, len(cleartext), ciph)
	decr = moo.decrypt(ciph, orig_len, mode, aes_key, moo.aes.keySize["SIZE_128"], iv)
	print decr

	# 3. Encrypt AES key with RSA

	# 4. Send the encrypted message as well as the encrypted AES key
	
	(pub, priv) = rsa.newkeys(256)

	#message = struct.pack('>IIII', 0, 0, 0, 1)
	#message = "$SF$1$13458792#13457893#ack$SF$"
	message = "hello world"
	print("\tMessage:   %r" % message)
	#message = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
	#bmsg = base64.b64encode(message)
	#print bmsg

	encrypted = rsa.encrypt(message, pub)
	print("\tEncrypted: %r" % encrypted)
	benc = base64.b64encode(encrypted)
	print benc
	print len(encrypted)
	print len(benc)

	decrypted = rsa.decrypt(encrypted, priv)
	print("\tDecrypted: %r" % decrypted)

	msg = "This is test messaget to test the capibility of base64"
	print len(msg)
	bmsg = base64.b64encode(msg)
	print len(bmsg)

	msg = " messaget to test the capibility of base64"
	print len(msg)
	bmsg = base64.b64encode(msg)
	print len(bmsg)


	#assertEqual(message, decrypted)
