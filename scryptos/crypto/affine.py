from scryptos.math.arithmetic import modinv

class Affine:
  def __init__(s, a, b, m):
    s.a = a % m
    s.b = b % m
    s.m = m

  def encrypt(s, m):
    r = []
    for x in m:
      r += [(s.a*x + s.b) % s.m]
    return r

  def decrypt(s, m):
    r = []
    for x in m:
      r += [(modinv(s.a, s.m) * (x - s.b)) % s.m]
    return r

class Classical_Affine(Affine):
  def __init__(s, a, b):
    Affine.__init__(s, a, b, 26)

  def encrypt(s, m):
    m = s.to_num(m)
    return s.to_alpha(Affine.encrypt(s, m))

  def decrypt(s, m):
    m = s.to_num(m)
    return s.to_alpha(Affine.decrypt(s, m))

  def to_num(s, m):
    return map(lambda x: "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(x), m)

  def to_alpha(s, m):
    return "".join(map(lambda x: "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[x], m))

def KPA(m1, c1, m2, c2, modulo):
  A = (modinv(m1 - m2, modulo) * (c1 - c2)) % modulo
  B = (c1 - m1 * A) % modulo
  return (A, B)

