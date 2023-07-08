import binascii
import struct


def p64(x):
    return struct.pack("<Q", x)


def p32(x):
    return struct.pack("<I", x)


def p16(x):
    return struct.pack("<H", x)


def p8(x):
    return struct.pack("<B", x)


def u64(x):
    return struct.unpack("<Q", x)[0]


def u32(x):
    return struct.unpack("<I", x)[0]


def u16(x):
    return struct.unpack("<H", x)[0]


def u8(x):
    return struct.unpack("<B", x)[0]


def pb64(x):
    return struct.pack(">Q", x)


def pb32(x):
    return struct.pack(">I", x)


def pb16(x):
    return struct.pack(">H", x)


def pb8(x):
    return struct.pack(">B", x)


def ub64(x):
    return struct.unpack(">Q", x)[0]


def ub32(x):
    return struct.unpack(">I", x)[0]


def ub16(x):
    return struct.unpack(">H", x)[0]


def ub8(x):
    return struct.unpack(">B", x)[0]


unhex = binascii.unhexlify


def hexa(x, align=1):
    minus = False
    r = format(x, "x")
    if r[0] == "-":
        minus = True
        r = r[1:]
    if not len(r) % align == 0:
        r = ("0" * (align - len(r) % align)) + r
    r = "0x" + r
    if minus:
        r = "-" + r
    return r


def long_to_bytes(x):
    return binascii.unhexlify(hexa(x, 2)[2:])


def bytes_to_long(x):
    return int(x.hex(), 16)


def crc32(x):
    return binascii.crc32(x) % (1 << 32)
