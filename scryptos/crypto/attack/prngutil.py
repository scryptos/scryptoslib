def crack_lcg(a, b, c, modulo):
  """
  Cracking LCG: from 3 Random integers
  Args:
    a      : random integer 1
    b      : random integer 2
    c      : random integer 3
    modulo : Modulus Parameter
  Return: Tuple of LCG Parameter, as (A, B)
  """
  from scryptos.math import modinv
  A = (((b - c) % modulo) * modinv((a-b) % modulo, modulo)) % modulo
  B = (b - A * a) % modulo
  return (A, B)

def crack_mt19937(random_bits):
  """
  Attack to MT19937 : Known Random-bits
  Args:
    random_bits : A list of 624 random elements
  Return: mt19937 class object
  """
  from scryptos.crypto import mt19937
  assert len(random_bits) == 624
  mt = mt19937(state=map(mt19937.untempering, random_bits))
  return mt
