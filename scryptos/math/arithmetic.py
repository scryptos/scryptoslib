
def gcd(x,y):
  while y: x,y = y,(x%y)
  return x

def egcd(a, b):
    if a == 0:
      return (b, 0, 1)
    else:
      g, y, x = egcd(b % a, a)
      return (g, x - (b // a) * y, y)

def lcm(x,y):
  return (x*y)/gcd(x,y)

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

def nth_root(x,n):
    high = 1
    while high ** n < x:
        high *= 2
    low = high/2
    while low < high:
        mid = (low + high) // 2
        if low < mid and mid**n < x:
            low = mid
        elif high > mid and mid**n > x:
            high = mid
        else:
            return mid
    return mid + 1

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

