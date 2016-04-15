from subprocess import Popen, PIPE
from .common import check

def asm(asm, bit=32):
  assert check("nasm")
  if isinstance(asm, str):
    asm = [asm]
  s = ("[BITS %d]\n" % bit)+"\n".join(asm)
  open("/tmp/nasm.in", "w").write(s) 
  p = Popen(["nasm", "-o", "/tmp/nasm.out", "/tmp/nasm.in"], stdout=PIPE)
  p.wait()
  return open("/tmp/nasm.out", "rb").read()

def disasm(data, bit=32, org=0):
  assert check("ndisasm")
  p = Popen(["ndisasm", "-o", format(org), "-b", str(bit), "-"], stdin=PIPE, stdout=PIPE)
  d = p.communicate(data)
  return map(lambda x: x.split("  ")[-1], d[0].split("\n"))[:-1]


