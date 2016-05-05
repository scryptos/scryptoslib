from scryptos.util.stringutils import xorstr

class RC4:
  def __init__(s, k=None, state=None):
    assert k != None or state != None
    if k != None:
      if type(k) is str:
        k = map(ord, k)
      s.k = k
      s.init_state()
    elif state != None:
      assert type(state) is list and len(state) == 256
      s.keystate = state

  def init_state(s):
    state = range(256)
    j = 0
    for  i in xrange(0, 256):
      j = (j + state[i] + s.k[i % len(s.k)]) % 256
      state[i], state[j] = state[j], state[i]
    s.keystate = state

  def prga(s, l):
    i = 0
    j = 0
    ret = []
    state = s.keystate
    for _ in xrange(l):
      i = (i + 1) % 256
      j = (j + state[i]) % 256
      state[i], state[j] = state[j], state[i]
      ret += [state[(state[i] + state[j]) % 256]]
    return ret

  def encrypt(s, m):
    key = map(chr, s.prga(len(m)))
    return xorstr(m, key)

  def decrypt(s, c):
    return s.encrypt(c)


if __name__ == "__main__":
  # ksnctf
  rc4 = RC4("M6eMYngDGFbYE9HQ")
  print rc4.decrypt('\xbf\xff\x1b\rG\xa7\x18O\xcb\xd6\\Y\x95asW\xb3\xd1\x94\x9f\xac') == 'FLAG_MEyR4Zf4A4HFW73k'
