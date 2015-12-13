from subprocess import Popen, PIPE, STDOUT
from threading  import Thread, Event
import select
import socket
import os
import sys
import fcntl
import telnetlib

class Tube:
  def __init__(s, filename="", host="", port=-1, args=[], debug=False, auto_argv_0=True):
    s.debug = debug
    if filename != "":
      if auto_argv_0:
        args = [filename] + args
      s.proc_sock(args)
    elif host != "" and port != -1:
      s.p = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      s.p.connect((host, port))
      s.p.setblocking(0)
      print "\x1b[0;32m[+] Connected: %s:%d\x1b[0m" % (host, port)
    else:
      raise Exception("Invalid Argument")

  def proc_sock(s, args):
    def run_server(s, e, argv):
      c, _ = s.proc_sock.accept()
      s.proc_sock.close()
      p = Popen(argv, stdin=c, stdout=c, stderr=c)
      print "\x1b[0;32m[+] Start Process: %s args: %s PID=%d\x1b[0m" % (args[0], repr(args), p.pid)
      if s.debug:
        raw_input("\x1b[0;32mPlease enter key to continue...\x1b[0m")
      e.set()
      p.wait()
      c.close()
    s.proc_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.proc_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.proc_sock.bind(("", 0))
    s.proc_sock.listen(1)
    e = Event()
    t = Thread(target=run_server, args=(s, e, args))
    t.start()
    s.p = socket.create_connection(s.proc_sock.getsockname())
    e.wait()

  def read(s, l=-1):
    select.select([s.p], [], [])
    try:
      if l == -1:
        l = 16777216
      return s.p.recv(l)
    except IOError:
      return ""

  def read_until(s, crib):
    r = s.read(len(crib))
    while not r.endswith(crib):
      r += s.read(1)
    return r

  def readline(s):
    return s.read_until("\n")

  def write(s, x):
    select.select([], [s.p], [])
    s.p.sendall(x)

  def writeline(s, x):
    s.write(x + "\n")

  def interact(s, fd=-1):
    check = 'echo -e "\x1b[32mGot a shell!\x1b[0m"\n'
    t = telnetlib.Telnet()
    t.sock = s.p
    if fd != -1:
      s.write(check)
      sys.stdout.write(s.read())
      s.write('exec /bin/sh <&%d >&%d 2>&%d\n' % (fd, fd, fd))
    t.interact()
    t.close()
