import functools
import numbers
import re
import sys

@functools.total_ordering
class Z:
  """ Zeckendorf Representation of Integer
  
    Represents an Integer as sum of Fibonacci Numbers.
  
    Zeckendorf Theorem states that every integer can be uniquely
  represented as a sum of nonconsecutive Fibonacci Numbers. 
  The resulting encoding statisfies Brown's Criterion, premitting it to 
  be respresented as a unique bitstring.
  
    For the sake of completeness, this class will rely on the default 
  int and arimethic and relational operators only when type converting 
  [i.e. Z -> int ,int -> Z]. In all other cases, only bitwise operators 
  [^,&,|,~,>>,<<], boolean comparison operators [and,or,not] and the 
  int.bit_length() function will be used when manipulating integers.
  
  
  Attributes:
    sign (bool) : whether the value is positive or negative
    value (int) : positive bitstring in canonical form (see above.)

  References and Sources:
    [1] : Connor Ahlbach, Jeremy Usatine, Nicholas Pippenger
      Efficient Algorithms for Zeckendorf Arithmetic
      arXiv:1207.4497 [cs.DS] : https://arxiv.org/abs/1207.4497
    [2] : N. J. A. Sloane 
      Fibonacci numbers: F(n) = F(n-1) + F(n-2) with F(0) = 0 and F(1) = 1. 
      A000045 : https://oeis.org/A000045  
  """
  
  def __init__(self,param=None):
    """ Constructor
    args:
      param (None|Z|str|Number) : value to be typecast
    raise:
      TypeError : param is can not convert to Z
    """
    if param is None: # Defualt Constructor
      self.sign,self.value = True,0
    elif type(param) == Z: # Copy Constructor
      self.sign,self.value = param.sign,param.value
    elif type(param) == str: # String to Z Type Conversion
      self.sign, self.value = self._from_str(param)
    elif isinstance(param,numbers.Number): # Numeric to Z Type Conversion
      self.sign, self.value = self._from_numeric(param)
    else:
      raise TypeError("Can't Cast to Z, given type {}".format(type(param)))
  def _from_str(self,param):
    """ String to Z type conversion helper
    
    Strips String and Converts to Z
    
    args:
      param (str) : See Constructor.
    return:
      sign (bool) : See Class Attr.
      value (int) : See Class Attr.
    raise:
      ValueError  : Regex Validity Test Failed
    """
    if not re.fullmatch(r"0z0|\-?0z1[01]*",param):
      raise ValueError("Malformed String : {}".format(param))
    sign = param[0] != "-"
    stream = param.split("0z")[-1][::-1]
    value,i = 0,1
    for character in stream:
      if character == "1":
        value |= i
      i <<= 1
    return sign,value
  def _from_numeric(self,param):
    """ Numeric to Z type conversion helper
    
    Truncates to Int and Converts to Z
    
    args:
      param (Numeric) : See Constructor.
    return:
      sign (bool) : See Class Attr.
      value (int) : See Class Attr.
    """
    sign = abs(param) == param
    value,stream = 0,abs(int(param))
    i,a,b = 1,1,1
    while stream >= b:
      i,a,b=i<<1,b,a+b
    while a > 0:
      if stream >= b:
        stream -= b
        value |= i
      i,a,b=i>>1,b-a,a
    return sign,value
  def _from_bitstring(self,sign,bitstring):
    za = Z()
    za.value = self._canonical_form(bitstring)
    za.sign = sign or za == Z("0z0")
    return za
    
  def __int__(self):
    """ Z to int type conversion
    
    return:
      out (int) : sum of fibonacci numbers
    """
    out,i,a,b = 0,1,1,1
    while self.value >= b:
      i,a,b = i<<1,b,b+a
    while a > 0:
      if self.value&i:
        out += b 
      i,a,b = i>>1,b-a,a
    return out if self.sign else -out
  def __float__(self):
    """ Z to int to float conversion """
    return float(int(self))
  def __complex__(self):
    """ Z to int to complex conversion """
    return complex(int(self))
  def __round__(self,n=None):
    """ Returns a copy of self"""
    return +self
  def __repr__(self):
    """ Z to string conversion (compatible with str.format()) """
    return ("0z" if self.sign else "-0z")+bin(self.value)[2:]
  def __hash__(self):
    """ Python hash on int converted self """
    return hash(int(self))
  def __index__(self):
    """ Indicates Z is a valid array/list index """
    return int(self) 
  def __bool__(self):
    """ Z to bool conversion """
    return self != Z("0z0")
  
  def _comparator(self,za,zb):
    """ Compares magnitude and sign of za and zb
    
    A difference mask is constructed to indicate the first (and only)
    bit to check to compare magnitudes, skipping any common bits shared 
    by za and zb. An empty difference mask indicates za and zb are equal
    in magnitude.
    
    Signs are returned as they correpond to the expected result when
    negative numbers are taken into account. 
    
    e.g. Z(-2) > Z(-4) even though Z(2) < Z(4)

    args:
      za,zb (Z) : values to be compared
    returns:
      sign (bool|None) : True if za > zb, False if za < zb, None if za == zb
    """
    if za.sign ^ zb.sign: # Check for sign disagreement (e.g Z(-2) < z(1))
      return za.sign
    difference = za.value ^ zb.value # Construct Xor Mask (approx. za-zb)
    if difference:
      msb = difference.bit_length() 
      # Check if za has a larger magnitude than zb
      return za.sign if za.value&(1<<msb>>1) else not za.sign 
    return None
  
  def _reduce_carry(self,carry,summation):
    """ Helper Function that trys to clear out the carry flag,
    leaving only the summation flag.
    
    A window is passed across the carry and summation bitstrings from 
    most-signifgant-bit to least-signifgant-bit once;it trys to matches
    descructive string replacement rules.
    
    After the pass, the last remaining carry flags located near 
    the least-signifgant-bit are handled
    
    Based on the Algorithm described in [1].Section2 
    args:
      carry (int): noncanoical bitstring reffering to za&zb
      summation (int): noncanoical bitstring reffering to za^zb
    return:
      summation (int): equvialent noncanoical bitstring with 0 carry
    raise:
      AssertError : carry flag was not cleared.
    """
    # Window-Size : 4
    window = 15 << carry.bit_length()
    while window >> 4:
      # Create Windows
      window >>= 1
      position = window.bit_length()
      sum_window = (summation&window) << 4 >> position
      carry_window = (carry&window) << 4 >> position
      # Check if window matches rule
      if (not (carry_window >> 1)^2) and ((not (sum_window >> 1)) or (not (sum_window >> 1)^2)):
        # 020x -> 100x' & 030x -> 110x'
        clear_carry, set_carry, toggle_carry = 4,0,sum_window&1
        clear_sum, set_sum, toggle_sum = 0,8,1
      elif (not (carry_window >> 1)^2) and (not (sum_window >> 1)^1):
        # 021x -> 110x
        clear_carry, set_carry, toggle_carry = 4,0,0
        clear_sum, set_sum, toggle_sum = 2,12,0
      elif (not (carry_window >> 1)^1) and (not (sum_window >> 1)^2):
        # 012x -> 101x
        clear_carry, set_carry, toggle_carry = 2,0,0
        clear_sum, set_sum, toggle_sum = 4,10,0       
      else:
        clear_carry, set_carry, toggle_carry = 0,0,0
        clear_sum, set_sum, toggle_sum = 0,0,0
      # Apply rules 
      carry &= ~(clear_carry << position >> 4)
      carry |=  (set_carry << position >> 4)
      carry ^=  (toggle_carry << position >> 4)
      summation &= ~(clear_sum << position >> 4)
      summation |=  (set_sum << position >> 4)
      summation ^=  (toggle_sum << position >> 4)
    
    # Clean up in rightmost-window
    if carry&3:
      if (not carry&3^1) and ((not summation&3^1) or (not summation&3)):
        # 02 -> 10 & 03 -> 11
        clear_carry,set_carry = 1,0
        clear_sum,set_sum = 0,2
      elif (not carry&7^2) and ((not summation&7^2) or (not summation&7)):
        # 020 -> 101 & 030 -> 111
        clear_carry,set_carry = 2,0
        clear_sum,set_sum = 0,5
      elif (not carry&7^2) and (not summation&7^1):
        # 021 -> 110 *Discovered while debugging*
        clear_carry,set_carry = 2,0
        clear_sum,set_sum = 1,6
      elif (not carry&7^1) and (not summation&7^2):
        # 012 -> 101
        clear_carry,set_carry = 1,0
        clear_sum,set_sum = 2,5
      elif (not carry&15^2) and (not summation&15^4):
        # 0120 -> 1010
        clear_carry,set_carry = 2,0
        clear_sum,set_sum = 4,10
      else:
        clear_carry,set_carry = 0,0
        clear_sum,set_sum = 0,0
      carry &= ~clear_carry
      carry |=  set_carry 
      summation &= ~clear_sum
      summation |=  set_sum
    err_msg = "Carry Flag Failed to Reduce {} {}"
    assert not carry,err_msg.format(bin(carry),bin(summation))
    return summation
  
  def _reduce_difference(self,summation,difference):
    """ Helper Function that trys to clear out the difference flag,
    leaving only the summation and a new carry flag.
        
    A window is passed across the carry, summation, difference bitstrings 
    from most-signifgant-bit to least-signifgant-bit once;it trys to matches
    descructive string replacement rules.
    
    After the pass, the last remaining carry flags located near 
    the least-signifgant-bit are handled
    
    Based on the Algorithm described in [1].Section3
    args:
      summation (int): noncanoical bitstring reffering to za&~zb
      difference (int): noncanoical bitstring reffering to ~za^zb
    return:
      carry (int): noncanoical bitstring than can be combined with summation
      summation (int): equvialent noncanoical bitstring with 0 difference
    raise:
      AssertError : difference flags wasn't cleared properly 
        This error will always be raised when the summation given is 
        less than the difference given.
    """
    carry = 0
    # Window-Size : 3
    window = 7 << summation.bit_length()
    while window >> 3:
      # Create Windows
      window >>= 1
      position = window.bit_length()
      carry_window = (carry&window) << 3 >> position
      sum_window = (summation&window) << 3 >> position
      diff_window = (difference&window) << 3 >> position
      # Check if window matches rule
      clear_carry, set_carry = 0,0
      clear_sum, set_sum, toggle_sum = 0,0,0
      clear_diff = 0
      if ((sum_window&4) or (carry_window&4)) and (not (carry_window&3)):
        # All Rules 2xx -> 1xx & 1xx -> 0xx
        clear_carry,toggle_sum = 4,4
        if (not sum_window&3) and (not diff_window&3):
          # x00 -> x'11
          set_sum = 3
        elif (not sum_window&3) and (not diff_window&3^2):
          # x*0 -> x'01
          set_sum,clear_diff = 1,2
        elif (not sum_window&3^1) and (not diff_window&3^2):
          # x*1 -> x'02
          set_carry,clear_sum,clear_diff = 1,1,2
        elif (not sum_window&3) and (not diff_window&3^1):
          # x0* -> x'10
          set_sum,clear_diff = 2,1
        else:
          # Clear rules if not valid
          clear_carry,toggle_sum = 0,0
      # Apply Rules
      carry &= ~(clear_carry << position >> 3)
      carry |= (set_carry << position >> 3)
      summation &= ~(clear_sum << position >> 3)
      summation |= (set_sum << position >> 3)
      summation ^= (toggle_sum << position >> 3)
      difference &= ~(clear_diff << position >> 3)
    #Cleap up
    if difference&1:
      if carry&2:
        # 02* -> 100
        clear_carry,clear_sum,set_sum,clear_diff = 2,0,4,1
      elif summation&2:
        # x1* -> x01
        clear_carry,clear_sum,set_sum,clear_diff = 0,2,1,1
      else:
        clear_carry,clear_sum,set_sum,clear_diff = 0,0,0,0
      carry &= ~clear_carry
      summation &= ~clear_sum
      summation |= set_sum
      difference &= ~clear_diff
    err_msg = "Difference Flag Failed to Reduce {} {} {}"
    assert not difference,err_msg.format(bin(carry),bin(summation),bin(difference))
    return carry,summation
  
  def _canonical_form(self,summation):
    """ Convert bitstring to equavliant canonical form
    
    args:
      summation : noncanonical bitstring
    return:
      summation : canonical bitstring
    """
    # Parellel check for subsequence "011"
    window = (summation<<1) & summation & (~summation>>1) 
    while window:
      # Toggle subsequences to "100" and repeat
      summation ^= ((window<<1) | window | (window>>1))
      window = (summation)<<1 & summation & (~summation>>1)
    return summation
  
  # Zeckendorf's Arithmetic
  def __lt__(self,other):
    """ Employs Z._comparator to determine relation """
    if type(other) is not Z:
      raise TypeError("Must be type Z . Given Type {}".format(type(other)))
    comp = self._comparator(self,other)
    return False if comp is None else not comp 
  def __eq__(self,other):
    """ Employs Z._comparator to determine equality """
    if type(other) is not Z:
      raise TypeError("Must be type Z . Given Type {}".format(type(other)))
    comp = self._comparator(self,other)
    return comp is None
  def __add__(self, other):
    """ Zeckendorf Signed Addition and Unsigned Addition 
    
    Depending on the signs of the operands, the underlying values are
    combined into carry, summation, and difference flags.
    
    These flags are then simplified into equivalent flags, reducing carry
    and difference flags to 0. Leaving only the summation flag to 
    represent the value of the result.
    
    raise:
      TypeError : other is not of type Z
    """
    if type(other) is not Z:
      raise TypeError("Must be type Z . Given Type {}".format(type(other)))
    signed_addition = self.sign ^ other.sign
    za,zb = abs(self),abs(other) # Preventing Accidental Modication of self/other
    sign_res = self.sign
    if signed_addition:
      if za == zb:
        return Z("0z0")
      elif zb > za: 
        sign_res = other.sign
        za,zb = zb,za
      # Element By Element Difference
      summation = za.value & (~zb.value)
      difference = (~za.value) & zb.value
      # Z._reduce_difference() will raise AssertError if difference > summation
      carry,summation = self._reduce_difference(summation,difference)
    else:
      # Element By Element Summation
      carry = za.value & zb.value
      summation = za.value ^ zb.value
    summation = self._reduce_carry(carry,summation)
    return self._from_bitstring(sign_res,summation)
  def __sub__(self, other):
    """ Subtraction as Signed Addition"""
    return self + (-other)
  def __mul__(self, other):
    """ Repeated Addition of Fibonacchi Multiples of the multiplier. """
    res_sign = not (self.sign ^ other.sign)
    product,multiplier,multiplicand = Z("0z0"),abs(other),abs(self)
    i,a,b,za,zb = 1,Z("0z1"),Z("0z1"),multiplicand,multiplicand
    while multiplier > b:
      i,a,b,za,zb = i<<1,b,b+a,zb,zb+za
    while a > Z("0z0"):
      if multiplier.value&i:
        product += zb
      i,a,b,za,zb = i>>1,b-a,a,zb-za,za
    return +product if res_sign else -product
  def __divmod__(self, other):
    """ Repeated Subtraction of Fibonacchi Multiples of the divisor.
    return:
      quotient (Z) : Rounded towards 0
      remainder (Z)
    """
    res_sign = not (self.sign ^ other.sign)
    quotient,remainder,divisor = Z("0z0"),abs(self),abs(other)
    a,b,za,zb = Z("0z1"),Z("0z1"),divisor,divisor    
    while remainder > zb:
      a,b,za,zb = b,b+a,zb,zb+za
    while remainder >= divisor:
      if remainder >= zb:
        quotient += b
        remainder -= zb
      a,b,za,zb = b-a,a,zb-za,za
    if res_sign:
      return +quotient,+remainder
    else:
      return -quotient,remainder-abs(other) 
  def __floordiv__(self, other):
    """ Quotient from divmod with self and other"""
    q,_ = divmod(self,other)
    return q
  def __mod__(self, other):
    """ Remainder from divmod with self and other"""
    _,r = divmod(self,other)
    return r
  def __pow__(self, other, modulo=None):
    """ Repeated Multiplication of Fibonacchi Powers of the base. """
    if other < Z("0z0") or (other == Z("0z0") and self == Z("0z0")):
      raise ValueError("Negative Power or 0^0 detected")
    res_sign = (abs(other)%Z("0z10") == Z("0z1")) or self.sign
    power,base,exponent = Z("0z1"),abs(self),abs(other)
    i,a,b,za,zb = 1,Z("0z1"),Z("0z1"),base,base
    while exponent > b:
      i,a,b,za,zb = i<<1,b,b+a,zb,zb*za
    while a > Z("0z0"):
      if exponent.value&i:
        power *= zb
      i,a,b,za,zb = i>>1,b-a,a,zb//za,za
    return +power if res_sign else -power
  def __neg__(self):
    """ Calls _from_bitstring() on self to invert sign """
    return self._from_bitstring(not self.sign,self.value)
  def __pos__(self):
    """ Calls _from_bitstring() on self """
    return self._from_bitstring(self.sign,self.value)
  def __abs__(self):
    """ Calls _from_bitstring() on self to turn positive"""
    return self._from_bitstring(True,self.value)

