from subprocess import Popen, PIPE
from .common import check
import sys

def fplll(m, mode, external_options=[]):
  if not check("fplll"):
    sys.stderr.write("Please install from https://github.com/dstehle/fplll\n")
    assert False
  s = "["
  for x in m:
    s += "[" + " ".join(["%d"%y for y in x]) + "]"
  s += "]"
  p = Popen(["fplll", "-a", mode] + external_options, stdin=PIPE, stdout=PIPE)
  d, _ = p.communicate(s)
  return eval(d.replace("\n", ",").replace(" ", ",")[:-1])

def lll(m):
  return fplll(m, "lll")
def svp(m):
  return fplll(m, "svp")
def bkz(m, block_size):
  return fplll(m, "bkz", ["-b", str(block_size)])
