from Crypto.PublicKey import RSA as RSA_pycrypto
from Crypto.Cipher import PKCS1_OAEP
from itertools import product
from scryptos.math import arithmetic, contfrac
import random

class RSA:
  def __init__(s, e, n, **kwargs):
    s.e = e
    s.n = n
    if "p" in kwargs.keys():
      s.p = kwargs["p"]
      if "q" in kwargs.keys():
        s.q = kwargs["q"]
      else:
        s.q = s.n / p
      s.d = gen_d(s.e, s.p, s.q)
    elif "d" in kwargs.keys():
      s.d = kwargs["d"]
  def __getitem__(s, n):
    if s.has_private():
      cond = {
          "e":s.e,
          "n":s.n,
          "p":s.p,
          "q":s.q,
          "d":s.d
      }
    else:
      cond = {
          "e":s.e,
          "n":s.n,
      }
    if n in cond.keys():
      return cond[n]
  def decrypt(s, c):
    return pow(c, s.d, s.n)
  def encrypt(s, m):
    return pow(m, s.e, s.n)
  def sign(s, m):
    return pow(m, s.d, s.n)
  def verify(s, sig, m):
    return pow(sig, s.e, s.n) == m
  def has_private(s):
    return hasattr(s, "d")
  def __repr__(s):
    return "RSA %s Key(e=%d, n=%d%s)" % (s.has_private()and"Private"or"Public", s.e, s.n, ", p=%d, q=%d, d=%d" % (s.p, s.q, s.d) if s.has_private() else "")
  def export_pem(s):
    if s.has_private():
      d = RSA_pycrypto.construct((s.n, s.e, s.d, s.p, s.q))
    elif hasattr(s, "d"):
      d = RSA_pycrypto.construct((s.n, s.e, s.d))
    return d.exportKey()

###############################################################################
#                             Helper Functions                                #
###############################################################################
def force_zip(a,b):
  return zip(a + [None] * (max(len(b) - len(a), 0)), b + [None] * (max(len(a) - len(b)), 0))
def bitlength(x):
    assert x >= 0
    n = 0
    while x > 0:
        n = n+1
        x = x>>1
    return n
def totient(*args):
  return reduce(lambda x,y: x*(y-1), map(int, args))
def gen_d(e, p, q):
  l = arithmetic.lcm(p-1, q-1)
  d = arithmetic.egcd(e, l)[1]
  if d < 0:
    d += l
  return d
def decrypt_pkcs1_oaep(ciphertext, rsa):
  key = PKCS1_OAEP.new(RSA_pycrypto.construct((rsa.n, rsa.e, rsa.d, rsa.p, rsa.q)))
  plaintext = key.decrypt(ciphertext.decode("base64"))
  return plaintext

###############################################################################
#                              Core Functions                                 #
###############################################################################
def load_rsa(fname, debug = False):
  rsa = RSA_pycrypto.importKey(open(fname).read())
  if debug:
    print "[+] Successfully Load File: %s" % fname
    if rsa.has_private():
      print "[+] This is Private Key"
      print "[+] p = %d\n[+] q = %d\n[+] d = %d\n" % (rsa.p, rsa.q, rsa.d)
    else:
      print "[+] This is Public Key"
    print "[+] e = %d\n[+] n = %d\n" % (rsa.e, rsa.n)
  if rsa.has_private():
    return RSA(rsa.e, rsa.n, p=rsa.p, q=rsa.q, d=rsa.d)
  else:
    return RSA(rsa.e, rsa.n)
