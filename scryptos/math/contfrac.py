def rational_to_contfrac(x, y):
  pquotients = []
  while x % y != 0:
    a = x // y
    pquotients += [a]
    x, y = y, x - a * y
  pquotients += [x // y]
  return pquotients

def convergents_from_contfrac(frac):    
    convs = [];
    for i in xrange(len(frac)):
        convs.append(contfrac_to_rational(frac[0:i]))
    return convs

def contfrac_to_rational(frac):
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

"""
def rational_to_contfrac_old (x, y):
    a = x//y
    if a * y == x:
        return [a]
    else:
        pquotients = rational_to_contfrac(y, x - a * y)
        pquotients.insert(0, a)
        return pquotients

def contfrac_to_rational_old(frac):
    if len(frac) == 0:
        return (0,1)
    elif len(frac) == 1:
        return (frac[0], 1)
    else:
        remainder = frac[1:len(frac)]
        (num, denom) = contfrac_to_rational(remainder)
        return (frac[0] * num + denom, num)

def convergents_from_contfrac_old(frac):    
    convs = [];
    for i in xrange(len(frac)):
        convs.append(contfrac_to_rational_old(frac[0:i]))
    return convs
"""

if __name__ == "__main__":
  d = rational_to_contfrac(114514, 1919810)
  #d_= rational_to_contfrac_old(114514, 1919810)
  print d
  #print d_
  e = contfrac_to_rational(d)
  #e_= contfrac_to_rational_old(d_)
  print e
  #print e_
  f = convergents_from_contfrac(d)
  #f_= convergents_from_contfrac_old(d_)
  print f
  #print f_
  #print f == f_
