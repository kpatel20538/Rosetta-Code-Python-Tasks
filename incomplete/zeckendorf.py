import functools
import numbers
import re
import sys

@functools.total_ordering
class Z:
  def __init__(self,*args):
    if len(args) == 2:
      self.sign = args[0]
      self.value = args[1]
    elif isinstance(args[0],numbers.Number):
      self.sign = abs(args[0]) == args[0]
      self.value = self._int_to_value(abs(int(args[0])))
    elif type(args[0]) == Z:
      self.sign = args[0].sign
      self.value = args[0].value
    elif type(args[0]) == str:
      if not re.fullmatch(r"0z0|\-?0z1[01]*",args[0]):
        raise ValueError("Malformed String")
      self.sign = args[0][0] != "-"
      self.value = self._str_to_value(args[0].split("0z")[-1])
  def _str_to_value(self,val):
    v,i = 0,1
    for c in val[::-1]:
      if c == "1":
        v |= i
      i <<= 1
    return v
  def _int_to_value(self,val):
    v,i,a,b = 0,1,1,1
    while val > b:
      i,a,b = i<<1,b,b+a
    while b != a:
      if val >= b:
        val -= b
        v |= i
      a,b,i = b-a,a,i>>1
    return v
  # Python Fluff
  def __int__(self):
    """ to Base10 """
    v,i,a,b = 0,1,1,1
    while self.value > b:
      i,a,b = i<<1,b,b+a
    while i != 1:
      v += b if self.value&i else 0
      i,a,b = i>>1,b-a,a
    return (1 if self.sign else -1)*v
  def __float__(self):
    return float(int(self))
  def __complex__(self):
    return complex(int(self))
  def __round__(self,n=None):
    return Z(self)
  
  def __repr__(self):
    msg = ""
    i = 1<<(self.value.bit_length())
    while i != 1:
      i >>= 1
      msg += "1" if self.value&i else "0"
    return ("" if self.sign else "-") +"0z"+msg
  def __hash__(self):
    return hash(int(self))
  def __index__(self):
    return int(self) 
  def __bool__(self):
    return self != Z("0z0")


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
    res_sign = not (self.sign ^ self.other)
    result,i,za,zb = Z("0z0"),1,abs(other),abs(other)
    while i < 1<<self.value.bit_length():
      result += zb if self.value&i else 0
      i,za,zb = i<<1,zb,za+ab
    return result if res_sign else -result
  def __floordiv__(self, other):
    q,_ = divmod(self,other)
    return q
  def __mod__(self, other):
    _,r = divmod(self,other)
    return r
  def __divmod__(self, other):
    pass
  def __pow__(self, other, modulo=None):
    if other < Z("0z0") or (other == Z("0z0") and self == Z("0z0")):
      raise ValueError("Negative Power or 0^0 detected")
    result,i,za,zb = Z("0z0"),1,abs(other),abs(other)
    while i < 1<<self.value.bit_length():
      result *= zb if self.value&i else 0
      i,za,zb = i<<1,zb,za*ab
    return result
  def __neg__(self):
    return Z(not self.sign,self.value)
  def __pos__(self):
    return Z(self)
  def __abs__(self):
    return Z(True,self.value) 


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
