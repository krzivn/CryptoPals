#! /usr/bin/python
"""

#https://docs.python.org/3/library/binascii.html
#https://docs.python.org/2/library/binascii.html#binascii.hexlify

"""

from cryptopallump import *
from Crypto.Cipher import AES

challfile = "7.txt"
file = open(challfile, 'r')
allit = file.read()
chall = binascii.a2b_base64(allit)
print challfile

obj2 = AES.new("YELLOW SUBMARINE")
print obj2.decrypt(chall)

