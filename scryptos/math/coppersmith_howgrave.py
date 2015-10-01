from scryptos.wrapper import parigp, fplll

def coppersmith_howgrave_method(polynomial, N, beta=1):
  delta = eval(parigp.parigp(["f = %s" % polynomial, "poldegree(f)"]))
  epsilon = eval(parigp.parigp(["%g/7.0" % beta]))
  m = eval(parigp.parigp(["ceil(%g^2/(%g*%g))" % (beta, delta, epsilon)]))
  t = eval(parigp.parigp(["floor(%g * %g * ((1/%g) - 1))" % (delta, m, beta)]))
  X = eval(parigp.parigp(["ceil(%g^(%g^2/%g - %g))" % (N, beta, delta, epsilon)]))
  gij = "g(x) = { x^%d * %d ^ %d * f(x)^%d }"
  ti  = "t(x) = { f(x)^%d * x^%d }"
  g = []
  n = m*delta+t

  for i in xrange(m):
    for j in xrange(delta):
      g += [eval(parigp.parigp(["f(x) = %s" % polynomial, gij % (j, N, m-i, i), "Vec(g(x*%d))" % X]))]
  for i in range(t):
    g += [eval(parigp.parigp(["f(x) = %s" % polynomial, ti % (m, i), "Vec(t(x*%d))" % X]))]
  mx_d = max(map(len, g))
  for x in xrange(len(g)):
    g[x] = [0] * (mx_d - len(g[x])) + g[x]
  g = map(lambda x: x[::-1], g)

  m = fplll.lll(g)

  coeffs = []
  for x in xrange(n):
    coeffs += ["%d/%d"%(m[0][x], X**x)]
  coeffs = coeffs[::-1]
  o_pol = parigp.parigp(["Pol([%s])" % ", ".join(coeffs)])
  s = int(parigp.parigp(["pol=%s" % o_pol, "floor(real(polroots(pol)[1]))"]))
  return s

"""
N = 10007 * 10009
pad = 30
q = 10009
qbar = q + pad

d = coppersmith_howgrave_method("x + %d" % (-qbar % N), N, 0.5) # => 30
print (qbar - d)%(10007*10009) # => 10009
"""
