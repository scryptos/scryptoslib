from scryptos.rsautil import *

rsa = RSA(7, 17*19)
c = rsa.encrypt(123)
print c

rsa = RSA(7, 17*19, p=17, q=19)
m = rsa.decrypt(c)
print m
assert c == 251
assert m == 123
