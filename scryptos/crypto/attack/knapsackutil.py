def merkle_hellman_low_density_LO(c, pub):
  """
  Attack to Merkle-Hellman Knapsack Cipher: Low-Density Attack using Lagarias-Odlyzko Algorithm
  Args:
    c   : Ciphertext
    pub : Public key list
  Return: Plaintext
  """
  from scryptos.math import LLL
  mat = []
  for x in xrange(len(pub)):
    mat += [[0] * x + [1] + [0] * (len(pub)-x-1) + [pub[x]]]
  mat += [[0] * (len(pub)) + [-c]]
  ml = LLL(mat)
  # find shortest vector(a.k.a. plaintext)
  for x in ml:
    if all([r == 0 or r == 1 for r in x[:len(pub)]]):
      # found!
      ret = ""
      for y in x[:len(pub)]:
        if y == 0:
          ret += "0"
        elif y == 1:
          ret += "1"
      return int(ret, 2)

def merkle_hellman_low_density_CLOS(c, pub):
  """
  Attack to Merkle-Hellman Knapsack Cipher: Low-Density Attack using CLOS Algorithm
  Args:
    c   : Ciphertext
    pub : Public key list
  Return: Plaintext
  """
  from scryptos.math import isqrt, Rational_LLL, vector_norm_i
  n = len(pub)
  L = 2*isqrt(n) + 1
  mat = []
  for x in xrange(n):
    mat += [[0] * x + [1] + [0] * (len(pub)-x-1) + [-L*pub[x]]]

  # -1/2
  mat += [[(-1, 2)] * (len(pub)) + [L*c]]

  # LLL
  ml = Rational_LLL(mat)

  # Convert Rational to Real
  for i in xrange(len(ml)):
    for j in xrange(len(ml[i])):
      if isinstance(ml[i][j], tuple):
        ml[i][j] = ml[i][j][0] * 1.0 / ml[i][j][1]

  # find shortest vector(a.k.a. plaintext)
  # In CLOS Method, vector (x1 - 1/2, x2 - 1/2, ..., xn - 1/2, 0) belongs to Lattice `mat`
  # that vector norm is very small. so, SVP of `mat` is that vector in high probability
  for x in ml:
    if x[-1] != 0:
      continue
    x = map(lambda x: int(x + 0.5), x[:-1])
    if all([r == 0 or r == 1 for r in x]):
      # found!
      ret = ""
      for y in x:
        ret += str(y)
      return int(ret, 2)

def merkle_hellman_modulo(c, pub, modulo):
  """
  Attack to Knapsack Cipher: Lattice Attack with Modulus
  Args:
    c      : Ciphertext
    pub    : Public key list
    modulo : Modulo
  Return: Plaintext
  """
  from scryptos.math import modinv, LLL
  import random
  mat = []
  pub = pub + [c]
  for x in xrange(len(pub)):
    mat += [[0] * x + [1] + [0] * (len(pub)-x-1) + [pub[x]]]
  mat += [[0] * (len(pub)) + [modulo]]
  ml = LLL(mat)
  # find shortest vector(a.k.a. plaintext)
  for x in ml:
    if x[-1] == 0:
      if x[-2] != -1:
        if x[-2] == 1:
          return [(y * modinv(-1, modulo)) % modulo for y in x[:-2]]
        return [(y * modinv(x[-2], modulo)) % modulo for y in x[:-2]]
      else:
        return x[:-2]

