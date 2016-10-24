def merkle_hellman_low_density_LO(c, pub):
  """
  Attack to Merkle-Hellman Knapsack Cipher: Low-Density Attack using Lagarias-Odlyzko Algorithm
  Args:
    c   : Ciphertext
    pub : Public key list
  Return: Plaintext
  """
  from scryptos.wrapper import lll
  mat = []
  for x in xrange(len(pub)):
    mat += [[0] * x + [2] + [0] * (len(pub)-x-1) + [pub[x]]]
  mat += [[1] * (len(pub)) + [c]]
  ml = lll(mat)
  # find shortest vector(a.k.a. plaintext)
  for x in ml:
    if all([r == 0 or r == 1 or r == -1 for r in x]):
      # found!
      ret = ""
      for y in x:
        if y == 1:
          ret += "0"
        elif y == -1:
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
  from scryptos.wrapper import lll
  from scryptos.math import isqrt
  n = len(pub)
  L = isqrt(n) + 1
  mat = []
  for x in xrange(n):
    mat += [[0] * x + [1] + [0] * (len(pub)-x-1) + [-L*pub[x]]]
  #mat += [[-0.5] * (len(pub)) + [L*c]]
  mat += [[-1] * (len(pub)) + [L*c]]
  ml = lll(mat)
  # find shortest vector(a.k.a. plaintext)
  for x in ml:
    if x[-1] != 0:
      continue
    x = x[:-1]
    if all([r == 0 or r == 1 or r == -1 for r in x]):
      # found!
      ret = ""
      for y in x:
        ret += str(y + 1)
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
  from scryptos.wrapper import lll
  from scryptos.math import modinv
  import random
  mat = []
  pub = pub + [c]
  for x in xrange(len(pub)):
    mat += [[0] * x + [1] + [0] * (len(pub)-x-1) + [pub[x]]]
  mat += [[0] * (len(pub)) + [modulo]]
  ml = lll(mat)
  # find shortest vector(a.k.a. plaintext)
  for x in ml:
    if x[-1] == 0:
      if x[-2] != -1:
        if x[-2] == 1:
          return [(y * modinv(-1, modulo)) % modulo for y in x[:-2]]
        return [(y * modinv(x[-2], modulo)) % modulo for y in x[:-2]]
      else:
        return x[:-2]

