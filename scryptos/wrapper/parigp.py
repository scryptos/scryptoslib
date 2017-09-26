from subprocess import Popen, PIPE
from .common import check

memsize = None

PARI_LIB = [
  'default(colors,no)',
  'sqrtnall(x,n)={my(V,r,z,r2);r=sqrtn(x,n,&z);if(!z,error("Impossible case in sqrtn"));if(type(x)=="t_INTMOD"||type(x)=="t_PADIC",r2=r*z;n=1;while(r2!=r,r2*=z;n++));V=vector(n);V[1]=r;for(i=2,n,V[i]=V[i-1]*z);V}',
  'addhelp(sqrtnall,"sqrtnall(x,n):compute the vector of nth-roots of x")',
  'int2ff(n,g)={subst(Pol(digits(n,g.p)),\'x,g)}',
  'ff2int(x)={subst(x.pol,variable(x.pol),x.p)}'
]

def parigp(cmd, isAll=False, debug=False):
  global memsize
  assert check("gp")
  if isinstance(cmd, str):
    cmd = [cmd]
  cmd = PARI_LIB + cmd
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
