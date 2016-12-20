from subprocess import Popen, PIPE
from .common import check
import os

def singular(cmd, isAll=False, debug=False):
  assert check("Singular")
  if isinstance(cmd, str):
    cmd = [cmd]
  s = ";\n".join(cmd) + ";"
  if debug:
    print "[+] Throughout to Singular Commands: %r" % cmd
  tmpname = os.tempnam()
  open(tmpname).write(s)
  p = Popen(["Singular", "-bq", tempname], stdin=PIPE, stdout=PIPE)
  d, _ = p.communicate()
  os.remove(tmpname)
  if isAll:
    return d.split("\n")[:-1]
  else:
    return d.split("\n")[:-1][-1]
