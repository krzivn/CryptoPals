#! /usr/bin/python
"""
XOR challenge
https://cryptopals.com/sets/1/challenges/2
#https://docs.python.org/3/library/binascii.html
#https://docs.python.org/2/library/binascii.html#binascii.hexlify

#REMEMBER, DON'T GET CONFUSED BETWEEN THE HEX VALUE OF AN ASCII CHARACTER AND THE VALUE OF AN ASCII ENCODED HEX VALUE
#eg: \x49 is an ascii 'I' ; chr(49) = I
#an ascii 4 and 9 are 34 and 39; ord(4) = 34, ord(9) = 39
#AFIK, str (strings) in python 2.7 are literal byte sequences, not limited by ascii values
"""
import binascii

def sep(count = 1, stuff = None):
    #just print some lines
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

chall  =  "1c0111001f010100061a024b53535009181c"
operand = "686974207468652062756c6c277320657965"
target =  "746865206b696420646f6e277420706c6179"

#convert from hex to byte string
step1 = binascii.a2b_hex(chall)
step2 = binascii.a2b_hex(operand)


sep(0, ">")

result = XORit(step1, step2)
print result
print "Target result :\n{}".format(target)

print binascii.b2a_hex(result)

#this isn't working, right but wrong...
