import tasks.zeckendorf

import unittest
import logging

class TestZeckendorf(unittest.TestCase):
  def setUp(self):
    """ Test Case Enviroment """
    logging.basicConfig(filename="./logs/zeckendorf_test.log",level=logging.DEBUG)
    logging.info('TestZeckendorf initialized')
  def test_addition(self):
    """ Zeckendorf Addition """ 
    a = tasks.zeckendorf.Z("0z10000101")
    b = tasks.zeckendorf.Z("0z1000010")
    c = a + b
    d = tasks.zeckendorf.Z("0z100001001")
    logging.info("{} + {} = {} == {}".format(a,b,c,d))
    self.assertEqual(c,d)
  def test_subtraction(self):
    """ Zeckendorf Subtraction """ 
    a = tasks.zeckendorf.Z("0z10000100")
    b = tasks.zeckendorf.Z("0z10100001")
    c = a - b
    d = tasks.zeckendorf.Z("-0z10100")
    logging.info("{} - {} = {} == {}".format(a,b,c,d))
    self.assertEqual(c,d)
  def test_multiplication(self):
    """ Zeckendorf Multplication """ 
    a = tasks.zeckendorf.Z("0z100101")
    b = tasks.zeckendorf.Z("-0z10100")
    c = a * b
    d = tasks.zeckendorf.Z("-0z10010010001")
    logging.info("{} * {} = {} == {}".format(a,b,c,d))
    self.assertEqual(c,d)
  def test_division(self):
    """ Zeckendorf Division """ 
    a = tasks.zeckendorf.Z("0z10000100")
    b = tasks.zeckendorf.Z("0z101001")
    q,r = divmod(a,b)
    logging.info("{} / {} = {} r {}".format(a,b,q,r))
    logging.info("{} * {} + {} == {}".format(q,b,r,a)) 
    self.assertEqual(q*b+r,a)
  def test_power(self):
    """ Zeckendorf Exponentiation """ 
    a = tasks.zeckendorf.Z(6)
    b = tasks.zeckendorf.Z(4)
    c = a ** b
    d = tasks.zeckendorf.Z(6**4)
    logging.info("{} ^ {} = {} == {}".format(a,b,c,d))
    self.assertEqual(c,d)
  def test_greater_than(self):
    """ Zeckendorf Comparison """ 
    a = tasks.zeckendorf.Z("0z10010101")
    b = tasks.zeckendorf.Z("0z101010")
    logging.info("{} > {}".format(a,b))
    self.assertTrue(a > b)
  def test_absolute(self):
    """ Zeckendorf Magnitude """ 
    a = tasks.zeckendorf.Z("-0z10101001")
    b = abs(a)
    logging.info("|{}| = {}".format(a,b))
    self.assertNotEqual(a,b)
  def test_value(self):
    """ Zeckendorf to Base10 """ 
    a = tasks.zeckendorf.Z("-0z1001")
    logging.info("|{}| = {}".format(a,int(a)))
    self.assertEqual(int(a),-6)

if __name__ == '__main__':
  unittest.main()
