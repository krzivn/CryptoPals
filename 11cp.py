#! /usr/bin/python
"""
Chall 11

An ECB/CBC detection oracle
Now that you have ECB and CBC working:

Write a function to generate a random AES key; that's just 16 random bytes.

Write a function that encrypts data under an unknown key --- that is, a function that generates a random key and encrypts under it.

The function should look like:

encryption_oracle(your-input)
=> [MEANINGLESS JIBBER JABBER]
Under the hood, have the function append 5-10 bytes (count chosen randomly) before the plaintext and 5-10 bytes after the plaintext.

Now, have the function choose to encrypt under ECB 1/2 the time, and under CBC the other half (just use random IVs each time for CBC). Use rand(2) to decide which to use.

Detect the block cipher mode the function is using each time. You should end up with a piece of code that, pointed at a block box that might be encrypting ECB or CBC, tells you which one is happening.

#https://docs.python.org/3/library/binascii.html
#https://docs.python.org/2/library/binascii.html#binascii.hexlify

"""

from cryptopallump import *
from Crypto.Cipher import AES
from Crypto.Random import random

def randbytes(count):
    #Return a count length string of random bytes
    rand = ''
    for i in range(count):
        rand += chr(random.randint(0, 255))
    return rand

def ecbrandom(cleartext):
    ecb = AES.new(randbytes(16))
    pad = randbytes(random.randint(5, 10))
    #ecb need 16 byte blocks, figure our needed padding to hit that
    padded = padpkcs(cleartext, len(cleartext) + 16 - len(pad + cleartext + pad)%16)
    scramble = pad + padded + pad
    ciphertext = ecb.encrypt(scramble)
    return ciphertext

def cbcrandom(cleartext):
    cbc = CBC(AES.new(randbytes(16), AES.MODE_ECB), randbytes(16))
    pad = randbytes(random.randint(5, 10))
    scramble = pad + cleartext + pad
    ciphertext = cbc.encrypt(scramble)
    return ciphertext

def makefiles(cleartext):
    if random.randint(0, 1) == 1:
        return {'type' : 'cbc', 'cipher':(cbcrandom(cleartext))}
    else:
        return {'type': 'ecb', 'cipher': (ecbrandom(cleartext))}

challfile = "ice.txt"
file = open(challfile, 'r')
allit = file.read()

challs = [makefiles(allit) for i in range(10)]

print len(challs)
for x in challs:
    print x['type'], scoreecb(blockit(x['cipher'], 16))
