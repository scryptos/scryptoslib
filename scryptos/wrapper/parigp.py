from subprocess import Popen, PIPE
from .common import check

memsize = None

def parigp(cmd, isAll=False, debug=False):
  global memsize
  assert check("gp")
  if isinstance(cmd, str):
    cmd = [cmd]
  if memsize != None:
    cmd = ["allocatemem(%s)" % memsize] + cmd
  s = "\n".join(cmd)
  if debug:
    print "[+] Throughout to Pari/GP Commands: %r" % cmd
  p = Popen(["gp", "-q"], stdin=PIPE, stdout=PIPE)
  d, _ = p.communicate(s)
  if isAll:
    return d.split("\n")[:-1]
  else:
    return d.split("\n")[:-1][-1]

def set_gp_memalloc_size(size):
  global memsize
  memsize = size
