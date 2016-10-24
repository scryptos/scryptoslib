from scryptos.math import *
from itertools import cycle, starmap
import operator as op
import gmpy

def vector_scalarmult(a, v):
  """
  Scalar Multiplication of Vector
  Args:
    a : A scalar
    v : A vector
  Return: Vector a*v
  """
  return list(starmap(op.mul, zip(cycle([a]), v)))

def vector_norm_i(v):
  """
  Calculate Norm of vector as Integer
  Args:
    v : A vector
  Return: || v ||
  """
  return int(gmpy.ceil(gmpy.sqrt(sum(starmap(op.pow, zip(v, cycle([2])))))))

def vector_add(u, v):
  """
  Addition of vector
  Args:
    u : A vector
    v : A vector
  Return: vector u + v
  """
  assert len(u) == len(v)
  return list(starmap(op.add, zip(u, v)))

def vector_sub(u, v):
  """
  Subtract of vector
  Args:
    u : A vector
    v : A vector
  Return: vector u - v
  """
  assert len(u) == len(v)
  return list(starmap(op.sub, zip(u, v)))

def vector_dot_product(u, v):
  """
  Calculate Dot product
  Args:
    u : A vector
    v : A vector
  Return: u . v
  """
  assert len(u) == len(v)
  return sum(starmap(op.mul, zip(u, v)))
