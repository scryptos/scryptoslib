from Crypto.PublicKey import RSA as RSA_pycrypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import random
from scryptos.math import arithmetic, contfrac, coppersmith_howgrave
from scryptos.wrapper import *
from scryptos.util    import factor

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
      s.p, s.q = factor.rsa_d(s, s.d)

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
  def decrypt_pkcs1_oaep(s, ciphertext):
    key = PKCS1_OAEP.new(RSA_pycrypto.construct((s.n, s.e, s.d, s.p, s.q)))
    plaintext = key.decrypt(ciphertext.decode("base64"))
    return plaintext
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
  @staticmethod
  def import_pem(fname):
    rsa = RSA_pycrypto.importKey(open(fname).read())
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

def gen_d(e, p, q):
  l = arithmetic.lcm(p-1, q-1)
  d = arithmetic.egcd(e, l)[1]
  if d < 0:
    d += l
  return d

def bitlength(x):
    assert x >= 0
    n = 0
    while x > 0:
        n = n+1
        x = x>>1
    return n
def totient(*args):
  r = 1
  for x in map(int, args):
    r *= x - 1
  return r
def gen_d(e, p, q):
  l = arithmetic.lcm(p-1, q-1)
  d = arithmetic.egcd(e, l)[1]
  if d < 0:
    d += l
  return d

def common_modulus(rsa1, rsa2, c1, c2):
  assert arithmetic.gcd(rsa1.e, rsa2.e) == 1
  assert rsa1.n == rsa2.n
  g, a, b = arithmetic.egcd(rsa1.e, rsa2.e)
  n = rsa1.n
  if a < 0:
    i = arithmetic.modinv(c1, n)
    return pow(i, -a, n) * pow(c2, b, n) % n
  elif b < 0:
    i = arithmetic.modinv(c2, n)
    return pow(c1, a, n) * pow(i, -b, n) % n
  else:
    return pow(c1, a, n) * pow(c2, b, n) % n
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
  assert len(set([x.e for x in dataset])) == 1
  assert len(cipherset) == len(dataset) == dataset[0].e
  e = dataset[0].e
  items = []
  for x,y in zip(dataset, cipherset):
    items.append((y, x.n))
  x = arithmetic.chinese_remainder_theorem(items)
  r = arithmetic.nth_root(x,e)
  return r
def wiener(rsa):
  import sys
  sys.setrecursionlimit(65537)
  e = rsa.e
  n = rsa.n
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
          return RSA(e=e, n=n, d=d)
def franklin_raiter(dataset, a, b, cipherset, impl = "PariGP"):
  if impl == "PariGP":
    expressions = []
    rsa = dataset[0]
    c = cipherset
    expressions.append("g1 = x^%d - %d" % (rsa.e, c[0]))
    expressions.append("g2 = (%d*x+%d)^%d - %d" % (a, b, rsa.e, c[1]))
    expressions.append("g1 = Pol(Vec(g1) * Mod(1, %d))" % rsa.n)
    expressions.append("g2 = Pol(Vec(g2) * Mod(1, %d))" % rsa.n)
    expressions.append("g=gcd(g1,g2)")
    expressions.append("lift(-Vec((Pol(Vec(g)*Vec(g)[1]^-1)))[2])")
    r = eval(parigp(expressions))
    return r
  else:
    from sympy import Symbol, Poly, FiniteField
    F = FiniteField(dataset[0].n)
    x = Symbol("x")

    g1 = Poly(x**dataset[0].e - cipherset[0], domain=F)
    g2 = Poly(((a*x+b))**dataset[1].e - cipherset[1], domain=F)
    while all(map(lambda x: x != 0, g2.all_coeffs())):
      g1, g2 = g2, g1 % g2
    g = g1.monic()
    print "[+] g = %s" % repr(g)

    m = -g.all_coeffs()[-1]
  return m
def high_bit_known(rsa, qbar, out="RSA"):
  diff = coppersmith_howgrave.coppersmith_howgrave_method("x+%d" % (-qbar%rsa.n), rsa.n, 0.5)
  q = qbar - diff
  if out == "RSA":
    return RSA(rsa.e, rsa.n, p=rsa.n/q, q=q)
  elif out == "pq":
    p, q = (rsa.n/q, q)
    return min(p, q), max(p, q)
