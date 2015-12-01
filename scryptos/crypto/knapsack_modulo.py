from scryptos.wrapper import lll

def create_matrix_from_knapsack(ciphertext, pubkeys, modulo):
  mat = []
  pubkeys = pubkeys + [ciphertext]
  for x in xrange(len(pubkeys)):
    mat += [[0] * x + [1] + [0] * (len(pubkeys)-x-1) + [pubkeys[x]]]
  mat += [[0] * (len(pubkeys)) + [modulo]]
  return mat

def Decrypt_Knapsack_With_Modulo(c, pub, modulo):
  mat = create_matrix_from_knapsack(c, pub, modulo)
  ml = lll(mat)
  # find shortest vector(a.k.a. plaintext)
  for x in ml:
    if x[-1] == 0:
      return x
  return None

