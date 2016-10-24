def rational_to_contfrac(x, y):
  """
  Convert Rational to Continued Fraction
  Args:
    x: numerator
    y: denominator
  Return:
    x/y as Continued Fraction
  """
  pquotients = []
  while x % y != 0:
    a = x // y
    pquotients += [a]
    x, y = y, x - a * y
  pquotients += [x // y]
  return pquotients

def convergents_from_contfrac(frac):    
  """
  Calculate Convergents of a continued fraction
  Args:
    frac: Continued Fraction List
  Return:
    All Convergents of a continued fraction
  """
  convs = [];
  for i in xrange(len(frac)):
      convs.append(contfrac_to_rational(frac[0:i]))
  return convs

def contfrac_to_rational(frac):
  """
  Convert Continued Fraction to Rational
  Args:
    frac: Continued Fraction List
  Return:
    x : numerator
    y : denominator
  """
  if len(frac) == 0:
    return (0, 1)
  num, denom = 1, 0
  frac = frac[::-1]
  while True:
    t = num
    num = frac[0] * num + denom
    denom = t
    if len(frac) == 1:
      break
    frac = frac[1:]
  return (num, denom)
