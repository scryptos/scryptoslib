import binascii, struct

unhex = lambda x: int(x.replace(" ", "").replace("\t", "").replace("\n", ""), 16)
bswap = lambda x: unhex(hex(x).decode("hex")[::-1])
p64   = lambda x: struct.pack("<Q", x)
p32   = lambda x: struct.pack("<I", x)
p16   = lambda x: struct.pack("<H", x)
p8    = lambda x: struct.pack("<B", x)
u64   = lambda x: struct.unpack("<Q", x)[0]
u32   = lambda x: struct.unpack("<I", x)[0]
u16   = lambda x: struct.unpack("<H", x)[0]
u8    = lambda x: struct.unpack("<B", x)[0]


def hex(x, align=1):
  r = format(x, "x")
  if not len(r) % align == 0:
    r = ("0" * (align - len(r)%align)) + r
  return "0x" + r
