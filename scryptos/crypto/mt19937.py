class mt19937(object):
    """
    Invertible mt19937
    Reference: http://plusletool.hatenablog.jp/entry/2014/10/27/230000
    """

    N = 624
    M = 397
    MATRIX_A = 0x9908B0DF
    UPPER_MASK = 0x80000000
    LOWER_MASK = 0x7FFFFFFF
    TEMPER_MASK_B = 0x9D2C5680
    TEMPER_MASK_C = 0xEFC60000
    mag01 = [0, MATRIX_A]
    MOD = 1 << 32

    def __init__(s, seed=None, state=None):
        """
        Constructor of mt19937
        Args:
          seed  : mt19937 seed
          state : mt19937 state
        """
        s.index = 0
        if seed is None and state is None:
            raise RuntimeError("Missing Argument")
        if seed is not None:
            s.table = [0 for _ in range(s.N)]
            s.table[0] = seed
            for i in range(1, s.N):
                s.table[i] = (
                    (((s.table[i - 1] >> 30) ^ s.table[i - 1]) * 0x6C078965) % s.MOD + i
                ) % s.MOD
            for i in range(s.N):
                s.next()
            s.index = 0
        elif state is not None:
            assert len(state) >= s.N
            s.table = state[: s.N]

    def next(s):
        """
        Get next random value
        Return: Next random
        """
        res = s.table[s.index % s.N]
        s.table[s.index % s.N] = s.calc_next(s.table, s.index)
        s.index += 1
        return s.tempering(res)

    def prev(s):
        """
        Get previous random value
        Return: Previous random
        """
        s.index -= 1
        res = s.calc_prev(s.table, s.index)
        s.table[s.index % s.N] = res
        return s.tempering(res)

    @classmethod
    def calc_next(cls, data, index):
        """
        INNER FUNCTION: calculate next random from data/index
        Args:
          data  : Random State
          index : State Index
        Return: Next random
        """
        assert data is not None
        assert len(data) == cls.N
        x = (data[index % cls.N] & cls.UPPER_MASK) | (
            data[(index + 1) % cls.N] & cls.LOWER_MASK
        )
        nxt = data[(index + cls.M) % cls.N] ^ (x >> 1) ^ cls.mag01[x & 1]
        return nxt

    @classmethod
    def calc_prev(cls, data, index):
        """
        INNER FUNCTION: calculate previous random from data/index
        Args:
          data  : Random State
          index : State Index
        Return: Previous random
        """
        assert data is not None
        assert len(data) == cls.N
        tail = data[(index + cls.N - 1) % cls.N] ^ data[(index + cls.M - 1) % cls.N]
        body = tail ^ cls.mag01[(tail >> 31)]
        head = data[(index + cls.N) % cls.N] ^ data[(index + cls.M) % cls.N]
        prv = (
            ((head << 1) & cls.UPPER_MASK)
            ^ ((body << 1) & cls.LOWER_MASK)
            ^ (tail >> 31)
        )
        return prv

    @classmethod
    def untempering(cls, rand):
        """
        Invert function of mt19937 tempering function
        Args:
          rand : A random value generated by mt19937
        Return: Untempered `rand`
        """
        rand ^= rand >> 18
        rand ^= (rand << 15) & cls.TEMPER_MASK_C
        a = rand ^ ((rand << 7) & cls.TEMPER_MASK_B)
        b = rand ^ ((a << 7) & cls.TEMPER_MASK_B)
        c = rand ^ ((b << 7) & cls.TEMPER_MASK_B)
        d = rand ^ ((c << 7) & cls.TEMPER_MASK_B)
        rand = rand ^ ((d << 7) & cls.TEMPER_MASK_B)
        rand ^= (rand ^ (rand >> 11)) >> 11
        return rand

    @classmethod
    def tempering(cls, rand_seed):
        """
        mt19937 tempering function
        Args:
          rand_seed : A random seed value
        Return: tempered `rand_seed`
        """
        rand_seed ^= rand_seed >> 11
        rand_seed ^= (rand_seed << 7) & cls.TEMPER_MASK_B
        rand_seed ^= (rand_seed << 15) & cls.TEMPER_MASK_C
        rand_seed ^= rand_seed >> 18
        return rand_seed
