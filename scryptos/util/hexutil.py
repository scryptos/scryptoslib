import binascii

globals()["__builtins__"].update({
  "hex"  : lambda x:format(x, "x"),
  "unhex": lambda x:int(x.replace(" ", "").replace("\t", "").replace("\n", ""), 16),
  "bswap": lambda x:unhex(hex(x).decode("hex")[::-1])
})

