#! /usr/bin/python
"""
Chall 12

Byte-at-a-time ECB decryption (Simple)
Copy your oracle function to a new function that encrypts buffers under ECB mode using a consistent but unknown key (for instance, assign a single random key, once, to a global variable).

Now take that same function and have it append to the plaintext, BEFORE ENCRYPTING, the following string:

Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkg
aGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBq
dXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUg
YnkK
Spoiler alert.
Do not decode this string now. Don't do it.

Base64 decode the string before appending it. Do not base64 decode the string by hand; make your code do it. The point is that you don't know its contents.

What you have now is a function that produces:

AES-128-ECB(your-string || unknown-string, random-key)
It turns out: you can decrypt "unknown-string" with repeated calls to the oracle function!

Here's roughly how:

Feed identical bytes of your-string to the function 1 at a time --- start with 1 byte ("A"), then "AA", then "AAA" and so on. Discover the block size of the cipher. You know it, but do this step anyway.
Detect that the function is using ECB. You already know, but do this step anyways.
Knowing the block size, craft an input block that is exactly 1 byte short (for instance, if the block size is 8 bytes, make "AAAAAAA"). Think about what the oracle function is going to put in that last byte position.
Make a dictionary of every possible last byte by feeding different strings to the oracle; for instance, "AAAAAAAA", "AAAAAAAB", "AAAAAAAC", remembering the first block of each invocation.
Match the output of the one-byte-short input to one of the entries in your dictionary. You've now discovered the first byte of unknown-string.
Repeat for the next byte.

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

stuff = 'Um9sbGluJyBpbiBteSA1LjAKV2l0aCBteSByYWctdG9wIGRvd24gc28gbXkgaGFpciBjYW4gYmxvdwpUaGUgZ2lybGllcyBvbiBzdGFuZGJ5IHdhdmluZyBqdXN0IHRvIHNheSBoaQpEaWQgeW91IHN0b3A/IE5vLCBJIGp1c3QgZHJvdmUgYnkK'

challfile = "ice.txt"
file = open(challfile, 'r')
allit = file.read()

challs = [makefiles(allit) for i in range(10)]

print len(challs)
for x in challs:
    print x['type'], scoreecb(blockit(x['cipher'], 16))