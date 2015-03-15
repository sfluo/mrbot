#!/bin/usr/env python
#
# Mr. Bot: data encryption
#
# Date: Nov. 4, 2012
# All rights are reserved.
# 

import sys, random, time, base64
import getopt
from array import array
from crypto import slowaes
from crypto import rsa

def _decrypt(data, pri):
	""" Decrypt the encrypted data collected and sent from bot

		Two blocks: len + enc(keyinfo) + sym_enc(data)
		format:
			0-3	len 
			4 	sym key type
			5-	key info 
	"""
	#msg = base64.b64decode(data)
	msg = data
	if len(msg) < 4:
		return

	try:
		keyinfo_len = int(msg[0:4])
	except ValueError:
		print("Error: Invalide data")
		return

	keyinfo_enc = msg[4:4+keyinfo_len]
	keyinfo = rsa.decrypt(keyinfo_enc, pri)
	cipher = array('B', msg[4+keyinfo_len:])
	alg = keyinfo[0]
	if alg.upper() != 'A':
		print "We only support AES currently."
		return

	try:
		mode = int(keyinfo[1:3])
		aes_len = int(keyinfo[3:7])
		print "aes_len=", aes_len
		aes_key_str = keyinfo[7:aes_len+7]
		iv_len = int(keyinfo[aes_len+7:aes_len+7+4])
		iv_str = keyinfo[7+aes_len+4:7+aes_len+4+iv_len]
		orig_len = int(keyinfo[-4:])
		print "alg=", alg, "mode=", mode, "aes_len=", aes_len, " iv_len=", iv_len, " orig=", orig_len
	except ValueError:
		print("Unable to parse keyinfo segment, quit.")
		return

	moo = slowaes.AESModeOfOperation()
	aes_key = array('B', aes_key_str)
	iv = array('B', iv_str)	
	#print aes_key, iv
	decr = moo.decrypt(cipher, orig_len, mode, aes_key, moo.aes.keySize["SIZE_256"], iv)
	return decr

def _encrypt(data, pub):
	""" Encrypt data collected by bot

		Two blocks: len + enc(keyinfo) + sym_enc(data)
		format:
			0-3	len 
			4 	sym key type
			5-	key info 
	"""
	# 0. TODO: zip the file

	# 1. generate 256-bit AES key and IV
	aes_key_str = rsa.randnum.read_random_bits(256)
	iv_str = rsa.randnum.read_random_bits(256)
	aes_key = array('B', aes_key_str)
	iv = array('B', iv_str)

	# 2. encrypt data with generated AES/IV, and encode the cipher text by Base64
	moo = slowaes.AESModeOfOperation()
	mode, orig_len, cipher = moo.encrypt(data, moo.modeOfOperation["CBC"], aes_key, moo.aes.keySize["SIZE_256"], iv)
	print aes_key, iv, orig_len
	#print("Raw_msg AES_mode=%d, len=%d" % (mode, orig_len))

	# 3. encrypt keyinfo(AES/IV) with public key, and encode it together with ciphertext by Base64
	keyinfo = ''.join(('A', str(mode).zfill(2), str(len(aes_key_str)).zfill(4), aes_key_str, str(len(iv_str)).zfill(4), iv_str, str(orig_len).zfill(4)))
	key_enc = rsa.encrypt(keyinfo, pub)
	
	# 4. return the result
	msg = str(len(key_enc)).zfill(4) + key_enc + str(bytearray(cipher))
	#b64msg = base64.b64encode(msg)
	return msg

def encode(rawfile, keyfile):

	print("Encrypt file with AES key and protect with public key ...")
	try:
		with open(keyfile, 'rb') as f:
			pub = rsa.PublicKey.load_pkcs1(f.read(), "PEM")
	except IOError, ValueError:
		print("Error: fail to read key file %s." % keyfile)
		return

	try:
		with open(datafile, 'rb') as fin:
			encrypted = _encrypt(fin.read(), pub)

		with open(datafile + '.enc', 'wb') as fout:
			fout.write(encrypted)
	except IOError:
		print("Error: fail to write %s encrypted and saved to file. " % datafile)
		if encrypted is not NULL:
			print encrypted
	
def decode(encfile, keyfile):
	print("Decrypt the encrypted file with private key ...")
	try:
		with open(keyfile, 'rb') as f:
			pri = rsa.PrivateKey.load_pkcs1(f.read(), "PEM")
	except IOError, ValueError:
		print("Error: fail to read key file %s." % keyfile)
		return

	try:
		with open(datafile, 'rb') as fin:
			decrypted = _decrypt(fin.read(), pri)
		with open(datafile + '.dec', 'wb') as fout:
			fout.write(decrypted)
	except IOError:
		print("Error: fail to write %s encrypted and saved to file. " % datafile)
		if encrypted is not NULL:
			print decrypted
	
def usage():
	print("Usage: %s [option] <file>" % sys.argv[0])
	print("	-d,--decode	Decode the file")
	print("	-e,--encode	Encode the file")
	print("	-k,--keyfile key file")
	
if __name__ == "__main__":
	try:
		opts, args = getopt.getopt(sys.argv[1:], "d:e:k:i", ["decode", "encode", "keyfile", "input"])
	except getopt.getGetoptError as err:
		print str(err)
		usage()
		sys.exit(2)

	print opts, args

	datafile=None
	keyfile=None
	_proc=None

	for o, a in opts:
		print o, a
		if o in ("-d", "--decode"):
			datafile = a
			_proc=decode
		elif o in ("-e", "--encode"):
			datafile = a
			_proc=encode
		elif o in ("-k", "--keyfile"):
			keyfile = a
		else:
			print("Unhandled options ", o)
	
	if keyfile is None or datafile is None:
		usage()
		sys.exit(2)

	_proc(datafile, keyfile)
			
