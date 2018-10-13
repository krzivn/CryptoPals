#! /usr/bin/python
"""
Detect AES in ECB mode
In this file are a bunch of hex-encoded ciphertexts.

One of them has been encrypted with ECB.

Detect it.

Remember that the problem with ECB is that it is stateless and deterministic; the same 16 byte plaintext
block will always produce the same 16 byte ciphertext.

#https://docs.python.org/3/library/binascii.html
#https://docs.python.org/2/library/binascii.html#binascii.hexlify

"""

from cryptopallump import *
from Crypto.Cipher import AES

challfile = "8.txt"
file = open(challfile, 'r')
allit = file.readlines()
#Turn read data from hex strings into bit values (stripping newline)
chall = [binascii.a2b_hex(i.strip()) for i in allit]

def scoreecb(x):
    #Build a set of unique pairs of elements being passed in
    #Exercise says if the cleartext is repeating, it will repeat every 16 bytes; thats to say the cipher repeats every 16 bytes.
    pairs = itertools.combinations(x, 2)
    same = 0
    count = 0
    for p in pairs:
        if p[0] == p[1]:
            same += 1
    return same

blocks = [blockit(i, 16) for i in chall]

for set in blocks:
    setscore = scoreecb(set)
    if setscore > 0:
        print setscore
        print "Found a repeating blockset on line {} with a score of {}.".format(blocks.index(set)+1, setscore)

