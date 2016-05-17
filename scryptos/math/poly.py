from scryptos.wrapper import *
import math

def coppersmith_howgrave_method(polynomial, N, beta=1, eps=0.05):
  d = eval(parigp(["n = %d" % N, "pol = %s" % polynomial, "beta = round(n^%s)" % str(beta), "X = round(n ^ (1.0/4 - %s))" % str(eps), "zncoppersmith(pol, n, X, beta)"]))
  return d

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
