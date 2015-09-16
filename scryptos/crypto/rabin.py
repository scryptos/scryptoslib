from scryptos.math.arithmetic import nth_root, modinv, chinese_remainder_theorem

class Rabin:
  def __init__(s, **kwargs):
    if "p" in kwargs.keys():
      s.p = kwargs["p"]
      s.q = kwargs["q"]
    else:
      s.p = None
      s.q = None
    s.n = kwargs["n"]
    s.b = kwargs["b"]

  def has_private(s):
    return s.p != None and s.q != None

  def encrypt(s, m):
    return m * (m + s.b) % s.n

  def decrypt(s, c):
    mp = nth_root((c + (s.b**2 * modinv(4, s.p))) ** (s.p + 1), 4) - (s.b * modinv(2, s.p)) % s.p
    mq = nth_root((c + (s.b**2 * modinv(4, s.q))) ** (s.q + 1), 4) - (s.b * modinv(2, s.q)) % s.q
    m1 = chinese_remainder_theorem([[mp, s.p], [mq, s.q]])
    m2 = chinese_remainder_theorem([[-mp-s.b % s.p, s.p], [mq, s.q]])
    m3 = chinese_remainder_theorem([[mp, s.p], [-mq-s.b % s.q, s.q]])
    m4 = chinese_remainder_theorem([[-mp-s.b % s.p, s.p], [-mq-s.b % s.q, s.q]])
    return (m1, m2, m3, m4)

  def __getitem__(s, k):
    cond = {
        "p": s.p, 
        "q": s.q, 
        "n": s.n, 
        "b": s.b
    }
    if k in cond.keys():
      return cond[k]

  def __repr__(s):
    return "Rabin %s Key: (n: %d%s)" % (s.has_private()and"Private"or"Public", s.n, s.has_private()and(", p: %d, q: %d"%(s.p, s.q))or"")

