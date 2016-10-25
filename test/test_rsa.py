import unittest
from scryptos import RSA, rsautil
import random
import gmpy

class TestRSA(unittest.TestCase):
  def setUp(s):
    pass
  def test_rsa(s):
    p = 10007
    q = 10009
    rsa = RSA(65537, p*q, p, q)
    s.assertEqual(rsa.d, 35910881)
    s.assertEqual(rsa.encrypt(2), 82696754)
    s.assertEqual(rsa.decrypt(82696754), 2)
    s.assertTrue(rsa.verify(2, 82696754))
    rsa = RSA(65537, p*q, p)
    s.assertEqual(rsa.q, q)
    rsa = RSA(65537, p*q, d=35910881)
    s.assertEqual(rsa.p, q)
    s.assertEqual(rsa.q, p)
    rsa = RSA(7, 17*19)
    s.assertEqual(rsa.to_pem(), '-----BEGIN PUBLIC KEY-----\nMBswDQYJKoZIhvcNAQEBBQADCgAwBwICAUMCAQc=\n-----END PUBLIC KEY-----')
    rsa2 = RSA.import_pem('-----BEGIN PUBLIC KEY-----\nMBswDQYJKoZIhvcNAQEBBQADCgAwBwICAUMCAQc=\n-----END PUBLIC KEY-----')
    s.assertEqual(rsa2.e, rsa.e)
    s.assertEqual(rsa2.n, rsa.n)

  # Common Modulus Attack
  def test_common_modulus(s):
    n = 100160063
    e1 = 65537
    e2 = 65539
    rsa1 = RSA(e1, n)
    rsa2 = RSA(e2, n)
    m = random.randint(2, n)
    c1 = rsa1.encrypt(m)
    c2 = rsa2.encrypt(m)
    s.assertEqual(rsautil.common_modulus(rsa1, rsa2, c1, c2), m)

  def test_common_private_exponent(s):
    # Common Private Exponent Attack
    # ek, nk from reference paper
    e1, n1 = 587438623,2915050561
    e2, n2 = 2382816879,3863354647
    e3, n3 = 2401927159,3943138939
    rsa1 = RSA(e1, n1)
    rsa2 = RSA(e2, n2)
    rsa3 = RSA(e3, n3)
    s.assertEqual(rsautil.common_private_exponent([rsa1, rsa2, rsa3]), 655)

  def test_hastads_broadcast(s):
    # Hastad's Broadcast Attack
    e = 3
    n1 = 100160063
    n2 = 100761443
    n3 = 101284087
    rsa1 = RSA(e, n1)
    rsa2 = RSA(e, n2)
    rsa3 = RSA(e, n3)
    m = random.randint(2, n1)
    c1 = rsa1.encrypt(m)
    c2 = rsa2.encrypt(m)
    c3 = rsa3.encrypt(m)
    s.assertEqual(rsautil.hastads_broadcast([rsa1, rsa2, rsa3], [c1, c2, c3]), m)

  def test_wiener(s):
    # Wiener's Attack
    e = 17993
    n = 90581
    rsa = RSA(e, n)
    rsa2 = rsautil.wiener(rsa)
    s.assertEqual(rsa2.d, 5)

  def test_franklin_reiter(s):
    # Franklin-Reiter Related Message Attack
    e = 255
    n = 100160063
    rsa = RSA(e, n)
    m1 = 86452943
    m2 = 7 * m1 + 3
    c1 = rsa.encrypt(m1)
    c2 = rsa.encrypt(m2)
    s.assertEqual(rsautil.franklin_reiter(rsa, 7, 3, c1, c2), m1)

  def test_fault_crt_signature(s):
    # Boneh-DeMillo-Lipton's CRT Fault Attack
    e = 65537
    n = 100160063
    m = 12345
    fault_sig = 82770107
    rsa = RSA(e, n)
    rsa2 = rsautil.fault_crt_signature(rsa, m, fault_sig)
    s.assertEqual(max(rsa2.p, rsa2.q), 10009)

  def test_modulus_fault_crt(s):
    n = 139597781215932958403361341802832587199L
    e = 65537
    rsa = RSA(e, n)
    fault_sigs = [1058535326842046404366164623977343348220096515298415971420L,
                  498516681624023022157905434041816372788280365785800693627L,
                  804996362997244807580066976356636401798047106638276618248L,
                  486102002898098045301788623412192711614890707650168500297L,
                  1109646572715192904427320549147799213950859213551899817975L]
    rsa2 = rsautil.modulus_fault_crt(rsa, fault_sigs)
    s.assertEqual(max(rsa2.p, rsa2.q), 14741565978953596877)

