#! /usr/bin/python
"""
Chall 10

Implement CBC mode
CBC mode is a block cipher mode that allows us to encrypt irregularly-sized messages, despite the fact that a block cipher natively only transforms individual blocks.

In CBC mode, each ciphertext block is added to the next plaintext block before the next call to the cipher core.

The first plaintext block, which has no associated previous ciphertext block, is added to a "fake 0th ciphertext block"
called the initialization vector, or IV.

Implement CBC mode by hand by taking the ECB function you wrote earlier, making it encrypt instead of decrypt
(verify this by decrypting whatever you encrypt to test), and using your XOR function from the previous exercise to combine them.

The file here is intelligible (somewhat) when CBC decrypted against "YELLOW SUBMARINE" with an IV of all ASCII 0 (\x00\x00\x00 &c)

Don't cheat.
Do not use OpenSSL's CBC code to do CBC mode, even to verify your results. What's the point of even doing this stuff if you aren't going to learn from it?

#https://docs.python.org/3/library/binascii.html
#https://docs.python.org/2/library/binascii.html#binascii.hexlify

"""

from cryptopallump import *
from Crypto.Cipher import AES

class CBC:
    def __init__(self, ECB, IV):
        #This first line creates an aes object, like obj2 from before in chall 7
        self._ECB = ECB
        #Initialization vector required for cyclical block cipher...
        self._IV = IV
        self._blocksize = 16

    def _getBlocks(self, data):
        return blockit(data, self._blocksize)

    def encrypt(self, plaintext):
        plainblocks = self._getBlocks(plaintext)
        ciphertext = ''
        prev = self._IV
        for block in range(len(plainblocks)):
            #In CBC we XOR previous block with current, then ECB encrypt
            if len(plainblocks[block]) < self._blocksize:
                plainblocks[block] = padpkcs(plainblocks[block], self._blocksize)
            cipherblock = self._ECB.encrypt(XORit(prev, plainblocks[block]))
            ciphertext += cipherblock
            prev = cipherblock
        return ciphertext

    def decrypt(self, ciphertext):
        cipherblocks = self._getBlocks(ciphertext)
        plaintext = ''
        prev = self._IV
        for cipherblock in cipherblocks:
            plainblock = XORit(self._ECB.decrypt(cipherblock), prev)
            plaintext += plainblock
            prev = cipherblock
        return plaintext

key = "YELLOW SUBMARINE"
cipher = CBC(AES.new(key, AES.MODE_ECB), chr(0) * 16)

challfile = "10.txt"
file = open(challfile, 'r')
allit = file.read()
chall = binascii.a2b_base64(allit)
print challfile

print cipher.decrypt(chall)


