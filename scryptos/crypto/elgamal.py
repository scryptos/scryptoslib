from scryptos.math.arithmetic import modinv

class Elgamal:
  def __init__(s, **kwargs):
    if "x" in kwargs.keys():
      s.x = kwargs["x"]
    else:
      s.x = None
    s.p = kwargs["p"]
    s.q = kwargs["q"]
    s.g = kwargs["g"]
    s.h = kwargs["h"]

  def has_private(s):
    return s.x != None

  def encrypt(s, m, r):
    c1 = s.g ** r % s.p
    c2 = m * (s.h ** r) % s.p
    return [c1, c2]

  def decrypt(s, c):
    assert len(c) == 2
    assert s.has_private()
    c1, c2 = c
    m = c2 * modinv(c1 ** s.x, s.p)
    return m % s.p

  def __getitem__(s, k):
    cond = {
        "p": s.p, 
        "q": s.q, 
        "g": s.g, 
        "h": s.h, 
        "x": s.x
    }
    if k in cond.keys():
      return cond[k]

  def __repr__(s):
    return "Elgamal %s Key: (p: %d, q: %d, g: %d, h: %d%s)" % (s.has_private()and"Private"or"Public", s.p, s.q, s.g, s.h, s.has_private()and(", x: %d"%s.x)or"")
