from scryptos.math import *
from Crypto.Random import random

def Mersenne(n):
  for x in xrange(2, 65536):
    if n%(2**x-1) == 0:
      return ((2**x-1), n/(2**x-1))
  return None

def Fermat(n):
  x = arithmetic.isqrt(n) + 1
  y = arithmetic.isqrt(x**2-n)
  while True:
    w = x**2 - n - y**2
    if w == 0:
      break
    if w > 0:
      y += 1
    else:
      x += 1
  return (x+y, x-y)

def p_1(n):
  if n%2==0: return 2
  x = random.randint(1, n-1)
  y = x
  c = random.randint(1, n-1)
  g = 1
  while g==1:
    x = ((x*x)%n+c)%n
    y = ((y*y)%n+c)%n
    y = ((y*y)%n+c)%n
    g = arithmetic.gcd(abs(x-y),n)
  return (g, n/g)

def brent(n):
  if n%2==0: return 2
  y,c,m = random.randint(1, n-1),random.randint(1, n-1),random.randint(1, n-1)
  g,r,q = 1,1,1
  while g==1:
    x = y
    for i in range(r):
      y = ((y*y)%n+c)%n
    k = 0
    while k<r and g==1:
      ys = y
      for i in range(min(m,r-k)):
        y = ((y*y)%n+c)%n
        q = q*(abs(x-y))%n
      g = arithmetic.gcd(q,n)
      k = k + m
    r = r*2
  if g==n:
    while True:
      ys = ((ys*ys)%n+c)%n
      g = arithmetic.gcd(abs(x-ys),n)
      if g>1: break
  return (g, n/g)

def rsa_d(rsa, d):
  k = rsa.e * d - 1
  g = 0
  x = 0
  while True:
    g = random.randint(2, rsa.n - 1)
    t = k
    while t % 2 == 0:
      t = t / 2
      x = pow(g, t, rsa.n)

      y = arithmetic.gcd(x - 1, rsa.n)
      if x > 1 and y > 1:
        p = y
        q = rsa.n / y
        return (max(p, q), min(p, q))

