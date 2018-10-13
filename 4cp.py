#! /usr/bin/python
"""
single byte XOR challenge
https://cryptopals.com/sets/1/challenges/3
#https://docs.python.org/3/library/binascii.html
#https://docs.python.org/2/library/binascii.html#binascii.hexlify

"""

from cryptopallump import *

def bigbrute(candidate):
    setlist = {}
    for x in range(0, 255):
        brute = chr(x) * len(candidate)
        #print "bruting with {}".format(x)
        #working = XORit(brute, candidate)
        working = XORcycle(candidate, chr(x))
        score = scoreAscii2(working)
        setlist[x] = score
    #get highest score & return
    fff = sorted(setlist, key=setlist.get, reverse=True)
    return {'score' : setlist[fff[0]], 'key' : fff[0]}


file = "4.txt"
mess = open(file, 'r')

#Build a dictionary of de-hexed strings from the file
shit = {}
for x in mess:
    #print "loading:\n" + x
    #print len(x)
    shit[binascii.a2b_hex(x.strip())] = ''

#print shit

print "Brute forcing list"
for piece in shit:
    shit[piece] = bigbrute(piece)

#print shit
'''
for w in sorted(shit, key=lambda xx: shit[xx]['score'], reverse=True):
  print shit[w]
'''
asdf = sorted(shit, key=lambda xx: shit[xx]['score'], reverse=True)

thisone = 1
print asdf[thisone]
print len(asdf[thisone])
print shit[asdf[thisone]]
print chr(shit[asdf[thisone]]['key'])

brute = chr(shit[asdf[thisone]]['key']) * len(asdf[thisone])
working = XORit(brute, asdf[thisone])
print working

thisone = 0
brute = chr(shit[asdf[thisone]]['key']) * len(asdf[thisone])
working = XORit(brute, asdf[thisone])
print working