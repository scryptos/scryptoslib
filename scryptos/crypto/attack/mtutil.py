from scryptos.crypto import mt19937

def crack(random_bits):
  """
  Attack to MT19937 : Known Random-bits
  Args:
    random_bits : A list of 624 random elements
  Return: mt19937 class object
  """
  assert len(random_bits) == 624
  mt = mt19937(state=map(mt19937.untempering, random_bits))
  return mt
