from scryptos.math.arithmetic import *
import gmpy

class FiniteField:
  def __init__(s, v, p):
    if not gmpy.is_prime(p):
      raise Exception("p must be prime")
    s.p = p
    if hasattr(v, "v"):
      s.v = v.v % p
    else:
      s.v = v % p
    if s.v < 0:
      s.v += p

  def __add__(s, o):
    if not hasattr(o, "v"):
      return s + FiniteField(o, s.p)
    return FiniteField(s.v + o.v, s.p)

  def __sub__(s, o):
    if not hasattr(o, "v"):
      return s - FiniteField(o, s.p)
    return FiniteField(s.v - o.v, s.p)

  def __rmul__(s, o):
    return s.__mul__(o)

  def __mul__(s, o):
    if not hasattr(o, "v"):
      return s * FiniteField(o, s.p)
    return FiniteField(s.v * o.v, s.p)

  def __div__(s, o):
    if not hasattr(o, "v"):
      return s / FiniteField(o, s.p)
    return FiniteField(s.v * modinv(o.v, s.p), s.p)

  def __mod__(s, n):
    if n == 0 or s.v == 0:
      return FiniteField(0, s.p)
    return FiniteField(s.v % n, s.p)

  def __rmod__(s, n):
    if n == 0 or s.v == 0:
      return FiniteField(0, s.p)
    return FiniteField(n % s.v, s.p)

  def __pow__(s, x):
    return FiniteField(pow(s.v, x, s.p), s.p)

  def __repr__(s):
    return "FiniteField(%d Mod %d)" % (s.v, s.p)

  def __eq__(s, o):
    if not hasattr(o, "v"):
      return False
    return s.v % s.p == o.v % s.p

  def __ne__(s, o):
    return not s == o
