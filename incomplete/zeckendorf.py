import functools
import numbers
import re
import sys

@functools.total_ordering
class Z:
  def __init__(self,value=None):
    if value is None:
      self.sign = True
      self.value = 0
    elif type(value) == Z:
      self.sign = value.sign
      self.value = value.value
    elif type(value) == str:
      if not re.fullmatch(r"0z0|\-?0z1[01]*",value):
        raise ValueError("Malformed String")
      self.sign = value[0] != "-"
      self.value = self._str_to_value(value.split("0z")[-1])
    elif isinstance(value,numbers.Number):
      self.sign = abs(value) == value
      self.value = self._int_to_value(abs(int(value)))
  def _str_to_value(self,val):
    v,i = 0,1
    for c in val[::-1]:
      if c == "1":
        v |= i
      i <<= 1
    return v
  def _int_to_value(self,val):
    i,a,b = 1,1,1
    while val >= b:
      i,a,b=i<<1,b,a+b
    i,a,b=i>>1,b-a,a
    v = 0
    while a > 0:
      if val >= b:
        val -= b
        v |= i
      i,a,b=i>>1,b-a,a
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
    return ("" if self.sign else "-")+"0z"+bin(self.value)[2:]
      
  def __hash__(self):
    return hash(int(self))
  def __index__(self):
    return int(self) 
  def __bool__(self):
    return self != Z("0z0")
  
  def _comparator(self,other):
    if self.sign ^ other.sign:
      return self.sign
    if self.value.bit_length() > other.value.bit_length():
      return self.sign
    if self.value.bit_length() < other.value.bit_length():
      return not self.sign
    comp = self.value ^ other.value
    if comp.bit_length():
      msb = comp.bit_length()
      return bool((self.value ^ (((~self.sign)<<msb)>>1)) & ((1<<msb)>>1))
    return None
  
  # Zeckendorf's Arithmetic
  def __lt__(self,other):
    comp = self._comparator(other)
    return False if comp is None else not comp 
  def __eq__(self,other):
    comp = self._comparator(other)
    return comp is None
  def __add__(self, other):
    signed_addition = self.sign ^ other.sign
    a,b = abs(self),abs(other)
    sign_res = self.sign
    if signed_addition:
      comp = self._comparator(other)
      if comp is None:
        return Z("0z0")
      elif not comp:
        sign_res = other.sign
        a,b = b,a
      summation = a.value
      difference = b.value
      carry = 0
      ## Removing Difference Flag
      while difference:
        nonzero = summation | carry
        zero = ~nonzero
  
        rule1 = nonzero & difference
        rule2 = nonzero & zero << 1 & ((difference & ~1) << 1)
        rule3 = nonzero & zero << 1 & zero << 2 & difference << 2
        rule4 = nonzero & zero << 1 & ((difference &  1) << 1)
        rule5 = nonzero & zero << 1 & zero << 2 & ~difference & ~(difference << 1) & ~(difference << 2)
  
        carry_down = rule1 | rule2 | rule3 | rule4 | rule5
        increment = rule2 >> 2
        set_bit = rule3 >> 1 |rule4 >> 1 | rule5 >> 1 | rule5 >> 2
        clear_bit = rule1 | rule2 >> 1 | rule3 >> 2 | rule4 >> 1
  
        carry = (carry & ~carry_down)
        summation = (summation ^ carry_down)
        carry = carry | ((summation | set_bit) & increment)
        summation = (summation | set_bit) ^ increment
        difference = difference & ~clear_bit
    else:
      summation = self.value ^ other.value
      carry = self.value & other.value
    ## Removing Carry Flag
    while carry:
      zero = ~( summation | carry)
      one = summation & ~carry
      rule1 = carry & ~(carry&3)
      rule2 = carry&3 & zero >> 1
      rule3 = carry&3 & one >> 1 & zero >> 2
      
      clear_carry = rule1 | rule2 | rule3
      clear_sum = rule1 | rule3 << 1
      set_sum = rule2 << 1 | rule2 >> 1 | rule3 | rule3 << 2
      increment = rule1 << 1 | rule1 >> 2
      
      carry &= ~clear_carry
      summation &= ~clear_sum
      carry = carry | ((summation | set_sum) & increment)
      summation = (summation | set_sum) ^ increment
    ## Canonizing
    window = (summation)<<1 & summation & (~summation>>1) 
    while window:
      summation ^= ((window<<1) | window | (window>>1))
      window = (summation)<<1 & summation & (~summation>>1)
    placeholder = Z()
    placeholder.sign = self.sign
    placeholder.value = summation
    return placeholder
  def __sub__(self, other):
    return self + (-other)
  def __mul__(self, other):
    res_sign = not (self.sign ^ other.sign)
    product,operand = Z("0z0"),abs(self)
    i,a,b,za,zb = 1,Z("0z1"),Z("0z1"),abs(other),abs(other)
    while operand > b:
      i,a,b,za,zb = i<<1,b,b+a,zb,zb+za
    while a > Z("0z0"):
      if self.value&i:
        product += zb
      i,a,b,za,zb = i>>1,b-a,a,zb-za,za
    return product if res_sign else -product
  def __divmod__(self, other):
    res_sign = not (self.sign ^ other.sign)
    quotient,remainder = Z("0z0"),abs(self)
    a,b,za,zb = Z("0z1"),Z("0z1"),abs(other),abs(other)
    while remainder > zb:
      a,b,za,zb = b,b+a,zb,zb+za
    while remainder > abs(other):
      if remainder > zb:
        quotient += b
        remainder -= zb
      a,b,za,zb = b-a,a,zb-za,za
    if res_sign:
      return quotient,remainder
    else:
      return -quotient,remainder-abs(other)
  def __floordiv__(self, other):
    q,_ = divmod(self,other)
    return q
  def __mod__(self, other):
    _,r = divmod(self,other)
    return r
  def __pow__(self, other, modulo=None):
    if other < Z("0z0") or (other == Z("0z0") and self == Z("0z0")):
      raise ValueError("Negative Power or 0^0 detected")
    result,i,za,zb = Z("0z1"),1,abs(self),abs(self)
    while i < 1<<other.value.bit_length():
      if other.value&i:
        result *= zb
        if modulo is not None:
          result %= modulo
      i,za,zb = i<<1,zb,za*ab
    return result
  def __neg__(self):
    placeholder = Z()
    placeholder.sign = not self.sign
    placeholder.value = self.value
    return placeholder
  def __pos__(self):
    return Z(self)
  def __abs__(self):
    placeholder = Z()
    placeholder.sign = True
    placeholder.value = self.value
    return placeholder


def task(argv):
  """ Implement Zeckendorf's Arithmetic for addition, subtraction,
  muliplaction, and division.
  """
  print("Integer")
  a = Z(-23)
  print(int(a))
  
  print("Addition")
  a = Z("0z10")
  a += Z("0z10")
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
  c += Z("0z101")
  print(c)
  
  print("Division")
  d = Z("0z1001010")
  q = d//Z("0z1010")
  r = d%Z("0z1010")
  print(q,r)
  print(q*Z("0z1010")+r)
  
  return 0

if __name__ == "__main__":
  sys.exit(task(sys.argv))
