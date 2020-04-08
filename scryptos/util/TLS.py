from scryptos.util.stringutil import xorbytes
import operator as op
import hashlib
import hmac

"""
Helper function library for TLS (Pre-)Master Secret Calulcation

References:
  [RFC2246] The TLS Protocol Version 1.0 - https://tools.ietf.org/html/rfc2246
  [RFC4346] The Transport Layer Security (TLS) Protocol Version 1.1 - https://tools.ietf.org/html/rfc4346
  [RFC5246] The Transport Layer Security (TLS) Protocol Version 1.2 - https://tools.ietf.org/html/rfc5246
"""


def p_hash(algo, secret, seed, size):
  """
  Calculate PHASH function
  Args:
    algo : Hash algorithm (e.g. sha1, md5, sha256, ...)
    secret : (Pre-)Master Secret
    seed : Hash Seed
    size : Output Size
  References :
    * [RFC2246] Section 5. HMAC and the pseudorandom function
  """
  out = bytearray([])
  algo = hashlib.__getattribute__(algo.lower())
  a = seed
  while len(out) < size:
    a = hmac.new(secret, a, algo).digest()
    out += hmac.new(secret, bytearray(a) + bytearray(seed), algo).digest()
  return out[:size]

def PRF(algo, secret, label : bytes, seed, size):
  """
    Pseudorandom Function for TLS 1.2
    Args:
      algo : Hash algorithm (e.g. sha1, md5, sha256, ...)
      secret : (Pre-)Master Secret
      label : Identifying label of PRF Value
      seed : Hash Seed
      size :  Output Size
    References :
      * [RFC5246] Section 5.  HMAC and the Pseudorandom Function
  """
  return p_hash(algo, secret, bytearray(label) + bytearray(seed), size)

def PRF_v1_v1_1(algo, secret, label : bytes, seed, size):
  """
    Pseudorandom Function for TLS 1.1 / 1.0
    Args:
      algo : Hash algorithm (e.g. sha1, md5, sha256, ...)
      secret : (Pre-)Master Secret
      label : Identifying label of PRF Value
      seed : Hash Seed
      size :  Output Size
    References :
      * [RFC2246] Section 5. HMAC and the Pseudorandom function
      * [RFC4346] Section 5. HMAC and the Pseudorandom function
  """
  s1 = secret[:len(secret)//2]
  s2 = secret[len(secret)//2:]
  l = bytearray(label) + bytearray(seed)
  return xorbytes(p_hash("md5", s1, l, size), p_hash("sha1", s2, l, size))

def calc_master_secret_v1_v1_1(algo, pre_master_secret, client_random, server_random):
  """
    Calculate Master Secret for TLS 1.1 / 1.0
    Args:
      algo : Hash algorithm (e.g. sha1, md5, sha256, ...)
      pre_master_secret : Pre-Master Secret
      client_random : Client Random
      server_random : Server Random
    References:
      * [RFC2246] Section 8.1. Computing the master secret
      * [RFC4346] Section 8.1. Computing the Master Secret
  """
  return PRF_v1_v1_1(algo, pre_master_secret, b"master secret", client_random + server_random, 48)

def calc_master_secret(algo, pre_master_secret, client_random, server_random):
  """
    Calculate Master Secret for TLS 1.2
    Args:
      algo : Hash algorithm (e.g. sha1, md5, sha256, ...)
      pre_master_secret : Pre-Master Secret
      client_random : Client Random
      server_random : Server Random
    References:
      * [RFC5246] Section 8.1. Computing the Master Secret
  """
  return PRF(algo, pre_master_secret, b"master secret", client_random + server_random, 48)
