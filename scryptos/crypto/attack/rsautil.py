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
    from scryptos.crypto import Ciphertext

    assert rsa1.n == rsa2.n
    if isinstance(c1, Ciphertext):
        c1 = c1.v
    if isinstance(c2, Ciphertext):
        c2 = c2.v
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
    from scryptos.math import LLL
    import gmpy2

    eset = list(map(lambda x: x.e, rsa_list))
    nset = list(map(lambda x: x.n, rsa_list))
    r = len(eset)
    M = int(gmpy2.floor(gmpy2.sqrt(nset[-1])))
    B = []
    B += [[M] + eset]
    for x in range(r):
        B += [[0] * (x + 1) + [-nset[x]] + [0] * (r - x - 1)]
    S = LLL(B)
    d = abs(S[0][0]) // M
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
    from scryptos.crypto import Ciphertext

    ct_list = [c.v if isinstance(c, Ciphertext) else c for c in ct_list]
    assert all([x.e == rsa_list[0].e for x in rsa_list[1:]])
    assert len(ct_list) == len(rsa_list) == rsa_list[0].e
    e = rsa_list[0].e
    x = crt(ct_list, list(map(lambda x: x.n, rsa_list)))
    return nth_root(x, e)


def wiener(rsa):
    """
    Attack to RSA: Wiener's Small Private Exponent Attack
    Args:
      rsa : RSA Object
    Return: RSA private key corresponding to `rsa`
    """
    from scryptos.math import (
        is_perfect_square,
        rational_to_contfrac,
        convergents_from_contfrac,
    )
    from scryptos.crypto.RSA import RSA

    e = rsa.e
    n = rsa.n
    frac = rational_to_contfrac(e, n)
    conv = convergents_from_contfrac(frac)
    for k, d in conv:
        if k != 0 and (e * d - 1) % k == 0:
            phi = (e * d - 1) // k
            s = n - phi + 1
            disc = s**2 - 4 * n
            if disc >= 0:
                t = is_perfect_square(disc)
                if t != -1 and (s + t) % 2 == 0:
                    # print("[+] d = %d" % d)
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
    from scryptos.crypto import Ciphertext

    if isinstance(c1, Ciphertext):
        c1 = c1.v
    if isinstance(c2, Ciphertext):
        c2 = c2.v
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
    from scryptos.math import (
        gcd,
        vector_add,
        vector_sub,
        vector_scalarmult,
        vector_norm_i,
        Orthogonal_Lattice,
    )
    from scryptos.crypto import RSA

    ITERATION_RANGE = range(-r, r + 1)
    assert len(fault_sigs) >= 5

    l = len(fault_sigs)
    # calculate v^\perp
    B = Orthogonal_Lattice([fault_sigs])
    assert len(B) == l - 1
    # calculate L'^\perp
    B2 = Orthogonal_Lattice(B[: l - 2])
    assert len(B2) == 2
    # enumerate u, v
    x, y = B2
    for a in ITERATION_RANGE:
        if int(vector_norm_i(a * x) ** 2) >= l * rsa.n:
            continue
        for b in ITERATION_RANGE:
            z = vector_add(vector_scalarmult(a, x), vector_scalarmult(b, y))
            if int(vector_norm_i(z) ** 2) >= l * rsa.n:
                continue
            for c in vector_sub(fault_sigs, z):
                g = gcd(c, rsa.n)
                if 1 < g < rsa.n:
                    # print "FACTOR", g
                    p = g
                    q = rsa.n // g
                    return RSA(rsa.e, rsa.n, p, q)


def lsb_oracle(rsa, ciphertext, oracle, state=None, quiet=False):
    """
    Attack to RSA: LSB Oracle Attack
    Args:
      rsa        : RSA Object
      ciphertext : A ciphertext to decrypt
      oracle     : An oracle function
      state      : A state tuple (k, lb, ub) Default: (1, 0, rsa.n)
      quiet      : Is print debug message

    Note:
      `oracle` MUST return 0 or 1

    Return: Decrypted ciphertext
    Reference: https://crypto.stackexchange.com/questions/11053/rsa-least-significant-bit-oracle-attack
    """
    from fractions import Fraction

    if state is not None:
        k, lb, ub = state
    else:
        k, lb, ub = 1, 0, Fraction(rsa.n)

    while True:
        o = oracle((rsa.encrypt(pow(2, k, rsa.n)) * ciphertext).v)
        if o == 1:
            lb = (ub + lb) / 2
        else:
            ub = (ub + lb) / 2
        if not quiet:
            print(repr((k, lb, ub)))
        if int(lb - ub) == 0:
            break
        k += 1
    return int(ub)
