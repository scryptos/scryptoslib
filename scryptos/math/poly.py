from scryptos.wrapper import *
import math

def coppersmith_howgrave_method(polynomial, N, beta=1, X=None, eps=0.05):
  if X == None:
    X = eval(parigp("round(%d ^ (1.0 / 4 - %s)" % (N, str(eps))))
  d = eval(parigp(["n = %d" % N, "pol = %s" % polynomial, "beta = round(n^%s)" % str(beta), "X = %d" % X, "zncoppersmith(pol, n, X, beta)"]))
  return d

def poly_monic(polynomial, modulo=None):
  if modulo == None:
    return parigp(["pol = %s" % polynomial, "a = pollead(pol)", "v = variable(pol)", "subst(pol, v, v/a)"])
  else:
    return parigp(["pol = (%s) * Mod(1, %d)" % (polynomial, modulo), "a = pollead(pol)", "liftall(pol * 1/a)"])

if __name__ == "__main__":
  pol = "x^3+10*x^2+5000*x-222"
  n = 10001
  print coppersmith_howgrave_method(pol, n, 0.5) # 4

  N = 10007 * 10009
  pad = 30
  q = 10009
  qbar = q + pad

  d = coppersmith_howgrave_method("x + %d" % (-qbar % N), N, 0.5)[0] # => 30
  print d
  print (qbar - d)%(10007*10009) # => 10009

  print poly_monic("3*x^2+x+1")
  print poly_monic("3*x^2+x+1", 5)
