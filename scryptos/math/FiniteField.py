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

  def __radd__(s, o):
    return s.__add__(o)

  def __add__(s, o):
    if not hasattr(o, "v"):
      return s + FiniteField(o, s.p)
    return FiniteField(s.v + o.v, s.p)

  def __rsub__(s, o):
    return s.__sub__(o)

  def __sub__(s, o):
    if not hasattr(o, "v"):
      return s - FiniteField(o, s.p)
    return FiniteField(s.v - o.v, s.p)

  def __rmul__(s, o):
    if not hasattr(o, "v"):
      return s * FiniteField(o, s.p)
    return FiniteField(s.v * o.v, s.p)

  def __mul__(s, o):
    if not hasattr(o, "v"):
      return s * FiniteField(o, s.p)
    return FiniteField(s.v * o.v, s.p)

  def __div__(s, o):
    if not hasattr(o, "v"):
      return s / FiniteField(o, s.p)
    return FiniteField(s.v * modinv(o.v, s.p), s.p)

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
