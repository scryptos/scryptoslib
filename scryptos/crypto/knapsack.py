from scryptos.wrapper import lll
from scryptos.math.arithmetic import modinv

def Decrypt_Merkle_Hellman_Knapsack(c, pub):
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
  return None

def Decrypt_Knapsack_With_Modulo(c, pub, modulo):
  mat = []
  pubkeys = pub + [c]
  for x in xrange(len(pub)):
    mat += [[0] * x + [1] + [0] * (len(pub)-x-1) + [pub[x]]]
  mat += [[0] * (len(pub)) + [modulo]]
  ml = lll(mat)
  # find shortest vector(a.k.a. plaintext)
  for x in ml:
    if x[-1] == 0:
      if x[-2] != -1:
        return [y * modinv(x[-2] % modulo, modulo) % modulo for y in x[:-2]]
      return x[:-2]
  return None
