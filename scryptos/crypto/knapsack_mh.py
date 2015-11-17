from scryptos.wrapper import lll

def create_matrix_from_knapsack(ciphertext, pubkeys):
  mat = []
  for x in xrange(len(pubkeys)):
    mat += [[0] * x + [2] + [0] * (len(pubkeys)-x-1) + [pubkeys[x]]]
  mat += [[1] * (len(pubkeys)) + [ciphertext]]
  return mat

def Decrypt_Merkle_Hellman_Knapsack(c, pub):
  mat = create_matrix_from_knapsack(c, pub)
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
