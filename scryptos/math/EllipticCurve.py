from scryptos.math.FiniteField import FiniteField
from scryptos.math.arithmetic import *
import sys
sys.setrecursionlimit(65537)

class EllipticCurve:
  def __init__(s, a, b, p, ring=FiniteField):
    s.ring = ring
    s.p = p
    s.a = ring(a, p)
    s.b = ring(b, p)
    if s.determinant() == 0:
      raise Exception("Invalid params of a, b(not smooth!)")

  def isoncurve(s, x, y):
    return s.ring(x**3 + s.a * x + s.b, s.p) == s.ring(y**2, s.p)

  def determinant(s):
    return s.ring(-16*(4 * s.a**3 + 27 * s.b**2), s.p)

  def Add(s, P, Q):
    if P.infinity():
      P, Q = Q, P
    if Q.infinity():
      return P

    if P == Q:
      l = (3 * P.x**2 + s.a) * modinv(2 * P.y.v, s.p)
    else:
      l = (Q.y - P.y) * modinv((Q.x - P.x).v, s.p)

    l = s.ring(l, s.p)
    Rx = l**2 - P.x - Q.x
    Ry = l*(P.x - Rx) - P.y
    return ECPoint(s, Rx, Ry)

  def Negate(s, P):
    if P.infinity(): return ECPoint(s, 0, 0)
    else: return ECPoint(s, P.x, -P.y)

  def __repr__(s):
    return "Elliptic Curve y^2 = x^3 + %dx + %d on %s" % (s.a.v, s.b.v, s.ring)
class EdwardsCurve:
  def __init__(s, c, d, p, ring=FiniteField):
    s.ring = ring
    s.p = p
    s.c = ring(c, p)
    s.d = ring(d, p)
    if s.determinant() == 0:
      raise Exception("Invalid params of a, b(not smooth!)")

  def determinant(s):
    return s.ring(s.c*s.d * (1 - s.c**4 * s.d), s.p).v

  def isoncurve(s, x, y):
    return s.ring(x**2+y**2, s.p) == s.ring((s.c ** 2) * (1 + s.d*x**2 * y**2), s.p)

  def Add(s, P, Q):
    if P.infinity():
      P, Q = Q, P
    if Q.infinity():
      return P

    Rx = (P.x * Q.y + P.y * Q.x) * modinv((1 + s.d * P.x * Q.x * P.y * Q.y).v, s.p)
    Ry = (P.y * Q.y - P.x * Q.x) * modinv((1 - s.d * P.x * Q.x * P.y * Q.y).v, s.p)
    return ECPoint(s, Rx, Ry)

  def Negate(s, P):
    if P.infinity(): return ECPoint(s, 0, 0)
    else: return ECPoint(s, P.x, -P.y)

  def __repr__(s):
    return "Edwards Curve x^2+y^2 = %d(1+%dx^2y^2) on %s" % (s.c.v, s.d.v, s.ring)

class ECPoint:
  def __init__(s, curve, x, y):
    s.c = curve
    s.ring = s.c.ring
    s.p = s.c.p
    s.x = s.ring(x, s.p)
    s.y = s.ring(y, s.p)
    s.memo = {}
    if not(s.infinity() or s.c.isoncurve(s.x, s.y)):
      raise Exception("(%d, %d) is not curve point!" % (x, y))

  def infinity(s):
    return s.x == s.y == s.ring(0, s.p)

  def __add__(s, o):
    if repr((s.x, s.y, o.x, o.y)) in s.memo.keys():
      return s.memo[repr((s.x, s.y, o.x, o.y))]
    r = s.c.Add(s, o)
    s.memo.update({repr((s.x, s.y, o.x, o.y)): r})
    return r

  def __sub__(s, o):
    return s + -o

  def __neg__(s):
    return s.c.Negate(s)

  def change_ring(s, ring):
    s.ring = ring

  def change_curve(s, curve):
    if not curve.isoncurve(s.x, s.y):
      raise Exception("(%d, %d) is not curve point!" % (x, y))
    s.curve = curve
    s.memo = {}

  def __mul__(s, n):
    if repr((s.x, s.y, n)) in s.memo.keys():
      return s.memo[repr((s.x, s.y, n))]
    P = s
    res = ECPoint(s.c, 0, 0)
    if n < 0:
      n = abs(n)
      P = -P
    while n != 0:
      if n & 1 == 1:
        res += P
      P += P
      n >>= 1
    s.memo.update({repr((s.x, s.y, n)): res})
    return res

  def __rmul__(s, n):
    return s.__mul__(n)

  def __repr__(s):
    return "ECPoint(%s, %s)" % (s.x.v, s.y.v)
