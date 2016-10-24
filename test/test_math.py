import unittest
from scryptos import num, contfrac, vector

class TestNum(unittest.TestCase):
  def setUp(s):
    pass

  def test_numtheory(s):
    s.assertEqual(num.gcd(2, 3), 1)
    s.assertEqual(num.gcd(4, 6), 2)
    s.assertEqual(num.lcm(2, 3), 6)
    s.assertEqual(num.lcm(2, 8), 8)
    s.assertEqual(num.modinv(17, 10007), 1766)
    s.assertEqual(num.modinv(7, 10007 * 10009), 28617161)
    s.assertTrue(1923 in num.modsqrt(5346, 10007))
    s.assertTrue(num.euler_phi(2, 2, 2), 4)
    s.assertTrue(num.euler_phi(10007, 10009), 100140048)

  def test_modular(s):
    s.assertEqual(num.egcd(2, 3), (-1, 1, 1))
    s.assertEqual(num.egcd(4, 6), (-1, 1, 2))
    s.assertEqual(num.crt([2, 3, 2], [3, 5, 7]), 23)
    s.assertEqual(num.crt([101, 6, 35], [111, 77, 85]), 545)
    s.assertTrue(num.is_prime(10007))
    s.assertFalse(num.is_prime(561))
    s.assertEqual(num.isqrt(121), 11)
    s.assertEqual(num.nth_root(19487171, 7), 11)

  def test_QR(s):
    s.assertEqual(num.legendre_symbol(4, 11), 1)
    s.assertEqual(num.legendre_symbol(2, 11), -1)
    s.assertEqual(num.legendre_symbol(11, 11), 0)
    s.assertEqual(num.jacobi_symbol(2, 15), 1)
    s.assertEqual(num.jacobi_symbol(7, 15), -1)
    s.assertEqual(num.jacobi_symbol(15, 15), 0)


class TestContfrac(unittest.TestCase):
  def setUp(s):
    pass

  def test_contfrac(s):
    s.assertEqual(contfrac.rational_to_contfrac(10007, 65537), [0, 6, 1, 1, 4, 1, 1, 2, 3, 1, 1, 1, 1, 2, 1, 2])
    s.assertEqual(contfrac.contfrac_to_rational([0, 6, 1, 1, 4, 1, 1, 2, 3, 1, 1, 1, 1, 2, 1, 2]), (10007, 65537))
    s.assertEqual(contfrac.convergents_from_contfrac([0, 6, 1, 1, 4, 1, 1, 2, 3, 1, 1, 1, 1, 2, 1, 2]), [(0, 1), (0, 1), (1, 6), (1, 7), (2, 13), (9, 59), (11, 72), (20, 131), (51, 334), (173, 1133), (224, 1467), (397, 2600), (621, 4067), (1018, 6667), (2657, 17401), (3675, 24068)])

class TestVector(unittest.TestCase):
  def setUp(s):
    pass

  def test_vector(s):
    u = [1, 6, 2, 3, 4]
    v = [2, 3, 4, 5, 7]
    s.assertEqual(vector.vector_add(u, v), [3, 9, 6, 8, 11])
    s.assertEqual(vector.vector_sub(u, v), [-1, 3, -2, -2, -3])
    s.assertEqual(vector.vector_dot_product(u, v), 71)
    s.assertEqual(vector.vector_scalarmult(2, u), [2, 12, 4, 6, 8])
    s.assertEqual(vector.vector_scalarmult(3, v), [6, 9, 12, 15, 21])
    s.assertEqual(vector.vector_norm_i(v), 10)

