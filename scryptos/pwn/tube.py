from subprocess import Popen, PIPE, STDOUT
import select
import socket
import os
import sys
import fcntl
import telnetlib

class Tube:
  def __init__(s, filename="", host="", port=-1, stderr=STDOUT, args=[], debug=False):
    def setNonBlocking(fobj):
      f = fcntl.fcntl(fobj, fcntl.F_GETFL)
      f |= os.O_NONBLOCK
      fcntl.fcntl(fobj, fcntl.F_SETFL, f)

    if filename != "":
      s.t = "POPEN"
      if args == []:
        args = [filename]
      s.p = Popen(args, stdin=PIPE, stdout=PIPE, stderr=stderr, bufsize=1)
      setNonBlocking(s.p.stdout)
      setNonBlocking(s.p.stdin)
      print "\x1b[0;32m[+] Start Process: %s args: %s PID=%d\x1b[0m" % (filename, repr(args), s.p.pid)
      if debug:
        raw_input("\x1b[0;32mPlease enter key to continue...\x1b[0m")
    elif host != "" and port != -1:
      s.t = "SOCKET"
      s.p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.p.connect((host, port))
      s.p.setblocking(0)
      print "\x1b[0;32m[+] Connected: %s:%d\x1b[0m" % (host, port)
    else:
      raise Exception("Invalid Argument")

  def read(s, l=-1):
    if s.t == "POPEN":
      try: 
        s.flush()
        r = s.p.stdout.read(l)
        return r
      except IOError:
        return ""
    elif s.t == "SOCKET":
      try:
        if l == -1:
          l = 16777216
        return s.p.recv(l)
      except IOError:
        return ""

  def read_until(s, crib):
    if s.t == "POPEN":
      r = ""
      while True:
        r += s.read(1)
        if crib in r:
          return r

  def readline(s):
    return s.read_until("\n")

  def write(s, x):
    if s.t == "POPEN":
      s.p.stdin.write(x)
      s.flush()
    elif s.t == "SOCK":
      s.p.sendall(x)

  def writeline(s, x):
    s.write(x + "\n")

  def flush(s):
    if s.t == "POPEN":
      s.p.stdin.flush()
      s.p.stdout.flush()

  def interact(s, fd=-1):
    check = "echo \x1b[0;37mGot a shell!\x1b[0m"
    if s.t == "POPEN":
      r = ""
      if fd != -1:
        m = 'exec /bin/sh <&%d >&%d 2>&%d\n' % (fd, fd, fd)
        s.writeline(m)
        s.writeline(check)
      while True:
        rfd, wfd, xfd = select.select([s.p.stdout, sys.stdin], [], [])
        if s.p.stdout in rfd:
          try:
            sys.stdout.write(s.read())
          except EOFError:
            print '*** Connection closed by remote host ***'
            break
        elif sys.stdin in rfd:
          r = sys.stdin.readline()
          if not r:
            break
          s.write(r)
          s.flush()
    elif s.t == "SOCKET":
      t = telnetlib.Telnet()
      t.sock = s.p
      t.interact()
