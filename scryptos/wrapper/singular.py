from subprocess import Popen, PIPE
import os
import sys

def check():
  if not any(map(lambda x:os.path.exists(x+"/Singular"), (os.environ["PATH"].split(":")))):
    sys.stderr.write("Error: Singular not found.\n")
    return False
  return True

def Singular(*cmd):
  assert check()
  s = ";".join(cmd) + ";"
  p = Popen(["Singular", "-q"], stdin=PIPE, stdout=PIPE)
  d, _ = p.communicate(s)
  return map(lambda x:x.split("=")[1], d.split("\n")[:-1])
