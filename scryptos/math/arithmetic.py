def gcd(x,y):
  import fractions
  return fractions.gcd(x, y)

def egcd(a, b):
  x, y, u, v = 0, 1, 1, 0
  while a != 0:
    q, r = b // a, b % a
    m, n = x - u * q, y - v * q
    b, a, x, y, u, v = a, r, u, v, m, n
  gcd = b
  return gcd, x, y

def lcm(x,y):
  import gmpy
  return gmpy.lcm(x, y)

def modinv(a, m):
    g, x, y = egcd(a, m)
    if g != 1:
      raise Exception('modular inverse does not exist')
    else:
      return x % m

def chinese_remainder_theorem(items):
  N = reduce(lambda x,y:int(x)*y, [x[1] for x in items])
  result = 0
  for a, n in items:
    m = N/n
    d, r, s = egcd(n, m)
    if d != 1:
      raise Exception("Input not pairwise co-prime")
    result += a*s*m
  return result % N

def generalized_crt(ak, nk):
  """
  ak : Parameter, [a1, a2, ..., ak]
  nk : Parameter, [n1, n2, ..., nk]
  should be len(ak) == len(nk)
  """
  assert len(ak) == len(nk)
  N = reduce(lambda x, y: x * y, nk, 1)
  l = lcm(nk)
  s = 0
  for n, a in zip(nk, ak):
    m = N / n
    g, x, y = egcd(m, n)
    s += (m / g) * x * a
    s %= l
  return s

def nth_root(x,n):
  import gmpy
  return int(gmpy.root(x, n)[0])

def isqrt(n):
  return nth_root(n, 2)

def is_perfect_square(n):
    h = n & 0xF
    if h > 9: return -1
    if not(h == 2 or h == 3 or h == 5 or h == 6 or h == 7 or h == 8):
        t = isqrt(n)
        if t*t == n:
            return t
        else:
            return -1
    return -1

