from subprocess import Popen, PIPE
import os
import sys

def check():
  if not any(map(lambda x:os.path.exists(x+"/gp"), (os.environ["PATH"].split(":")))):
    sys.stderr.write("Error: Pari/GP not found.\n")
    return False
  return True

def parigp(cmd):
  assert check()
  s = "\n".join(cmd)
  p = Popen(["gp", "-q"], stdin=PIPE, stdout=PIPE)
  d, _ = p.communicate(s)
  return d.split("\n")[:-1][-1]
