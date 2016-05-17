from Crypto.PublicKey import RSA as RSA_pycrypto
from Crypto.Cipher import PKCS1_OAEP
from Crypto.Random import random
from scryptos.math import arithmetic, contfrac, coppersmith_howgrave
from scryptos.wrapper import *
from scryptos.util    import factor, hexutil

class RSA:
  """
  RSA Encryption/Decryption Class
  """
  def __init__(s, e, n, **kwargs):
    """
    Initialization Method

    e : Public Exponent
    n : Public Modulo
    Keyword Arguments: 
      p : Prime 1
      q : Prime 2
      d : Private Exponent

    If e, n, [dpq] is given, auto factoring n and p, q, d is auto set
    so, `RSA(e, n, p=p).q` is OK.
    """
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
    """
    Return RSA parameter

    n : parameter name

    If public key, n is 'e' or 'n'
    In private key, n is 'e', 'n', 'p', 'q' or 'd'
    """
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
    """
    Decrypt RSA Cipher Text

    c : Cipher Text
    """
    return pow(c, s.d, s.n)

  def decrypt_pkcs1_oaep(s, c):
    """
    Decrypt RSA with PKCS#1-OAEP

    c : Cipher Text

    If Invalid PKCS#1-OAEP Message, raise Error.
    In other, return decrypted message
    """
    key = PKCS1_OAEP.new(RSA_pycrypto.construct((s.n, s.e, s.d, s.p, s.q)))
    plaintext = key.decrypt(hexutil.unhex(c))
    return plaintext


  def decrypt_pkcs1(s, c):
    """
    Decrypt RSA with PKCS#1

    c : Cipher Text

    If c is invalid PKCS#1 Ciphertext, Print Error Message and return False
    In other, return decrypted message
    """
    c = s.decrypt(c)
    d = hexutil.unhex(c)
    if d[:2] != "\x00\x02":
      print "[-] Invalid PKCS#1 Data!"
      print "[-] - Invalid Header"
      return False
    i = d.find("\x00", 2)
    if i == -1:
      print "[-] Invalid PKCS#1 Data!"
      print "[-] - Invalid Data"
      return False
    if i < 10:
      print "[-] Invalid PKCS#1 Data!"
      print "[-] - Too Short Padding"
      return False
    return d[i+1:]

  def encrypt(s, m):
    """
    Encrypt Message using RSA

    m ; Message
    """
    return pow(m, s.e, s.n)

  def sign(s, m):
    """
    Sign to message using RSA

    m : Message
    """
    return pow(m, s.d, s.n)

  def verify(s, sig, m):
    """
    Verify signature using RSA

    sig : Signature
    m : Message
    """
    return pow(sig, s.e, s.n) == m

  def has_private(s):
    """
    return `Is this private-key object?`
    """
    return hasattr(s, "d")

  def __str__(s):
    return "RSA %s Key(e=%d, n=%d%s)" % (s.has_private()and"Private"or"Public", s.e, s.n, ", p=%d, q=%d, d=%d" % (s.p, s.q, s.d) if s.has_private() else "")

  def __repr__(s):
    ret = s.__class__.__name__
    ret += "(%d, %d" % (s.e, s.n)
    if s.has_private():
      ret += ", p = %d, q = %d, d = %d" % (s.p, s.q, s.d)
    ret += ")"
    return ret

  def export_pem(s):
    """
    Export to pem string RSA object
    """
    if s.has_private():
      d = RSA_pycrypto.construct((s.n, s.e, s.d, s.p, s.q))
    elif hasattr(s, "d"):
      d = RSA_pycrypto.construct((s.n, s.e, s.d))
    else:
      d = RSA_pycrypto.construct((s.n, s.e))
    return d.exportKey()

  @staticmethod
  def import_pem(pem_string):
    """
    Import PEM string to RSA object

    pem_string : pem as string
    """
    rsa = RSA_pycrypto.importKey(pem_string)
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
  """
  Calculate d from p, q

  p : Prime 1
  q : Prime 2
  """
  l = arithmetic.lcm(p-1, q-1)
  d = arithmetic.egcd(e, l)[1]
  if d < 0:
    d += l
  return d

