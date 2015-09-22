from scryptos.util.hexutil import *
from scryptos.util.tables import *
from itertools import product

def xorstr(s, key):
  out = ""
  if type(key) is int:
    key = hex(key, 2)[2:].decode("hex")
  for x in xrange(len(s)):
    out += chr(ord(s[x]) ^ ord(key[x % len(key)]))
  return out
def XORSearch(ciphertext, crib=None, mxlen=4, mslen=1, table=all_table, silent=False):
  key = ""
  candidate = []
  for x in xrange(mslen, mxlen + 1):
    if not silent: print "Searching XOR Key: Len %d..." % x
    for c in product(table, repeat=x):
      key = "".join(c)
      p = xorstr(ciphertext, key)
      if crib == None:
        if p in ascii_table:
          if not silent: print "Candidate: %s" % p
          candidate += [(key, p)]
      else:
        if crib in p:
          candidate += [(key, p)]
          if not silent: print "Matched! -> %s" % p
  return candidate
