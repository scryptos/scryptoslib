from scryptos.math.num import *

class RC4(object):
  """
  RSA Public/Private Key Class
  """
  def __init__(s, key):
    """
    Constructor of RC4
    Args: 
      key : RC4 Key
    """
    s.key = key

  def init_ksa(s):
    import math
    s.table = range(256)
    j = 0
    key = s.key * int(math.ceil(256./len(s.key)))
    for i in xrange(256):
      j = (j + s.table[i] + ord(key[i])) % 256
      s.table[i], s.table[j] = s.table[j], s.table[i]

  def prga(s, length):
    s.init_ksa()
    i, j = 0, 0
    rand = ""
    for _ in xrange(length):
      i = (i + 1) % 256
      j = (j + s.table[i]) % 256
      s.table[i], s.table[j] = s.table[j], s.table[i]
      rand += chr(s.table[(s.table[i] + s.table[j]) % 256])
    return rand


  def encrypt(s, m):
    """
    RC4 Encryption
    Args:
      m : Plaintext Message (must be string object)
    Return: RC4 Encrypted String (c_i = m_i XOR PRGA())
    """
    return "".join([chr(ord(x) ^ ord(y)) for x, y in zip(m, s.prga(len(m)))])

  def decrypt(s, c):
    """
    RC4 Decryption
    Args:
      c : Ciphertext (must be string object)
    Return: RC4 Decrypted String (same as `encrypt`)
    """
    return s.encrypt(c)

  def __str__(s):
    return "RC4 Instance: key = %r" % s.key

  def __repr__(s):
    return "RC4(%r)" % s.key
