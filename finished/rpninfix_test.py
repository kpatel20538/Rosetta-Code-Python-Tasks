import tasks.rpninfix

import unittest
import logging

class TestRpnInfix(unittest.TestCase):
  def setUp(self):
    """ Test Case Enviroment """
    logging.basicConfig(filename="./logs/rpninfix_test.log",level=logging.DEBUG)
    logging.info('TestRpnInfix initialized')
  def test_left_assoc(self):
    """ Testing Left Associativity """ 
    logging.info("test_left_assoc()")
    rpn = "3 4 5 - *"
    infix = tasks.rpninfix.rpn_to_infix(rpn)
    self.assertEqual(infix,"3 * ( 4 - 5 )")
  def test_right_assoc(self):
    """ Testing Right Associativity """ 
    logging.info("test_right_assoc()")
    rpn = "5 6 ^ 7 ^"
    infix = tasks.rpninfix.rpn_to_infix(rpn)
    self.assertEqual(infix,"( 5 ^ 6 ) ^ 7")

if __name__ == '__main__':
  unittest.main()
