def common_modulus(rsa1, rsa2, c1, c2):
  """
  Attack to RSA: Common Modulus Attack
  Args:
    rsa1 : RSA Object 1
    rsa2 : RSA Object 2
    c1   : ciphertext encrypted by `rsa1`
    c2   : ciphertext encrypted by `rsa2`
  Return: plaintext message
  """
  from scryptos.math import egcd, modinv
  assert rsa1.n == rsa2.n
  a, b, g = egcd(rsa1.e, rsa2.e)
  if a < 0:
    c1 = modinv(c1, rsa1.n)
    a *= -1
  if b < 0:
    c2 = modinv(c2, rsa2.n)
    b *= -1
  return (pow(c1, a, rsa1.n) * pow(c2, b, rsa2.n)) % rsa1.n

def common_private_exponent(rsa_list):
  """
  Attack to RSA: Common Private-Exponent Attack
  Args: 
    rsa_list : RSA Object List (They have a same private exponent)
  Return: Private Exponent
  Reference: http://ijcsi.org/papers/IJCSI-9-2-1-311-314.pdf
  """
  from scryptos.wrapper import lll
  import math
  import gmpy
  eset = map(lambda x: x.e, rsa_list)
  nset = map(lambda x: x.n, rsa_list)
  r = len(eset)
  M = int(gmpy.floor(gmpy.sqrt(nset[-1])))
  B = []
  B += [[M] + eset]
  for x in xrange(r):
    B += [[0]*(x+1) + [-nset[x]] + [0] * (r-x-1)]
  S = lll(B)
  d = abs(S[0][0])/M
  return d

def hastads_broadcast(rsa_list, ct_list):
  """
  Attack to RSA: Hastad's Broadcast Attack (Only CRT Attack)
  Args:
    rsa_list: RSA Object List
    ct_list : Ciphertext List (they have same plain message)
  Return: Plain Message
  """
  from scryptos.math import crt, nth_root
  assert all([x.e == rsa_list[0].e for x in rsa_list[1:]])
  assert len(ct_list) == len(rsa_list) == rsa_list[0].e
  e = rsa_list[0].e
  x = crt(ct_list, map(lambda x: x.n, rsa_list))
  return nth_root(x, e)

def wiener(rsa):
  """
  Attack to RSA: Wiener's Small Private Exponent Attack
  Args:
    rsa : RSA Object
  Return: RSA private key corresponding to `rsa`
  """
  from scryptos.math import is_perfect_square, rational_to_contfrac, convergents_from_contfrac
  from scryptos.crypto.RSA import RSA
  e = rsa.e
  n = rsa.n
  frac = rational_to_contfrac(e, n)
  conv = convergents_from_contfrac(frac)
  for (k, d) in conv:
    if k != 0 and (e*d - 1) % k == 0:
      phi = (e * d - 1) % k
      s = n - phi + 1
      disc = s**2 - 4*n
      if disc >= 0:
        t = is_perfect_square(disc)
        if t != -1 and (s + t) % 2 == 0:
          # print "[+] d = %d" % d
          return RSA(e, n, d=d)

def franklin_reiter(rsa, a, b, c1, c2):
  """
  Attack to RSA: Franklin-Reiter's Related Message Attack
  - related message example: plain message `m1`, and `m2` = `a` * `m1` + `b`
  Args:
    rsa : RSA Object
    a   : linear parameter A
    b   : linear parameter B
    c1  : cipher text 1 (corresponding to `m1`)
    c2  : cipher text 2 (corresponding to `m2` = `a` * `m1` + `b`)
  Return: Recovered `m1`
  Reference: https://www.cs.unc.edu/~reiter/papers/1996/Eurocrypt.pdf
  """
  from scryptos.wrapper import parigp
  expr = []
  expr += ["g1 = Mod(x^%d, %d) - %d" % (rsa.e, rsa.n, c1)]
  expr += ["g2 = Mod(%d * x + %d, %d)^%d - %d" % (a, b, rsa.n, rsa.e, c2)]
  expr += ["g = gcd(g1, g2)"]
  expr += ["lift(-Vec((Pol(Vec(g)*Vec(g)[1]^-1)))[2])"]
  r = eval(parigp(expr))
  return r

def fault_crt_signature(rsa, m, sig):
  """
  Attack to RSA: Boneh, DeMillo and Lipton's CRT-Fault Attack
  This attack is Known-Plaintext-Attack
  Args:
    rsa : RSA Object
    m   : plaintext message
    sig : Faulted signature of `m`
  Return: Recovered RSA Private Key corresponding to `rsa`
  """
  from scryptos.math import gcd
  from scryptos.crypto.RSA import RSA
  p = gcd((pow(sig, rsa.e, rsa.n) - m) % rsa.n, rsa.n)
  if 1 < p < rsa.n and rsa.n % p == 0:
    return RSA(rsa.e, rsa.n, p)

def modulus_fault_crt(rsa, fault_sigs, r=50):
  """
  Attack to RSA: Brier et al.'s Modulus Fault Attack
  Args:
    rsa        : RSA Object
    fault_sigs : Fault Signatures (len(fault_sigs) >= 5)
    r          : Tweakable Iteration Range
  Return: Recovered RSA Private Key
  Reference : https://eprint.iacr.org/2011/388.pdf
  """
  from scryptos.math import gcd, vector_add, vector_sub, vector_scalarmult, vector_norm_i
  from scryptos.crypto import RSA
  ITERATION_RANGE = xrange(-r, r+1)
  assert len(fault_sigs) >= 5

  def lattice_orthogonal(vs):
    """
    From: `Merkle-Hellman Revisited: A Cryptanalysis of the Qu-Vanstone Cryptosystem Based on Group Factorizations` - Algorithm 5
    Reference implementation: https://gist.github.com/hellman/350bed296fc66bcb128dcf7da014684e
    """
    from scryptos.math import vector_norm_i, vector_dot_product
    from scryptos.wrapper import lll
    n = len(vs[0])
    d = len(vs)
    c = 2**((n-1)/2 + (n-d)*(n-d-1)/4)
    c = c * reduce(lambda x,y:x*vector_norm_i(y), vs, 1)
    M = []
    for i in xrange(n):
      a = []
      for j in xrange(d):
        a += [c * vs[j][i]]
      a += [0] * i + [1] + [0] * (n-i-1)
      M += [a]
    B = lll(M)
    # perspective map
    res = [r[-n:] for r in B]
    res = res[:n-d]
    for r in res:
      assert all(vector_dot_product(r, v) == 0 for v in vs)
    return res

  l = len(fault_sigs)
  # calculate v^\perp
  B = lattice_orthogonal([fault_sigs])
  assert len(B) == l - 1
  # calculate L'^\perp
  B2 = lattice_orthogonal(B[:l-2])
  assert len(B2) == 2
  # enumerate u, v
  x, y = B2
  for a in ITERATION_RANGE:
    if int(vector_norm_i(a*x)**2) >= l*rsa.n:
      continue
    for b in ITERATION_RANGE:
      z = vector_add(vector_scalarmult(a, x), vector_scalarmult(b, y))
      if int(vector_norm_i(z)**2) >= l*rsa.n:
        continue
      for c in (vector_sub(fault_sigs, z)):
        g = gcd(c, rsa.n)
        if 1 < g < rsa.n:
          #print "FACTOR", g
          p = g
          q = rsa.n / g
          return RSA(rsa.e, rsa.n, p, q)
