from scryptos import *

class Scytale:
  def __init__(s, k):
    s.k = k
  def encrypt(s, m):
    return "".join(transpose(nth_split(m, len(m)/s.k))).replace(" ", "")

  def decrypt(s, m):
    return "".join(transpose(nth_split(m, s.k))).replace(" ", "")