def bitlength(x):
  """
  Calculate bit length

  x : target integer

  return log2(x)
  """
  return x.bit_length()

def totient(*args):
  """
  Calculate Euler Totient Function

  args : Primes

  \phi(n) = \phi(a) \phi(b) ...
  a, b, ... is prime factor of n

  In this function, totient(a, b, ...)
  """
  r = 1
  for x in map(int, args):
    r *= x - 1
  return r

def common_modulus(rsa1, rsa2, c1, c2):
  """
  Breaking RSA : Common Modulus Attack

  rsa1 : RSA Object 1
  rsa2 : RSA Object 2
  c1 : Cipher Text 1 (encrypted by rsa1)
  c2 : Cipher Text 2 (encrypted by rsa2)

  return m
  """
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

def common_private_exponent(rsa_list):
  """
  Breaking RSA : Common Private Exponent Attack

  rsa_list : public rsa key list has common private exponent

  return d

  Reference : http://ijcsi.org/papers/IJCSI-9-2-1-311-314.pdf

  ===========================================================

  >>> rsa1 = RSA(e1, n1)
  >>> rsa2 = RSA(e2, d2)
  ...
  >>> d = rsautil.common_private_exponent([rsa1, rsa2, ...])
  >>> rsa_1 = RSA(e1, n1, d)
  >>> rsa_2 = RSA(e2, n2, d)
  ...

  """
  from scryptos.wrapper import fplll
  eset = map(lambda x:x.e, dataset)
  nset = map(lambda x:x.n, dataset)
  r = len(eset)
  M = arithmetic.isqrt(nset[r - 1])
  B = []
  B.append([M] + eset)
  for x in xrange(r):
    B.append([0]*(x+1) + [-nset[x]] + [0]*(r-x-1))
  S = fplll.svp(B)
  d = abs(S[0])/M
  return d

def hastad_broadcast(dataset, cipherset):
  """
  Breaking RSA : Hastad's Broadcast Attack

  dataset : RSA Object List can this attack
  cipherset : Cipher Text List , corresponding to dataset
              cipherset[n] <=> dataset[n]
  return m

  =======================================================
  However, this method onlu supported CRT Attack.
  Lattice attack is not support(in future...?)
  """
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
  """
  Breaking RSA : Wiener Attack

  rsa : RSA Obect can this attack

  return private key corresponding to RSA

  =======================================
  If d < 1/3 * N^(1/4), get d from (e, N).
  """
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

def franklin_raiter(rsa, a, b, cipherset, impl = "PariGP"):
  """
  Breaking RSA : Franklin-Reiter Related Message Attack

  rsa : RSA Object ( only public key )
  a,b : parameter of c2 = m * a + b.
  cipherset : Cipher Text List, only 2 elements
  impl : support "PariGP" or "SymPy". (in future, Groebner basis?)
  ================================================================
  see "Low-Exponent RSA with Related Messages" - https://www.cs.unc.edu/~reiter/papers/1996/Eurocrypt.pdf
  """
  if impl == "PariGP":
    expressions = []
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

    g1 = Poly(x**rsa.e - cipherset[0], domain=F)
    g2 = Poly(((a*x+b))**rsa.e - cipherset[1], domain=F)
    while all(map(lambda x: x != 0, g2.all_coeffs())):
      g1, g2 = g2, g1 % g2
    g = g1.monic()
    print "[+] g = %s" % repr(g)

    m = -g.all_coeffs()[-1]
  return m

def high_bit_known(rsa, qbar, out="RSA"):
  """
  Breaking RSA : High-bit Known Attack 

  rsa : RSA Object
  qbar : qbar = q + some_constant, |q-qbar| < N^(1/4).
  out : "RSA" or "pq".

  return : In out == "RSA", RSA Object.
  In out == "pq", return tuple (p, q)
  """
  diff = coppersmith_howgrave.coppersmith_howgrave_method("x+%d" % (-qbar%rsa.n), rsa.n, 0.5)
  q = qbar - diff
  if out == "RSA":
    return RSA(rsa.e, rsa.n, p=rsa.n/q, q=q)
  elif out == "pq":
    p, q = (rsa.n/q, q)
    return min(p, q), max(p, q)
