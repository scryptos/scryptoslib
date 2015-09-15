from subprocess import Popen, PIPE
import os
import sys

def check():
  if not any(map(lambda x:os.path.exists(x+"/fplll"), (os.environ["PATH"].split(":")))):
    sys.stderr.write("Error: fplll not found.\n")
    sys.stderr.write("Please install from https://github.com/dstehle/fplll\n")
    return False
  return True

def fplll(m, mode):
  assert all([len(x) == len(m) for x in m])
  assert check()
  s = "["
  for x in m:
    s += "[" + " ".join(["%d"%y for y in x]) + "]"
  s += "]"
  p = Popen(["fplll", "-r", "%d"%len(m), "-c", "%d"%len(m[0]), "-a", mode], stdin=PIPE, stdout=PIPE)
  d, _ = p.communicate(s)
  return eval(d.replace("\n", ",").replace(" ", ",")[:-1])

def lll(m):
  return fplll(m, "lll")
def svp(m):
  return fplll(m, "svp")
def bkz(m):
  return fplll(m, "bkz")