def task(argv):
  """ Implement Zeckendorf's Arithmetic for addition, subtraction,
  muliplaction, and division.
  """
  print("=Addition=")
  # 38 + 23 = 61
  a = Z("0z10000101")
  b = Z("0z1000010")
  c = a + b # Z("0z100001001")
  print("{} + {} = {}".format(a,b,c)) 
  print("{} + {} = {}\n".format(int(a),int(b),int(c)))

  print("=Subtraction=")
  # 37 - 48 = -11
  a = Z("0z10000100")
  b = Z("0z10100001")
  c = a - b # Z("-0z10100")
  print("{} - {} = {}".format(a,b,c)) 
  print("{} - {} = {}\n".format(int(a),int(b),int(c)))
  
  print("=Multication=")
  # 17 * -11 = -187
  a = Z("0z100101")
  b = Z("-0z10100")
  c = a * b # Z("-0z10010010001")
  print("{} * {} = {}".format(a,b,c)) 
  print("{} * {} = {}\n".format(int(a),int(b),int(c)))
  
  print("=Division=")
  # 100 // 7 = 14
  # 100 % 7 = 2
  a = Z("0z1000010100")
  b = Z("0z1010")
  q = a // b  # Z("0z100001")
  r = a % b # Z("0z10")
  print("{} // {} = {}".format(a,b,q))
  print("{} // {} = {}".format(int(a),int(b),int(q)))
  print("{} % {} = {}".format(a,b,r)) 
  print("{} % {} = {}\n".format(int(a),int(b),int(r)))
  return 0

if __name__ == "__main__":
  sys.exit(task(sys.argv))
