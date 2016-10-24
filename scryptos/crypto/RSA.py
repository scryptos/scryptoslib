from scryptos.math.num import *
from Crypto.Random import random
from Crypto.PublicKey import RSA as pycrypto_RSA

def rsa_d(rsa, d):
  """
  Factor RSA Public Key using Private Exponent.
  Args:
    rsa : instance of RSA
    d   : Private Exponent
  Return:
    p   : Prime 1 (bigger than `q`)
    q   : Prime 2 (smaller than `p`)
  """
  k = rsa.e * d - 1
  g = 0
  x = 0
  while True:
    g = random.randint(2, rsa.n - 1)
    t = k
    while t % 2 == 0:
      t = t / 2
      x = pow(g, t, rsa.n)
      y = gcd(x - 1, rsa.n)
      if x > 1 and y > 1:
        p = y
        q = rsa.n / y
        return (max(p, q), min(p, q))

class RSA(object):
  """
  RSA Public/Private Key Class
  """
  def __init__(s, e, n, p=None, q=None, d=None):
    """
    Constructor of RSA
    Args:
      e : Public Exponent
      n : Public Modulus s.t. n = p*q
      p : Prime 1
      q : Prime 2
      d : Private Exponent

    If one of `p`, `q` or `d` is appointed, auto generate other (private) parameter.
    """
    s.e = e
    s.n = n
    s.p = p
    s.q = q
    s.d = d
    if s.p is not None or s.q is not None or s.d is not None:
      if s.p is not None and s.q is None:
        s.q = s.n / s.p
        assert s.q * s.p == s.n
      if s.d is not None and s.p is None and s.q is None:
        s.p, s.q = rsa_d(s, s.d)
      if s.d is None and s.p is not None:
        phi = euler_phi(s.p, s.q)
        s.d = modinv(s.e, phi)

  def is_public(s):
    """
    Is Public Key object?

    Return: Is this public key?
    """
    return s.p is None

  def encrypt(s, m):
    """
    RSA Encryption
    Args:
      m : Plaintext Message (must be integer object)
    Return: RSA Encrypted integer (m^e mod n)
    """
    return pow(m, s.e, s.n)

  def decrypt(s, c):
    """
    RSA Decryption
    Args:
      c : Ciphertext (must be integer object)
    Return: RSA Decrypted integer (c^d mod n)
    """
    return pow(c, s.d, s.n)

  def sign(s, m):
    """
    Sign to m using RSA
    Args:
      m : Plaintext Message (must be integer object)
    Return: Signature of `m`
    """
    return s.decrypt(c)

  def verify(s, m, sig):
    """
    Verify Signature using RSA
    Args:
      m   : Plaintext Message (must be integer object)
      sig : Signature of `m`
    Return: If valid signature, then True, else False.

    """
    return s.encrypt(m) == sig

  def __str__(s):
    if s.is_public():
      return "RSA Public Key: e = %s, n = %s" % (s.e, s.n)
    else:
      return "RSA Private Key: e = %s, n = %s, p = %s, q = %s" % (s.e, s.n, s.p, s.q)

  def __repr__(s):
    if s.is_public():
      return "RSA(%r, %r)" % (s.e, s.n)
    else:
      return "RSA(%r, %r, %d, %d, %d)" % (s.e, s.n, s.p, s.q, s.d)

  def to_pem(s):
    if s.is_public():
      rsa = pycrypto_RSA.construct((long(s.n), long(s.e)))
    else:
      rsa = pycrypto_RSA.construct((long(s.n), long(s.e), long(s.d), long(s.p), long(s.q)))
    return rsa.exportKey("PEM")

  @staticmethod
  def import_pem(pem_string):
    d = pycrypto_RSA.importKey(pem_string)
    if d.has_private():
      return RSA(d.e, d.n, d.p, d.q, d.d)
    else:
      return RSA(d.e, d.n)
