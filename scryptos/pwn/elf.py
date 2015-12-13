import struct
import re

class EHDR:
  def __init__(s, d):
    s.e_magic = struct.unpack("BBBB", d[:4])
    (s.e_class, s.e_byteorder, s.e_hversion) = struct.unpack("BBB", d[4:7])
    s.e_pad = [0] * 9
    if s.e_class == 1:
      (s.e_filetype, s.e_archtype, s.e_fversion, s.e_entry, s.e_phdrpos, s.e_shdrpos, s.e_flags, s.e_hdrsize, s.e_phdrent, s.e_phdrcnt, s.e_shdrent, s.e_shdrcnt, s.e_strsec) = struct.unpack("<2H5I6H", d[16:52])
    elif s.e_class == 2:
      (s.e_filetype, s.e_archtype, s.e_fversion, s.e_entry, s.e_phdrpos, s.e_shdrpos, s.e_flags, s.e_hdrsize, s.e_phdrent, s.e_phdrcnt, s.e_shdrent, s.e_shdrcnt, s.e_strsec) = struct.unpack("<2HI3QI6H", d[16:64])
  def __len__(s):
    if s.e_class == 1:
      return 52
    elif s.e_class == 2:
      return 64

class PHDR:
  def __init__(s, d):
    (s.p_type, s.p_offset, s.p_vaddr, s.p_paddr, s.p_filesz, s.p_memsz, s.p_flags, s.p_align) = struct.unpack("<8I", d[:32])
  def __len__(s):
    return 32

class SHDR32:
  def __init__(s, d):
    (s.sh_name, s.sh_type, s.sh_flags, s.sh_addr, s.sh_offset, s.sh_size, s.sh_link, s.sh_info, s.sh_align, s.sh_entsize) = struct.unpack("<10I", d[:40])
  def __len__(s):
    return 40

class SHDR64:
  def __init__(s, d):
    (s.sh_name, s.sh_type, s.sh_flags, s.sh_addr, s.sh_offset, s.sh_size, s.sh_link, s.sh_info, s.sh_align, s.sh_entsize) = struct.unpack("<2I4Q2I2Q", d[:64])
  def __len__(s):
    return 64

class SymTab32:
  def __init__(s, d, strtab):
    s.a = 1
    (s.sym_name, s.sym_value, s.sym_size, typebind, s.sym_other, s.sym_sect) = struct.unpack("3I2BH", d)
    s.sym_type = typebind & 0xFF00 >> 8
    s.sym_bizsnd = typebind & 0xFF
    if not strtab == None:
      s.name = strtab[s.sym_name+1:]
      s.name = s.name[:s.name.index("\0")]
      s.name = re.match("(.+)(@.+)?", s.name).group(1)
  def __len__(s):
    return 16

class SymTab64:
  def __init__(s, d, strtab):
    s.a = 1
    (s.sym_name, typebind, s.sym_other, s.sym_sect, s.sym_value, s.sym_size) = struct.unpack("I2BH2Q", d)
    s.sym_type = typebind & 0xFF00 >> 8
    s.sym_bizsnd = typebind & 0xFF
    if not strtab == None:
      s.name = strtab[s.sym_name+1:]
      s.name = s.name[:s.name.index("\0")]
      s.name = re.match("(.+)(@.+)?", s.name).group(1)
  def __len__(s):
    return 24

class ELF:
  def __init__(s, f, base=0):
    s.base = base
    s.data = open(f, "rb").read()
    s.ehdr = EHDR(s.data)
    data = s.data[s.ehdr.e_phdrpos:]
    s.phdrs = [PHDR(data[x*s.ehdr.e_phdrent:(x+1)*s.ehdr.e_phdrent]) for x in xrange(s.ehdr.e_phdrcnt)]

    data = s.data[s.ehdr.e_shdrpos:]
    if s.ehdr.e_class == 1:
      s.shdrs = [SHDR32(data[x*s.ehdr.e_shdrent:(x+1)*s.ehdr.e_shdrent]) for x in xrange(s.ehdr.e_shdrcnt)]
    elif s.ehdr.e_class == 2:
      s.shdrs = [SHDR64(data[x*s.ehdr.e_shdrent:(x+1)*s.ehdr.e_shdrent]) for x in xrange(s.ehdr.e_shdrcnt)]
    if s.ehdr.e_shdrcnt > 0:
      symtab = s._section(".symtab")
      strtab = s._section(".strtab")
      s.symbols = []
      if not symtab == None and not strtab == None:
        d = s.data[symtab.sh_offset:symtab.sh_offset + symtab.sh_size]
        strtab = s.data[strtab.sh_offset:strtab.sh_offset + strtab.sh_size]
        while len(d) > 0:
          if s.ehdr.e_class == 1:
            s.symbols += [SymTab32(d[:16], strtab)]
          elif s.ehdr.e_class == 2:
            s.symbols += [SymTab64(d[:24], strtab)]
          d = d[len(s.symbols[0]):]

  def set_base(s, base):
    s.base = base

  def section(s, name):
    return s._section(name).sh_addr + s.base

  def _section(s, name):
    shstrtab = s.shdrs[s.ehdr.e_strsec]
    print repr(s.data[shstrtab.sh_offset:][:shstrtab.sh_size])
    if name in s.data[shstrtab.sh_offset:][:shstrtab.sh_size]:
      idx = s.data[shstrtab.sh_offset:][:shstrtab.sh_size].index(name)
      for x in s.shdrs:
        if x.sh_name == idx:
          return x

  def addr(s, name):
    for x in s.symbols:
      if x.name == name:
        return x.sym_value + s.base

  def resolve_name(s, address):
    for x in s.symbols:
      if x.sym_value + s.base <= address < x.sym_value + x.sym_size + s.base:
        return x.name
