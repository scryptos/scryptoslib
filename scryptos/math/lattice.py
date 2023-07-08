from scryptos.wrapper import fplll_lll, parigp, gap
from scryptos.wrapper.common import check
from functools import reduce


def LLL(M, impl="auto"):
    """
    Calculate LLL-reduced Matrix
    Args:
      M    : A matrix
      impl : LLL Implementation (default: auto)
             You can select implementation: auto, fplll, parigp or gap
    Return: LLL-reduced Matrix
    """
    if impl == "auto":
        if check("fplll"):
            impl = "fplll"
        elif check("gap"):
            impl = "gap"
        elif check("gp"):
            impl = "parigp"
    if impl == "fplll":
        return fplll_lll(M)
    elif impl == "parigp":
        mat = "[" + "; ".join(map(lambda x: ", ".join(map(str, x)), M)) + "]"
        return eval(
            "["
            + parigp(
                ["M = mattranspose(%s)" % mat, "Str(mattranspose(M * qflll(M)))"]
            ).replace("; ", "], [")[1:-1]
            + "]"
        )
    elif impl == "gap":
        mat = str(M).replace("L", "")
        return eval(
            gap(["vector := %s" % mat, "LLLReducedBasis(vector).basis"]).rstrip(";")
        )
    else:
        raise RuntimeError("Invalid Implementation: %s" % impl)


def Rational_LLL(M, impl="auto"):
    """
    Calculate LLL-reduced Matrix on Rational Field
    Args:
      M    : A matrix
      impl : LLL Implementation (default: auto)
             You can select implementation: auto, fplll, parigp or gap
    Return: LLL-reduced Matrix
    Matrix Element Format: (num, denom)
    """
    from scryptos.math import gcd

    g = None
    for i in range(len(M)):
        for j in range(len(M[i])):
            if isinstance(M[i][j], int):
                continue
            if M[i][j][1] == 1:
                continue
            if g is None:
                g = M[i][j][1]
            else:
                g = gcd(g, M[i][j][1])
    for i in range(len(M)):
        for j in range(len(M[i])):
            if isinstance(M[i][j], int):
                M[i][j] = M[i][j] * g
            else:
                M[i][j] = M[i][j][0] * (g // M[i][j][1])
    B = LLL(M)
    for i in range(len(B)):
        for j in range(len(B[i])):
            p, q = (B[i][j], g)
            p, q = (p // gcd(p, q), q // gcd(p, q))
            if q == 1:
                B[i][j] = p
            else:
                B[i][j] = (p, q)
    return B


def Orthogonal_Lattice(vs):
    """
    From: `Merkle-Hellman Revisited: A Cryptanalysis of the Qu-Vanstone Cryptosystem Based on Group Factorizations` - Algorithm 5
    Reference implementation: https://gist.github.com/hellman/350bed296fc66bcb128dcf7da014684e
    """
    from scryptos.math import vector_norm_i, vector_dot_product, LLL

    n = len(vs[0])
    d = len(vs)
    c = 2 ** ((n - 1) // 2 + (n - d) * (n - d - 1) // 4)
    c = c * reduce(lambda x, y: x * vector_norm_i(y), vs, 1)
    M = []
    for i in range(n):
        a = []
        for j in range(d):
            a += [c * vs[j][i]]
        a += [0] * i + [1] + [0] * (n - i - 1)
        M += [a]
    B = LLL(M)
    # perspective map
    res = [r[-n:] for r in B]
    res = res[: n - d]
    for r in res:
        assert all(vector_dot_product(r, v) == 0 for v in vs)
    return res
