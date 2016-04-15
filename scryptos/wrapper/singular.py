from subprocess import Popen, PIPE
from .common import check

def Singular(*cmd):
  assert check("Singular")
  s = ";".join(cmd) + ";"
  p = Popen(["Singular", "-q"], stdin=PIPE, stdout=PIPE)
  d, _ = p.communicate(s)
  return map(lambda x:x.split("=")[1], d.split("\n")[:-1])
