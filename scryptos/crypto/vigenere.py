class Vigenere:
  def __init__(s, key):
    s.k = s.to_num(key)

  def encrypt(s, m):
    m = s.to_num(m)
    r = []
    for x in xrange(len(m)):
      r += [(m[x] + s.k[x % len(s.k)])%26]
    return s.to_alpha(r)

  def decrypt(s, m):
    m = s.to_num(m)
    r = []
    for x in xrange(len(m)):
      r += [(m[x] - s.k[x % len(s.k)])%26]
    return s.to_alpha(r)

  def to_num(s, m):
    return map(lambda x: "ABCDEFGHIJKLMNOPQRSTUVWXYZ".index(x), m)

  def to_alpha(s, m):
    return "".join(map(lambda x: "ABCDEFGHIJKLMNOPQRSTUVWXYZ"[x], m))
