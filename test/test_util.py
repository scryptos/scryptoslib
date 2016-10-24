import unittest
from scryptos import hexutil, stringutil

class TestHexUtil(unittest.TestCase):
  def setUp(s):
    pass

  def test_pack(s):
    s.assertEqual(hexutil.p64(0xdeadbeefcafebabe), '\xbe\xba\xfe\xca\xef\xbe\xad\xde')
    s.assertEqual(hexutil.p32(0xdeadbeef), '\xef\xbe\xad\xde')
    s.assertEqual(hexutil.p16(0x1234), '\x34\x12')
    s.assertEqual(hexutil.p8(0xef), '\xef')

  def test_unpack(s):
    s.assertEqual(hexutil.u64('\xbe\xba\xfe\xca\xef\xbe\xad\xde'), 0xdeadbeefcafebabe)
    s.assertEqual(hexutil.u32('\xef\xbe\xad\xde'), 0xdeadbeef)
    s.assertEqual(hexutil.u16('\x34\x12'), 0x1234)
    s.assertEqual(hexutil.u8('\xef'), 0xef)

  def test_bpack(s):
    s.assertEqual(hexutil.pb64(0xdeadbeefcafebabe), '\xbe\xba\xfe\xca\xef\xbe\xad\xde'[::-1])
    s.assertEqual(hexutil.pb32(0xdeadbeef), '\xef\xbe\xad\xde'[::-1])
    s.assertEqual(hexutil.pb16(0x1234), '\x34\x12'[::-1])
    s.assertEqual(hexutil.pb8(0xef), '\xef')

  def test_bunpack(s):
    s.assertEqual(hexutil.ub64('\xbe\xba\xfe\xca\xef\xbe\xad\xde'[::-1]), 0xdeadbeefcafebabe)
    s.assertEqual(hexutil.ub32('\xef\xbe\xad\xde'[::-1]), 0xdeadbeef)
    s.assertEqual(hexutil.ub16('\x34\x12'[::-1]), 0x1234)
    s.assertEqual(hexutil.ub8('\xef'), 0xef)

  def test_misc(s):
    s.assertEqual(hexutil.hexa(0xabcd), '0xabcd')
    s.assertEqual(hexutil.hexa(0xabcd, 8), '0x0000abcd')
    s.assertEqual(hexutil.hexa(-0xabcd, 6), '-0x00abcd')
    s.assertEqual(hexutil.long_to_bytes(0xabcd), '\xab\xcd')
    s.assertEqual(hexutil.crc32('abcdefg'), 0x312a6aa6)

class TestStringUtil(unittest.TestCase):
  def setUp(s):
    pass

  def test_string_func(s):
    s.assertEqual(stringutil.xorstr('abcdefgsomethingthisistesttext', 'scryptos'),  '\x12\x01\x11\x1d\x15\x12\x08\x00\x1c\x0e\x17\r\x18\x1d\x01\x14\x07\x0b\x1b\n\x19\x07\x1b\x16\x00\x17\x06\x1c\x08\x00')
    s.assertEqual(stringutil.xorstr('abcdefg', 0x20), 'ABCDEFG')
    s.assertEqual(stringutil.mapstr('abcdefgsomethingthisistesttext', 'scryptos', lambda x,y: chr(abs(ord(x) - ord(y)))), '\x12\x01\x0f\x15\x0b\x0e\x08\x00\x04\n\r\x05\x08\x0b\x01\x0c\x01\x05\t\x06\x07\x01\x05\x0e\x00\x11\x02\x14\x08\x00')
    s.assertEqual(stringutil.transpose(["abcdefg", "hijklmn"]), 'ahbicjdkelfmgn')
    s.assertEqual(stringutil.nth_split('thisistesttextflag{wei}', 4), ['this', 'iste', 'stte', 'xtfl', 'ag{w', 'ei}'])
