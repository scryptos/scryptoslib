#!/usr/bin/env python
import unittest
from scryptos import *

class RabinTest(unittest.TestCase):

    def test(self):
        pubkey = Rabin(n=77, b=2)
        c = pubkey.encrypt(32)
        print c

        privkey = Rabin(n=77, b=2, p=7, q=11)
        m_list = privkey.decrypt(c)
        print m_list
        self.assertTrue(32 in m_list)

class RSATest(unittest.TestCase):
    def test_rsa(self):
        rsa = RSA(7, 17*19)
        c = rsa.encrypt(123)
        print c

        rsa = RSA(7, 17*19, p=17, q=19)
        m = rsa.decrypt(c)
        print m
        self.assertTrue(c == 251 and m == 123)

    def test_common_modulus(self):
        rsa1 = RSA(3, 17*19)
        rsa2 = RSA(7, 17*19)

        c1 = rsa1.encrypt(123)
        c2 = rsa2.encrypt(123)

        m = rsa.common_modulus(rsa1, rsa2, c1, c2)
        print m
        self.assertTrue(m == 123)

    def test_franklin_raiter(self):
        a = 2
        b = 5
        e = 7
        n = 9967 * 9973

        m = 123456
        rsa = RSA(e, n)
        c1 = rsa.encrypt(m)
        c2 = rsa.encrypt(a*m+b)

        m0 = rsautil.franklin_raiter(rsa, a, b, [c1, c2])
        print m0
        self.assertTrue(m0 == 123456)

    def test_wiener(self):
        n = 0x009AD06BC971363A84B5936FF365518684B89866C76557EF6CAA3108EE1D15ACD87C01B6EF4B9E9F4ECCACFE21937FE66C7F86DB7A28B5B3F12A0F02218B8C8978963B82C4A75F260FC6AD6AB2275D57D8A2CAE879339D2252D6DA68A702C0174785554637E703E8ED4732FE2E19B2AACF113646D51986C88171D02E4913C3AE3A6A3FC9F98A58B445A3A9AE2357E3D537F6AF90EF78CB9B7B6A9634452A0292B1457F61DA822948583A29FE5CA31D45B353CDC756E101084EE6C96425B86E1DA62D657A1D59C270F2CBC0ADB46446F8ADFBCD7C2DBC7B5E7779505CB779A82E05A9A14E957745B092B7E644D70EA87ED8030021DCCD367D97C06CDEEDBF82AF77
        e = 0x340F753CB50C4DF1643C85A708EFFBC070E1E3C3E6B6BD8B03EEE8281A884AD0330869F6016E434B00F87B2CCF0DC22DB8EEBC6778AF81B880C9386305F7C6DFDF2FA5193C9663C53FE07AAE46115C087FC94F83C777B7FEBAABB23997985D6FFBF8FB06AD6176E54A9A75F637E3FB67C814DE298AF0A51650607C749A5618E4461D25F8D46086D0FFDC8805C30BB429826FA67CC287583E9514238194A71405D574EDB5722FB8FA92C2C6E9A9F61DA1528B165CDB3D86608FCF3BA3F2B36654F235EAC6B52594FE0704F946D54747E7F8754B80FF9EA4C397835275564D62E5D694538A7E44B4A82B7FE926B8F2D60C50F6286C4165FC8D9DD519CCD6D95249

        rsa = RSA(e, n)
        c = rsa.encrypt(12345)
        rsa = rsautil.wiener(rsa)
        print rsa
        m = rsa.decrypt(c)
        print m
        self.assertTrue(m == 12345)

    def test_high_bit_known(self):
      p, q = (10007, 10009)
      n = p*q
      e = 65537
      qbar = q + 30
      rsa = RSA(e=e, n=n)
      self.assertTrue(rsautil.high_bit_known(rsa, qbar, "pq") == (p, q))

    def test_bleichenbachers_signature_forgery(self):
      n = 0x6a7ce66be5565243fc6e989d6ef30d7db24ecf6d66137f84e22a94ee8590b5ad7e38a775602608f8669af8ffb7956952b6de2eb2e214c80bff8354ad84ef8092b73106c8de79bfda495e2ce6b261774781a09387e5d3d20215cf25a1a1329645422981aa759f2f4cf1cde00372838ea7a236efae68d6f01cb711253c94a6e608b18ae8f601a2ca5fd703fb050e19a7c37099a2035b46a2004ff397aec5bb59cc3c30975d577b9788bdc127441f2aafc8fcdf6241840e9fa0077aa19119cdd7d1a095513c61ac11db97fbdedf0beec0922825c8be5b5bd0522b5cc2f3cb3caecc895a4fde74283134294bf57d92853387bd2af6f3a523625884e134cceb818da9L
      e = 3L
      rsa = RSA(e, n)
      sig = rsautil.bleichenbachers_signature_forgery_with_e_3(rsa, "flag", rsautil.HASH_METHODS["SHA-256"])
      print sig

      print repr(long_to_bytes(rsa.encrypt(sig)))
      print repr(rsautil.HASH_METHODS["SHA-256"]("flag").digest())
      self.assertTrue(long_to_bytes(rsa.encrypt(sig)).endswith(rsautil.HASH_METHODS["SHA-256"]("flag").digest()))


class HexUtilTest(unittest.TestCase):
    def test_hex(self):
        t = hexutil.hex(127)
        self.assertTrue(t == "0x7f")
        t = hexutil.hex(127, 4)
        self.assertTrue(t == "0x007f")

    def test_pack(self):
      t = hexutil.p64(0xcafebabedeadbeef)
      print repr(t)
      self.assertTrue(t == "\xef\xbe\xad\xde\xbe\xba\xfe\xca")

      t = hexutil.p32(0xdeadbeef)
      print repr(t)
      self.assertTrue(t == "\xef\xbe\xad\xde")

      t = hexutil.p16(0x1234)
      print repr(t)
      self.assertTrue(t == "\x34\x12")

      t = hexutil.p8(0x7f)
      print repr(t)
      self.assertTrue(t == "\x7f")

    def test_unpack(self):
      t = hexutil.u64("\xef\xbe\xad\xde\xbe\xba\xfe\xca")
      print repr(t)
      self.assertTrue(t == 0xcafebabedeadbeef)

      t = hexutil.u32("\xef\xbe\xad\xde")
      print repr(t)
      self.assertTrue(t == 0xdeadbeef)

      t = hexutil.u16("\x34\x12")
      print repr(t)
      self.assertTrue(t == 0x1234)

      t = hexutil.u8("\x7f")
      print repr(t)
      self.assertTrue(t == 0x7f)

class VigenereTest(unittest.TestCase):
  def test_vigenere(s):
    c = Vigenere("CTF")
    s.assertTrue(c.encrypt("WEARESCRYPTOS") == "YXFTXXEKDRMTU")
    s.assertTrue(c.decrypt("YXFTXXEKDRMTU") == "WEARESCRYPTOS")

class ScytaleTest(unittest.TestCase):
  def test_scytale(s):
    c = Scytale(3)
    s.assertTrue(c.encrypt("HELLOWEARESCRYPTOS") == "HEREAYLRPLETOSOWCS")
    s.assertTrue(c.decrypt("HEREAYLRPLETOSOWCS") == "HELLOWEARESCRYPTOS")

if __name__ == '__main__':
    unittest.main()

