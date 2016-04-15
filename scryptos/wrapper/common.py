import os
import sys

def check(cmd):
  if not any(map(lambda x:os.path.exists(x+"/" + cmd), (os.environ["PATH"].split(":")))):
    sys.stderr.write("Error: %s not found.\n" % cmd)
    return False
  return True

