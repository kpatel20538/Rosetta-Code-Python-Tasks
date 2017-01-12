import tasks.task_template

import unittest
import logging

class TestTemplate(unittest.TestCase):
  def setUp(self):
    """ Test Case Enviroment """
    logging.basicConfig(filename="template_test.log",level=logging.DEBUG)
    logging.info('TestTemplate initialized')
  def test_truth(self):
    """ Test Decription 1 """ 
    logging.info("Establishing Truth")
    self.assertTrue(True)
  def test_equality(self):
    """ Test Decription 2 """ 
    logging.info("Establishing Equality")
    self.assertEqual(1,1)

if __name__ == '__main__':
  unittest.main()
