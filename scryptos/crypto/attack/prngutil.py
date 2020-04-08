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
  assert len(random_bits) == mt19937.N
  mt = mt19937(state=list(map(mt19937.untempering, random_bits)))
  return mt

def crack_mt19937_using_index_difference(mA, mB, idxA, idxB):
  """
  Attack to MT19937 : Guess initial state and seed cracking
  Args:
    mA   : A generated random value 1
    mB   : A generated random value 2
    idxA : An index of `mA`
    idxB : An index of `mB`
  Return: Seed Candidates
  See: Scrapbox [Mersenne Twister]
  """
  from scryptos.math import modinv
  from scryptos.crypto import mt19937
  assert (idxA + 397) % 624 == idxB
  # untempering
  mA_ = mt19937.untempering(mA)
  mB_ = mt19937.untempering(mB)
  res = []
  y_ = (mA_ ^ mB_)
  # Guess LSB
  for lsb in [0, 1]:
    y = y_
    if lsb == 1:
      y ^= mt19937.MATRIX_A
    y = (y << 1) & 0xffffffff
    if lsb == 1:
      y |= 1
    # Guess MSB of mt[idxA] and mt[idxA+1]
    invMult = modinv(0x6c078965, mt19937.MOD)
    for msb_mA in [0, 1]:
      for msb_mC in [0, 1]:
        mC = y ^ (msb_mA << 31) ^ (msb_mC << 31)
        x = mC
        for i in range(idxA + 1, 0, -1):
          x = ((x - i) * invMult) % mt19937.MOD
          x = x ^ (x >> 30)
        res += [x]
  ret = set()
  for seed in res:
    mt = mt19937(seed=seed)
    rand = [mt.next() for _ in range(max(idxA, idxB) + 1)]
    if mA in rand and mB in rand:
      ret.add(seed)
  return sorted(map(int, ret))
