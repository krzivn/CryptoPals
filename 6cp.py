#! /usr/bin/python
"""

#https://docs.python.org/3/library/binascii.html
#https://docs.python.org/2/library/binascii.html#binascii.hexlify

"""

from cryptopallump import *

cfile = "6.txt"
mess = open(cfile, 'r')

allit = mess.read()

sep(2)

#De-64 encode the file
chall = binascii.a2b_base64(allit)

#print normalizedEditDistance(chall, 29)
sep(2)

#Chop chall into various lengths
blocks = [blockit(chall, i) for i in range(2, 41)]
#Generate hamming scores from a sample selection of blocks
scores = [Nhamming(i[:12]) for i in blocks]
#Get the key length with the lowest score
keylen = range(2, 41)[scores.index(min(scores))]
#Reindex the set of blocks
redex = reblock(blockit(chall, keylen))

#print redex

key = [brutescore(i) for i in redex]
key = ''.join(key)
print XORcycle(chall, key)