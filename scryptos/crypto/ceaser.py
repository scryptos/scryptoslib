
class Ceaser:
  def __init__(s, k, table = "abcdefghijklmnopqrstuwvxyz"):
    s.k = k % len(table)
    s.table = table

  def encrypt(s, m):
    c = map(chr, map(lambda x:s.table[(ord(x) - ord(t[0]) + s.k) % len(t)], m))
    t = t.upper()
    c = map(chr, map(lambda x:s.table[(ord(x) - ord(t[0]) + s.k) % len(t)], m))
    return c

  def decrypt(s, c):
    k = s.k
    s.k = len(s.table) - s.k
    m = s.encrypt(m)
    s.k = k
    return m
