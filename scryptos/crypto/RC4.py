from scryptos.math.num import *
from .Ciphertext import Ciphertext


class RC4(object):
    """
    RSA Public/Private Key Class
    """

    def __init__(s, key):
        """
        Constructor of RC4
        Args:
          key : RC4 Key
        """
        s.key = key

    def init_ksa(s):
        import math

        s.table = list(range(256))
        j = 0
        key = s.key * int(math.ceil(256.0 / len(s.key)))
        for i in range(256):
            j = (j + s.table[i] + ord(key[i])) % 256
            s.table[i], s.table[j] = s.table[j], s.table[i]

    def prga(s, length):
        s.init_ksa()
        i, j = 0, 0
        rand = ""
        for _ in range(length):
            i = (i + 1) % 256
            j = (j + s.table[i]) % 256
            s.table[i], s.table[j] = s.table[j], s.table[i]
            rand += chr(s.table[(s.table[i] + s.table[j]) % 256])
        return rand

    def encrypt(s, m, raw=False):
        """
        RC4 Encryption
        Args:
          m   : Plaintext Message (must be string object)
          raw : Is result wrapped by Ciphertext object?
        Return: RC4 Ciphertext object or Encrypted String (c_i = m_i XOR PRGA())
        """
        c = "".join([chr(ord(x) ^ ord(y)) for x, y in zip(m, s.prga(len(m)))])
        if raw:
            return c
        return Ciphertext(s, c)

    def decrypt(s, c):
        """
        RC4 Decryption
        Args:
          c : Ciphertext (must be string object or Ciphertext object)
        Return: RC4 Decrypted String (same as `encrypt`)
        """
        if isinstance(c, Ciphertext):
            c = c.v
        return s.encrypt(c, True)

    def __str__(s):
        return "RC4 Instance: key = %r" % s.key

    def __repr__(s):
        return "RC4(%r)" % s.key
