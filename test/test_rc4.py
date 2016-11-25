import unittest
from scryptos import RC4
import random
import gmpy

class TestRC4(unittest.TestCase):
  def setUp(s):
    pass
  def test_RC4(s):
    rc4 = RC4("abcdefghijklmn")
    s.assertEqual(rc4.decrypt('\xd6@\x9b \xf9.\x867\x9b\x145\x91\xd1;\xb8\x0b\x9c\xd787\xe8\xf6\xb4\xd9\xbc\xcda\xd3\xf1$-\xb1\x94\xb2\x01\x13\xa4P\x8c'), "this is test message hogefuga foobarbaz")
