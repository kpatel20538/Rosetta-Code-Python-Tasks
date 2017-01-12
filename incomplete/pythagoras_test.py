import tasks.pythagoras

import unittest
import logging

class TestPythagoras(unittest.TestCase):
  def setUp(self):
    """ Test Case Enviroment """
    logging.basicConfig(filename="./logs/pythagoras_test.log",level=logging.DEBUG)
    logging.info('TestPythagoras initialized')
  def test_gather_squares(self):
    """ Test Decription 1 """ 
    logging.info("test_gather_squares()")
    squares,_ = tasks.pythagoras.gather_squares_triangles((1.0,0.0),(0.0,0.0),1)
    measure = sum(x+y for x,y in squares[0])
    self.assertAlmostEqual(measure,4.0)
  def test_gather_triangles(self):
    """ Test Decription 1 """ 
    logging.info("test_gather_triangles()")
    _,triangles = tasks.pythagoras.gather_squares_triangles((1.0,0.0),(0.0,0.0),1)
    measure = sum(x+y for x,y in triangles[0])
    self.assertAlmostEqual(measure,4.0)
if __name__ == '__main__':
  unittest.main()
