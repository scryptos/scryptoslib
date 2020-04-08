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
  p = Popen(["fplll", "-r", str(len(m)), "-c", str(len(m[0])), "-a", mode] + external_options, stdin=PIPE, stdout=PIPE)
  d, _ = p.communicate(s.encode())
  d = d.decode()
  return eval(d.replace("\n", ",").replace(" ", ",")[:-1])

def fplll_lll(m):
  return fplll(m, "lll")
def fplll_svp(m):
  return fplll(m, "svp")
def fplll_bkz(m, block_size):
  return fplll(m, "bkz", ["-b", str(block_size)])
