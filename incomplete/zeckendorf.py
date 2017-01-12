import functools
import sys

@functools.total_ordering()
class Z:
  def __init__(self,val):
    pass

  # Python Fluff
  def __repr__(self):
    pass
  def __hash__(self):
    pass
  def __bool__(self):
    pass
  def __index__(self):
    pass
  def __complex__(self):
    pass
  def __int__(self):
    pass
  def __float__(self):
    pass
  def __round__(self,n=None):
    pass

  # Zeckendorf's Arithmetic
  def __lt__(self,other):
    pass
  def __eq__(self,other):
    pass
  def __add__(self, other):
    pass
  def __sub__(self, other):
    pass
  def __mul__(self, other):
    pass
  def __floordiv__(self, other):
    pass
  def __mod__(self, other):
    pass
  def __divmod__(self, other):
    pass
  def __pow__(self, other,modulo=None):
    pass
  def __neg__(self):
    pass
  def __pos__(self):
    pass
  def __abs__(self):
    pass


def task(argv):
  """ Implement Zeckendorf's Arithmetic for addition, subtraction,
  muliplaction, and division.
  """
  print("Addition")
  a = Z("0z10")
  print(a)
  a += Z("0z10")
  print(a)
  a += Z("0z1001")
  print(a)
  a += Z("0z1000")
  print(a)
  a += Z("0z10101")
  print(a)
  
  print("Subtraction")
  b = Z("0z1000")
  b -= Z("0z101")
  print(b)
  b = Z("0z10101010")
  b -= Z("0z1010101")
  print(b)
  
  print("Multication")
  c = Z("0z1001")
  c *= Z("0z101")
  print(c)
  c = Z("0z101010")
  c *= Z("0z101")
  print(c)
  
  print("Division")
  d = Z("0z1001010")
  d //= Z("0z1010")
  print(d)
  d = Z("0z1001010")
  d %= Z("0z1010")
  print(d)
  return 0
  
if __name__ == "__main__":
  sys.exit(task(sys.argv))
