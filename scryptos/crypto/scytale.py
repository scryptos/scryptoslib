from scryptos import *

def transpose(s):
  return "".join(map(lambda x: "".join(x), zip(*s)))

def nth_split(s, n):
  r = []
  i = 0
  while True:
    if i + n > len(s):
      r += [s[i:]]
      break
    r += [s[i:i+n]]
    i += n
  if r[-1] == "":
    r = r[:-1]
  return r

class Scytale:
  def __init__(s, k):
    s.k = k
  def encrypt(s, m):
    return "".join(transpose(nth_split(m, len(m)/s.k))).replace(" ", "")

  def decrypt(s, m):
    return "".join(transpose(nth_split(m, s.k))).replace(" ", "")