def decrypt_rsa(dataset, cipherset = []):
  e = dataset[0].e
  n = dataset[0].n
  if e == len(dataset) and all([e == x["e"] for x in dataset]):
      print "[+] Hastad Broadcast Attack"
      return hastad_broadcast(dataset, cipherset)
  elif any([x.n == y.n and arithmetic.gcd(x.e, y.e) == 1 for x,y in product(dataset, repeat = 2)]):
    print "[+] Common Modulus Attack"
    return common_modulus(dataset, cipherset)
  elif any([x.e > 65537 ** 2 for x in dataset]):
    print "[-] Wiener's Attack"
    return wiener(dataset, cipherset)
  elif any([not (x == y or arithmetic.gcd(x.n, y.n) == 1) for x,y in product(dataset, repeat=2)]):
    print "[+] Found GCD!"
    for a,b in product(force_zip(dataset, cipherset), repeat=2):
      x = a[0]
      y = b[0]
      if not (x == y or arithmetic.gcd(x.n, y.n) == 1):
        p = arithmetic.gcd(x.n, y.n)
        print "x :",x,"\ny :",y
        print "p1 = p2 = gcd(n1,n2) =",p
        print "q1 =",x.n/p
        print "q2 =",y.n/p
        e = x.e
        n = x.n
        p = p
        q = x.n/p
        c = a[1]
        return RSA(e, n, p=p, q=q).decrypt(c)
        break
  elif any([(d.n%2) == 1 and len(hex(d.n).replace("ff", "")) < (len(hex(d.n)) - 5) for d in dataset]):
    print "[+] Trying Mersenne Prime Factorization..."
    for d,f in force_zip(dataset, cipherset):
      print d
      if (d.n%2) == 1 and len(hex(d.n).replace("ff", "")) < (len(hex(d.n)) - 5):
        n = d.n
        m = fact_mersenne(n)
        if not m == None:
          print "[+] p = %d, q = %d" % m
          return RSA(d.e, n, p=m[0], q=m[1])
    print "[-] Not Mersenne Prime..."
  else:
    print "[*] Unknown"

###############################################################################
#                            Attack Functions                                 #
###############################################################################
def common_modulus(dataset, cipherset):
  for r,s in product(zip(dataset, cipherset), repeat=2):
    x = r[0]
    y = s[0]
    if arithmetic.gcd(x.e, y.e) == 1:
      g, a, b = arithmetic.egcd(x.e, y.e)
      n = x.n
      if a < 0:
        i = arithmetic.modinv(r[1], n)
        return pow(i, -a, n) * pow(s[1], b, n) % n
      elif b < 0:
        i = arithmetic.modinv(s[1], n)
        return pow(r[1], a, n) * pow(i, -b, n) % n
      else:
        return pow(r[1], a, n) * pow(s[1], b, n) % n
  raise ValueError("Invalid Dataset")
def common_private_exponent(dataset):
  # Referenced : http://ijcsi.org/papers/IJCSI-9-2-1-311-314.pdf
  from scryptos.wrapper import fplll
  eset = map(lambda x:x.e, dataset)
  nset = map(lambda x:x.n, dataset)
  r = len(eset)
  M = arithmetic.isqrt(nset[r - 1])
  B = []
  B.append([M] + eset)
  for x in xrange(r):
    B.append([0]*(x+1) + [-nset[x]] + [0]*(r-x-1))
  S = fplll.svp(B) # fplll.lll(B)[0]
  d = abs(S[0])/M
  return d
def hastad_broadcast(dataset, cipherset):
  e = dataset[0].e
  if e == len(dataset) and all([e == x.e for x in dataset]):
    items = []
    for x,y in zip(dataset, cipherset):
      items.append((y, x.n))
    x = arithmetic.chinese_remainder_theorem(items)
    r = arithmetic.nth_root(x,e)
    return r
def wiener(dataset, cipherset):
  import sys
  sys.setrecursionlimit(65537)
  for x,y in zip(dataset, cipherset):
    e = x.e
    n = x.n
    frac = contfrac.rational_to_contfrac(e, n)
    convergents = contfrac.convergents_from_contfrac(frac)
    for (k,d) in convergents:
      if k!=0 and (e*d-1)%k == 0:
        phi = (e*d-1)//k
        s = n - phi + 1
        discr = s*s - 4*n
        if(discr>=0):
          t = arithmetic.is_perfect_square(discr)
          if t!=-1 and (s+t)%2==0:
            print "[+] d = %d" % d
            return pow(y, d, n)
def franklin_raiter(dataset, a, b, cipherset):
  from sympy import Symbol, Poly, FiniteField
  F = FiniteField(dataset[0].n)
  x = Symbol("x")

  g1 = Poly(x**dataset[0].e - cipherset[0], domain=F)
  g2 = Poly(((a*x+b))**dataset[1].e - cipherset[1], domain=F)
  while all(map(lambda x: x != 0, g2.all_coeffs())):
    g1, g2 = g2, g1 % g2
  g = g.monic()
  print "[+] g = %s" % repr(g)

  m = -g.all_coeffs()[-1]
  return m

###############################################################################
#                        Factorization Functions                              #
###############################################################################
def fact_mersenne(n):
  for x in xrange(2, 65536):
    if n%(2**x-1) == 0:
      return ((2**x-1), n/(2**x-1))
  return None
def fact_fermat(n):
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
def fact_p1(n):
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
def fact_brent(n):
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
