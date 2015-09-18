from scryptos.rsautil import *

rsa1 = RSA(3, 17*19)
rsa2 = RSA(7, 17*19)

c1 = rsa1.encrypt(123)
c2 = rsa2.encrypt(123)

m = common_modulus([rsa1, rsa2], [c1, c2])
print m
assert m == 123
