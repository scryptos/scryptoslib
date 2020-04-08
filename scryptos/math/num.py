from functools import reduce
import operator as op
import gmpy

def modinv(a, n):
  """
  Calculate Modular Inverse of a mod n
  Args:
    a : An element of Z/nZ
    n : Modulo
  Return : Modular inverse of a mod n
  """
  return int(gmpy.invert(a, n))

def nth_root(a, n):
  """
  Calculate n-th root of a on Integer
  Args:
    a : An element of Z
    n : root param
  """
  return int(gmpy.root(a, n)[0])

def egcd(x, y):
  """
    Calculate Extended GCD
    Args:
      x : integer
      y : integer
    Return:
      a, b : A Integer satisfy ax + by = gcd(x, y)
      g    : gcd(x, y)
  """
  g, a, b = map(int, gmpy.gcdext(x, y))
  return (a, b, g)

def gcd(*args):
  """
  Calculate GCD
  Args:
    *args : Some Integers
  Return: GCD of *args
  """
  return int(reduce(lambda x,y: gmpy.gcd(x, y), args[1:], args[0]))

def lcm(*args):
  """
  Calculate LCM
  Args:
    *args : Some Integers
  Return: LCM of *args
  """
  g = gcd(*args)
  return int(reduce(lambda x,y: (x*y) // g, args[1:], args[0]))

def legendre_symbol(a, p):
  """
  Calculate Legendre Symbol
  Args:
    a : An element of Z/pZ
    p : A prime
  Return:
    a is quadratic residue : 1
    a is non-quadratic residue : -1
    a is factor of p : 0
  """
  return int(gmpy.legendre(a, p))

def jacobi_symbol(a, n):
  """
  Calculate Jacobi Symbol
  Args:
    a : An element of Z/nZ
    n : A number
  Return:
    a is quadratic residue : 1
    a is non-quadratic residue : -1
    a is factor of n : 0
  """
  return int(gmpy.jacobi(a, n))

def is_prime(x):
  """
  Is prime x?
  Args:
    x : An integer
  Return: Is prime x?
  """
  return gmpy.is_prime(x) > 0

def isqrt(x):
  """
  Calculate sqrt(x) on Z
  Args:
    x : An integer
  Return: sqrt(x)
  """
  return nth_root(x, 2)

def modsqrt(a, m):
  """
  Calculate Modular Square Root of a mod m
  Args:
    a : An element of Z/mZ
    m : A prime
  Return: Modular square root of a mod m
  """
  import random
  def _find_power_divisor(base, x, modulo=None):
    k = 0
    m = base
    while x % m == 0:
      k += 1
      m = pow(m * base, 1, modulo)
    return k
  def _find_power(power_base, x, crib, modulo=None):
    k = 1
    r = power_base
    while pow(x, r, modulo) != crib:
      k += 1
      r *= power_base
    return k
  if is_prime(m):
    # Tonelli-Shanks Algorithm
    if m % 4 == 3:
      r = pow(a, (m + 1) // 4, m)
      return [r, m - r]
    s = _find_power_divisor(2, m - 1)
    q = (m - 1) // 2**s
    z = 0
    while legendre_symbol(z, m) != -1:
      z = random.randint(1, m)
    c = pow(z, q, m)
    r = pow(a, (q + 1) // 2, m)
    t = pow(a, q, m)
    l = s
    while True:
      if t % m == 1:
        return [r, m - r]
      i = _find_power(2, t, 1, m)
      b = pow(c, 2 ** (l - i - 1), m)
      r = (r * b) % m
      t = (t * (b**2)) % m
      c = pow(b, 2, m)
      l = i
  if m == 2:
    return a
  if m % 4 == 3:
    r = pow(a, (m + 1) // 4, m)
    return [r, m - r]
  if m % 8 == 5:
    v = pow(2 * a, (m - 5) // 8, m)
    i = pow(2 * a * v, 2, m)
    r = a * v * (i - 1) % m
    return [r, m - r]
  if m % 8 == 1:
    e = _find_power_divisor(2, m - 1)
    q = (m - 1) // 2**e
    z = 1
    while pow(z, 2**(e - 1), m) == 1:
      x = random.randint(1, m)
      z = pow(x, q, m)
    y = z
    r = e
    x = pow(a, (q - 1) // 2, m)
    v = (a * x) % m
    w = (v * x) % m
    while True:
      if w == 1:
        return [v, m - v]
      k = _find_power(2, w, 1, m)
      d = pow(y, 2**(r - k - 1), m)
      y = pow(d, 2, m)
      r = k
      v = d * v % m
      w = w * y % m

def crt(ak, nk):
  """
  An Implementation of Generalized Chinese Reminder Theorem
  Args:
    ak : Parameter, [a1, a2, ..., ak]
    nk : Parameter, [n1, n2, ..., nk]
  Return:
    Solution of Modular Equation ak = x mod nk
  should be len(ak) == len(nk)
  """
  assert len(ak) == len(nk)
  N = reduce(lambda x, y: x * y, nk, 1)
  l = lcm(*nk)
  s = 0
  for n, a in zip(nk, ak):
    m = N // n
    x, y, g = egcd(m, n)
    s += (m // g) * x * a
    s %= l
  return s

def euler_phi(*primes):
  """
  Calculate Euler Totient-function
  Args:
    *primes: Prime-factored modulo e.g. n = \prod_{p\in *primes} p
  Return: \phi(n)
  """
  res = 1
  for x in list(set(primes)):
    k = primes.count(x)
    res *= x ** k - x ** (k - 1)
  return res

def is_perfect_square(n):
  """
  Is perfect square number?
  Args:
    n : an integer for square test
  Return: is perfect square n?
  """
  h = n & 0xF
  if h > 9 or  h == 2 or h == 3 or h == 5 or h == 6 or h == 7 or h == 8:
    return -1
  t = isqrt(n)
  if t*t == n:
    return t
  else:
    return -1

