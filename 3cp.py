#! /usr/bin/python
"""
single byte XOR challenge
https://cryptopals.com/sets/1/challenges/3
#https://docs.python.org/3/library/binascii.html
#https://docs.python.org/2/library/binascii.html#binascii.hexlify

"""

from cryptopallump import *

chall = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"

rawchall = binascii.a2b_hex(chall)

print rawchall
setlist = {}
for x in range(0, 255):
    brute = chr(x) * len(rawchall)
    #print "bruting with {}".format(x)
    working = XORit(brute, rawchall)
    score = scoreAscii2(working)
    setlist[x] = score

#print setlist

'''
for w in sorted(setlist, key=setlist.get, reverse=True):
  print w, setlist[w]
'''

fff = sorted(setlist, key=setlist.get, reverse=True)
brute = chr(fff[0]) * len(rawchall)
print XORit(brute, rawchall)

