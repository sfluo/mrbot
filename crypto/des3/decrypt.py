#!/usr/bin/env python
# http://www.laurentluce.com/posts/python-and-cryptography-with-pycrypto/

import os
from Crypto.Cipher import DES3
from Crypto import Random

def decrypt_file(in_filename, out_filename, chunk_size, key, iv):
	des3 = DES3.new(key, DES3.MODE_CFB, iv)

	with open(in_filename, 'r') as in_file:
		with open(out_filename, 'w') as out_file:
			while True:
				chunk = in_file.read(chunk_size)
				if len(chunk) == 0:
					break;
				out_file.write(des3.decrypt(chunk))


with open('des3iv.txt','r') as iv_file:
	iv = iv_file.read()
with open('des3key.txt', 'r') as key_file:
	key = key_file.read()

with open('cipher.txt', 'r') as f:
	print 'cipher.txt: %s' % f.read()

decrypt_file('cipher.txt', 'plaintext_after_dec.txt', 8192, key, iv)

with open('plaintext_after_dec.txt', 'r') as f:
	print 'plaintext_after_dec.txt: %s' % f.read()
