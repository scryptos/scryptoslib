from scryptos.crypto.attack import prngutil
from scryptos.crypto import mt19937
import random
import unittest


class TestMT19937(unittest.TestCase):
  def setUp(s):
    pass

  def test_mt19937(s):
    seed = 0xdeadbeef
    mt = mt19937(seed)
    random.seed(seed)
    s.assertEqual(mt.next(), 956529277)
    s.assertEqual(mt.next(), 3842322136)
    s.assertEqual(mt.next(), 3319553134)
    s.assertEqual(mt.next(), 1843186657)
    s.assertEqual(mt.next(), 2704993644)

    d = []
    for _ in range(624):
      d += [random.getrandbits(32)]
    mt = prngutil.crack_mt19937(d)
    for x in range(624):
      s.assertEqual(mt.next(), d[x])
    for x in range(624):
      s.assertEqual(mt.next(), random.getrandbits(32))
    for x in range(624):
      mt.prev()
    for x in d[::-1]:
      s.assertEqual(mt.prev(), x)

    mt = mt19937(seed)
    rand = [mt.next() for _ in range(624)]
    s.assertEqual(prngutil.crack_mt19937_using_index_difference(rand[227], rand[0], 227, 0), [seed])

class TestLCG(unittest.TestCase):
  def setUp(s):
    pass

  def test_lcg(s):
    M = 65537
    A = 114
    B = 514
    x = 893

    x = (A * x + B) % M
    a = x

    x = (A * x + B) % M
    b = x

    x = (A * x + B) % M
    c = x
    s.assertEqual(prngutil.crack_lcg(a, b, c, M), (A, B))
