import os
import sys


def check(cmd, error=True):
    if not any(
        map(lambda x: os.path.exists(x + "/" + cmd), (os.environ["PATH"].split(":")))
    ):
        if error:
            sys.stderr.write("Error: %s not found.\n" % cmd)
        return False
    return True
