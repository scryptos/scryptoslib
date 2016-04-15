from subprocess import Popen, PIPE
from .common import check

def parigp(cmd, isAll=False):
  assert check("gp")
  if isinstance(cmd, str):
    cmd = [cmd]
  s = "\n".join(cmd)
  p = Popen(["gp", "-q"], stdin=PIPE, stdout=PIPE)
  d, _ = p.communicate(s)
  if isAll:
    return d.split("\n")[:-1]
  else:
    return d.split("\n")[:-1][-1]
