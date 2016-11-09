from scryptos.crypto.attack import mtutil
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
    for _ in xrange(624):
      d += [random.getrandbits(32)]
    mt = mtutil.crack(d)
    for x in xrange(624):
      s.assertEqual(mt.next(), d[x])
    for x in xrange(624):
      s.assertEqual(mt.next(), random.getrandbits(32))
    for x in xrange(624):
      mt.prev()
    for x in d[::-1]:
      s.assertEqual(mt.prev(), x)
