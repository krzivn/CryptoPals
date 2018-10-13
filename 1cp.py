#! /usr/bin/python
"""
#https://cryptopals.com/sets/1/challenges/1
#https://docs.python.org/3/library/binascii.html
#https://docs.python.org/2/library/binascii.html#binascii.hexlify

#REMEMBER, DON'T GET CONFUSED BETWEEN THE HEX VALUE OF AN ASCII CHARACTER AND THE VALUE OF AN ASCII ENCODED HEX VALUE
#eg: \x49 is an ascii 'I' ; chr(49) = I
#an ascii 4 and 9 are 34 and 39; ord(4) = 34, ord(9) = 39
#AFIK, str (strings) in python 2.7 are literal byte sequences, not limited by ascii values
"""
import binascii

#ascii encode base16 (hex) value
practicehex = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
print "Start value in hex:"
print practicehex

b64 = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
print "Target Base 64 encoded value:"
print b64

print "binascii.unhexlify of start value, turns hex string to ascii"
print binascii.unhexlify(practicehex)

aa = 10
print aa
print bin(aa)
print hex(aa)

#Convert from a string, base 16, to an int
numhex = int(practicehex, 16)
print "Converted value of practice hex as int:"
print numhex
print "from ascii hex, to int, back to hex:"
print hex(numhex)

print binascii.a2b_base64(b64)

#This gets us our 'true' data, not represented by hex
# Calls ascii to binary
step1 = binascii.a2b_hex(practicehex)
print step1
print type(step1)

print binascii.b2a_base64(binascii.a2b_hex(practicehex))

arr = bytearray(binascii.a2b_hex(practicehex))
print arr