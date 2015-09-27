from subprocess import Popen, PIPE
import os
import sys

def check():
  if not any(map(lambda x:os.path.exists(x+"/nasm"), (os.environ["PATH"].split(":")))):
    sys.stderr.write("Error: nasm not found.\n")
    return False
  return True

def asm(asm, bit=32):
  assert check()
  s = ("[BITS %d]\n" % bit)+"\n".join(asm)
  open("/tmp/nasm.in", "w").write(s) 
  p = Popen(["nasm", "-o", "/tmp/nasm.out", "/tmp/nasm.in"], stdout=PIPE)
  p.wait()
  return open("/tmp/nasm.out", "rb").read()

def disasm(data, bit=32, org=0):
  assert check()
  p = Popen(["ndisasm", "-o", format(org), "-b", str(bit), "-"], stdin=PIPE, stdout=PIPE)
  d = p.communicate(data)
  return map(lambda x: x.split("  ")[-1], d[0].split("\n"))[:-1]


