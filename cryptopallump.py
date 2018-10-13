#! /usr/bin/python
"""
Accumulation of useful code from challenges. Some might call it a library.


#https://docs.python.org/3/library/binascii.html
#https://docs.python.org/2/library/binascii.html#binascii.hexlify

#REMEMBER, DON'T GET CONFUSED BETWEEN THE HEX VALUE OF AN ASCII CHARACTER AND THE VALUE OF AN ASCII ENCODED HEX VALUE
#eg: \x49 is an ascii 'I' ; chr(49) = I
#an ascii 4 and 9 are 34 and 39; ord(4) = 34, ord(9) = 39
#AFIK, str (strings) in python 2.7 are literal byte sequences, not limited by ascii values
"""
import binascii, string, itertools, base64
from Crypto.Cipher import AES
from Crypto.Random import random

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

# From http://www.data-compression.com/english.html
freqs = {
    'a': 0.0651738,
    'b': 0.0124248,
    'c': 0.0217339,
    'd': 0.0349835,
    'e': 0.1041442,
    'f': 0.0197881,
    'g': 0.0158610,
    'h': 0.0492888,
    'i': 0.0558094,
    'j': 0.0009033,
    'k': 0.0050529,
    'l': 0.0331490,
    'm': 0.0202124,
    'n': 0.0564513,
    'o': 0.0596302,
    'p': 0.0137645,
    'q': 0.0008606,
    'r': 0.0497563,
    's': 0.0515760,
    't': 0.0729357,
    'u': 0.0225134,
    'v': 0.0082903,
    'w': 0.0171272,
    'x': 0.0013692,
    'y': 0.0145984,
    'z': 0.0007836,
    ' ': 0.1918182
}

def sep(count = 1, stuff = None):
    #Separator, just print some lines
    if stuff:
        stuff = str(stuff)
        if len(stuff) > 1:
            mark = (stuff + ' ')*3
        else:
            mark = stuff * 20
        print mark
    print "\n" * count,

def XORit(a, b):
    #Feed me only byte strings. must be same length
    d = zip(a, b)
    result = ''
    for x, y in d:
        #Convert chr to int for bitwise op, then back to chr. ug.
        result = result + chr(ord(x) ^ ord(y))
    return result

def XORcycle(cipher, key):
    # Feed me only byte strings.
    # Do XOR with a repeating key
    keycycle = itertools.cycle(key)
    d = zip(cipher, keycycle)
    result = ''
    for x, y in d:
        # Convert chr to int for bitwise op, then back to chr. ug.
        result = result + chr(ord(x) ^ ord(y))
    return result

def scoreAscii(target):
    #Check and see if printable ascii
    #return a score...
    #need something better, will prefer gibberish with lots of letters
    score = 0
    for x in target:
        # +1 for being on the acsii table
        if 0 <= ord(x) <= 127:
            score += 1
            #+1 for being printable
            if x in string.printable:
                score += 1
                #+2 for being a letter
                if x in string.letters:
                    score += 2
        else:
            #if it's not in ascii, bail
            return 0
    return score

def scoreAscii2(target):
    score = 0
    for i in target:
        c = i.lower()
        if c in freqs:
            score += freqs[c]
    return score

def histogram(target):
    #Take a string and count occurance of chars
    histo = {}
    for x in target:
        histo[chr(ord(x))] =+ 1

    for x in histo:
        histo[x] = histo[x] / (len(target) * 1.0)
    return histo

def hamdist(bytesS1, bytesS2):
    """
    calculate the hamming distance
    This is the number of differing BITS in a BYTE (not chars in a string)
    Calculate the Hamming distance between two bit strings
    theres probably a better way that blowing a string to an int, then making that a string of 1's and 0's"""

    diff = 0
    for i in range(min(len(bytesS1), len(bytesS2))):
        #force python to keep leading 0's and no 'b'
        sub1 = format(ord(bytesS1[i]), '08b')
        sub2 = format(ord(bytesS2[i]), '08b')
        for x in range(min(len(sub1), len(sub2))):
            if ord(sub1[x]) ^ ord(sub2[x]) != 0:
                diff += 1
    return diff

def getHammingDistance(x, y):
    h =  sum([bin(ord(x[i]) ^ ord(y[i])).count('1') for i in range(len(x))])
    #print h
    return h

def Nhamming(hammwork):
    """
    Return a normalized hamming distance 'score'
    requires an even number of operands in a list
    Avg score of pair by length, then avg set by number of pairs
    """
    hammworki = iter(hammwork)
    scores = [hamdist(x, next(hammworki)) for x in hammworki]
    score = sum(scores) / float(len(scores) * len(hammwork[0]))
    #print scores
    return score

def padpkcs(clear, size):
    #pad a clear text to a necessary size
    #Using rules from https://en.wikipedia.org/wiki/Padding_(cryptography)#PKCS#5_and_PKCS#7
    padlen = size - len(clear)
    return clear + chr(padlen)*padlen

def blockit(xtest, keysize):
    #Chop a string into keysize length
    return [xtest[start:start + keysize] for start in xrange(0, len(xtest), keysize)]

def reblock(blockset):
    #Take a set of blocks and recoalate to new block based on position
    #eg: block of pos 0, block of pos 1
    newblockset = []
    for x in range(len(blockset[0])):
        newblock = ''
        for origblock in blockset:
            try:
                newblock = newblock + origblock[x]
            except:
                pass

        newblockset.append(newblock)
    #print  newblockset
    return newblockset

def brutescore(candidate):
    #Get a string, cycle through chars, then return score
    setlist = {}
    for x in range(0, 256):
        working = XORcycle(candidate, chr(x))
        score = scoreAscii2(working)
        setlist[x] = score
        # get highest score & return
    fff = sorted(setlist, key=setlist.get, reverse=True)
    #return {'score': setlist[fff[0]], 'key': fff[0]}
    return chr(fff[0])

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

def randbytes(count):
    #Return a count length string of random bytes
    rand = ''
    for i in range(count):
        rand += chr(random.randint(0, 255))
    return rand