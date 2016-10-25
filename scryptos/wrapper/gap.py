from subprocess import Popen, PIPE
from .common import check

def gap(cmd, isAll=False, debug=False):
  assert check("gap")
  if isinstance(cmd, str):
    cmd = [cmd]
  s = ";\n".join(cmd) + ";"
  if debug:
    print "[+] Throughout to GAP Commands: %r" % cmd
  p = Popen(["gap", "-q"], stdin=PIPE, stdout=PIPE)
  d, _ = p.communicate(s)
  if isAll:
    return d.split("\n")[:-1]
  else:
    return d.split("\n")[:-1][-1]
