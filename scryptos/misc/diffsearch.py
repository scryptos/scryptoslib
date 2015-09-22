from scryptos.util.hexutil import *
from scryptos.util.tables import *
from itertools import product

def DiffSearch(diffs, crib=None, silent=False):
  u = lambda x: "".join([chr(x)]+[chr((x + sum(diffs[:y+1])) % 256) for y in xrange(len(diffs))])
  candidate = []
  for x in xrange(256):
    p = u(x)
    if crib in u(x):
      candidate += [p]
      if not silent: print "Candidate: %s" % p
  return candidate
