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
    while a > 0:
      if self.value&i:
        v += b 
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
      comp = a._comparator(b)
      if comp is None:
        return Z("0z0")
      elif not comp:
        sign_res = other.sign
        a,b = b,a
      carry = 0
      summation = a.value & (~b.value)
      difference = (~a.value) & b.value
      window = 7 << summation.bit_length()
      while window >> 3:
        window >>= 1
        carry_window = (carry&window) << 3 >> window.bit_length()
        sum_window = (summation&window) << 3 >> window.bit_length()
        diff_window = (difference&window) << 3 >> window.bit_length()
        clear_carry,set_carry,clear_sum,set_sum,toggle_sum,clear_diff = 0,0,0,0,0,0
        if (sum_window&4) or (carry_window&4) and (not (carry_window&3)):
          clear_carry |= 4
          toggle_sum |= 4
          if (not sum_window&3) and (not diff_window&3):
            set_sum |= 3
          elif (not sum_window&3) and (not diff_window&3^2):
            set_sum |= 1
            clear_diff |= 2
          elif (not sum_window&3^1) and (not diff_window&3^2):
            set_carry |= 1
            clear_sum |= 1
            clear_diff |= 2
          elif (not sum_window&3) and (not diff_window&3^1):
            set_sum |= 2
            clear_diff |= 1
          else:
            clear_carry = 0
            toggle_sum = 0
        carry &= ~(clear_carry << window.bit_length() >> 3)
        carry |= (set_carry << window.bit_length() >> 3)
        summation &= ~(clear_sum << window.bit_length() >> 3)
        summation |= (set_sum << window.bit_length() >> 3)
        summation ^= (toggle_sum << window.bit_length() >> 3)
        difference &= ~(clear_diff << window.bit_length() >> 3)
      if difference&1:
        difference &= ~1
        if carry&2:
          carry &= ~2
          summation |= 4
        elif summation&2:
          summation &= ~2
          summation |= 1
    else:
      summation = self.value ^ other.value
      carry = self.value & other.value
    ## Removing Carry Flag
    window = 15 << carry.bit_length()
    while window >> 4:
      window >>= 1
      sum_window = (summation&window) << 4 >> window.bit_length()
      carry_window = (carry&window) << 4 >> window.bit_length()
      clear_carry,clear_sum,set_sum = 0,0,0
      increment = False
      if (not (carry_window >> 1)^2) and ((not (sum_window >> 1)) or (not (sum_window >> 1)^2)):
        clear_carry |= 4
        set_sum |= 8
        increment = True
      elif (not (carry_window >> 1)^2) and (not (sum_window >> 1)^1):
        clear_carry |= 4
        clear_sum |= 2
        set_sum |= 12
      elif (not (carry_window >> 1)^1) and (not (sum_window >> 1)^2):
        clear_carry |= 2
        clear_sum |= 4
        set_sum |= 10
      carry &= ~(clear_carry << window.bit_length() >> 4)
      summation &= ~(clear_sum << window.bit_length() >> 4)
      summation |= (set_sum << window.bit_length() >> 4)
      if increment:
        carry ^= ((sum_window&1) << window.bit_length() >> 4)
        summation ^= (1 << window.bit_length() >> 4)
    if (not carry&3^1) and ((not summation&3^1) or (not summation&3)):
      carry &= ~1
      summation |= 2
    elif (not carry&7^2) and ((not summation&7^2) or (not summation&7)):
      carry &= ~2
      summation |= 5
    elif (not carry&7^2) and (not summation&7^1):
      carry &= ~2
      summation &= ~1
      summation |= 6
    elif (not carry&7^1) and (not summation&7^2):
      carry &= ~1
      summation &= ~2
      summation |= 5
    elif (not carry&15^2) and (not summation&15^4):
      carry &= ~2
      summation &= ~4
      summation |= 10
    ## Canonizing
    window = (summation)<<1 & summation & (~summation>>1) 
    while window:
      summation ^= ((window<<1) | window | (window>>1))
      window = (summation)<<1 & summation & (~summation>>1)
    placeholder = Z()
    placeholder.sign = sign_res
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
      if operand.value&i:
        product += zb
      i,a,b,za,zb = i>>1,b-a,a,zb-za,za
    return product if res_sign else -product
  def __divmod__(self, other):
    res_sign = not (self.sign ^ other.sign)
    quotient,remainder = Z("0z0"),abs(self)
    a,b,za,zb = Z("0z1"),Z("0z1"),abs(other),abs(other)    
    while remainder > zb:
      a,b,za,zb = b,b+a,zb,zb+za
    while remainder >= abs(other):
      if remainder >= zb:
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
    power,exponent = Z("0z1"),abs(other)
    i,a,b,za,zb = 1,Z("0z1"),Z("0z1"),abs(self),abs(self)
    while exponent > b:
      i,a,b,za,zb = i<<1,b,b+a,zb,zb*za
    while a > Z("0z0"):
      if exponent.value&i:
        power *= zb
      i,a,b,za,zb = i>>1,b-a,a,zb//za,za
    return power
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
  b = Z("0z10010")
  b -= Z("0z100100")
  print(b)
  
  print("Multication")
  c = Z("0z1001")
  c *= Z("0z101")
  print(c)
  c = Z("0z101010")
  c += Z("0z101")
  print(c)
  
  print("Division")
  d = Z(100)
  q = d//Z(7)
  r = d%Z(7)
  print(q,r)
  print(d,q*Z(7)+r)
  
  print("Empower")
  p = Z(6)
  p **= Z(4)  
  print(p)
  return 0

if __name__ == "__main__":
  sys.exit(task(sys.argv))
