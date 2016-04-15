class Scytale:
  def __init__(s, k):
    s.k = k
  def encrypt(s, m):
    from scryptos.util.stringutils import transpose, nth_split
    return "".join(transpose(nth_split(m, len(m)/s.k))).replace(" ", "")

  def decrypt(s, m):
    from scryptos.util.stringutils import transpose, nth_split
    return "".join(transpose(nth_split(m, s.k))).replace(" ", "")
