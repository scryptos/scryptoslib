class Ciphertext(object):
    def __init__(s, parent, v):
        s.parent = parent
        s.v = v
        s.is_homomorphic = hasattr(s.parent, "_homomorphic_type")
        if s.is_homomorphic:
            s.homomorphic_type = s.parent._homomorphic_type()

    def __add__(s, rhs):
        assert (
            s.is_homomorphic
        ), "The cryptosystem/cipher does not support homomorphic encryption"
        assert "+" in s.homomorphic_type, "Parents does not support addition"
        if isinstance(rhs, Ciphertext):
            assert rhs.parent == s.parent, "Invalid Parents: %s != %s" % (
                rhs.parent,
                s.parent,
            )
            return Ciphertext(s.parent, s.parent.hom("+", s.v, rhs.v))
        else:
            return s + s.parent.encrypt(rhs)

    def __mul__(s, rhs):
        assert (
            s.is_homomorphic
        ), "The cryptosystem/cipher does not support homomorphic encryption"
        if isinstance(rhs, Ciphertext):
            assert "*" in s.homomorphic_type, "Parents does not support multiplication"
            assert rhs.parent == s.parent, "Invalid Parents: %s != %s" % (
                rhs.parent,
                s.parent,
            )
            return Ciphertext(s.parent, s.parent.hom("*", s.v, rhs.v))
        else:
            if "*" in s.homomorphic_type:
                return s * s.parent.encrypt(rhs)
            elif "+" in s.homomorphic_type:
                bin_repr = map(int, format(rhs, "b"))
                t = s.parent.encrypt(0)
                for x in bin_repr:
                    if x:
                        t += s
                    t += t
                return t
            else:
                raise TypeError("Parents does not support multiplication")

    def __sub__(s, rhs):
        assert (
            s.is_homomorphic
        ), "The cryptosystem/cipher does not support homomorphic encryption"
        if isinstance(rhs, Ciphertext):
            assert rhs.parent == s.parent, "Invalid Parents: %s != %s" % (
                rhs.parent,
                s.parent,
            )
            if "-" in s.homomorphic_type:
                return Ciphertext(s.parent, s.parent.hom("-", s.v, rhs.v))
            return s + -rhs
        else:
            return s - s.parent.encrypt(rhs)

    def __div__(s, rhs):
        assert (
            s.is_homomorphic
        ), "The cryptosystem/cipher does not support homomorphic encryption"
        assert "/" in s.homomorphic_type, "Parents does not support division"
        if isinstance(rhs, Ciphertext):
            assert rhs.parent == s.parent, "Invalid Parents: %s != %s" % (
                rhs.parent,
                s.parent,
            )
            return Ciphertext(s.parent, s.parent.hom("/", s.v, rhs.v))
        else:
            return s / s.parent.encrypt(rhs)

    def __neg__(s):
        assert (
            s.is_homomorphic
        ), "The cryptosystem/cipher does not support homomorphic encryption"
        if "*" in s.homomorphic_type:
            return s * s.parent.encrypt(-1)
        elif "-" in s.homomorphic_type:
            return s.parent.encrypt(0) - s
        else:
            raise TypeError("Parents does not support negation")

    def __radd__(s, lhs):
        assert (
            s.is_homomorphic
        ), "The cryptosystem/cipher does not support homomorphic encryption"
        assert "+" in s.homomorphic_type, "Parents does not support addition"
        return s.parent.encrypt(lhs) + s

    def __rmul__(s, lhs):
        assert (
            s.is_homomorphic
        ), "The cryptosystem/cipher does not support homomorphic encryption"
        if "*" in s.homomorphic_type:
            return s.parent.encrypt(lhs) * s
        elif "+" in s.homomorphic_type:
            return s * lhs
        else:
            raise TypeError("Parents does not support multiplication")

    def __rsub__(s, lhs):
        assert (
            s.is_homomorphic
        ), "The cryptosystem/cipher does not support homomorphic encryption"
        assert "-" in s.homomorphic_type, "Parents does not support subtract"
        return s.parent.encrypt(lhs) - s

    def __rdiv__(s, lhs):
        assert (
            s.is_homomorphic
        ), "The cryptosystem/cipher does not support homomorphic encryption"
        assert "/" in s.homomorphic_type, "Parents does not support division"
        return s.parent.encrypt(lhs) / s

    def __eq__(s, rhs):
        if isinstance(rhs, Ciphertext):
            return s.v == rhs.v
        return s.v == rhs

    def __str__(s):
        return "Ciphertext of %s: %s" % (s.parent, s.v)

    def __repr__(s):
        return "%s(%r, %r)" % (s.__class__.__name__, s.parent, s.v)
