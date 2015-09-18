from scryptos.rsautil import *

a = 2
b = 5
e = 7
n = 9967 * 9973

m = 123456

rsa = RSA(e, n)
c1 = rsa.encrypt(m)
c2 = rsa.encrypt(a*m+b)

m0 = franklin_raiter([rsa, rsa], a, b, [c1, c2])
print m0
assert m0 == 123456
