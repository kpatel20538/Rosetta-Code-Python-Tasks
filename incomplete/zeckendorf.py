import functools
import numbers
import re
import sys

@functools.total_ordering()
class Z:
  def __init__(self,val):
    if isinstance(val,numbers.Number):
      self.sign = abs(val) == val
      self.value = self._int_to_value(abs(int(val)))
    elif type(val) == Z:
      self.sign = val.sign
      self.value = val.value
    elif type(val) == str:
      if not re.fullmatch(r"0z0|\-?0z1[01]*",val):
        raise ValueError("Malformed String")
      self.sign = val[0] != "-"
      self.value = self._str_to_value(val.split("0z")[-1])
  def _str_to_value(self,val):
    v,i = 0,0
    for c in val[::-1]:
      if c == "1":
        v |= i
      i <<= 1
    return v
  def _int_to_value(self,val):
    v,i,a,b = 0,0,1,1
    while val <= b:
      i,a,b = i+1,b,b+a
    while val:
      if val > b:
        val -= b
        v |= 1<<i
      a,b = b-a,a
    return v
  # Python Fluff
  def __repr__(self):
    return ("" if self.sign else "-") +"0z"+str(self.value)
  def __hash__(self):
    return hash(int(self))
  def __bool__(self):
    return self != Z("0z0")
  def __index__(self):
    return int(self) 
  def __complex__(self):
    return complex(int(self))
  def __int__(self):
    """ to Base10 """
    v,a,b = 0,1,1
    for i in range(self.value.bit_length()):
      v += b*bool(z&1<<i)
      a,b = b-a,a
    return v
  def __float__(self):
    return float(int(self))
  def __round__(self,n=None):
    return Z(self)

  # Zeckendorf's Arithmetic
  def __lt__(self,other):
    pass
  def __eq__(self,other):
    pass
  def __add__(self, other):
    pass
  def __sub__(self, other):
    return self + (-other)
  def __mul__(self, other):
    pass
  def __floordiv__(self, other):
    q,_ = divmod(self,other)
    return q
  def __mod__(self, other):
    _,r = divmod(self,other)
    return r
  def __divmod__(self, other):
    pass
  def __pow__(self, other, modulo=None):
    pass
  def __neg__(self):
    self.sign = False
    return Z(self)
  def __pos__(self):
    return Z(self)
  def __abs__(self):
    self.sign = True
    return Z(self) 


def task(argv):
  """ Implement Zeckendorf's Arithmetic for addition, subtraction,
  muliplaction, and division.
  """
  print("Integer")
  a = Z(-23)
  print(int(a))
  
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
