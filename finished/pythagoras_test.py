import tasks.pythagoras

import unittest
import logging

class TestPythagoras(unittest.TestCase):
  def setUp(self):
    """ Test Case Enviroment """
    logging.basicConfig(filename="./logs/pythagoras_test.log",level=logging.DEBUG)
    logging.info('TestPythagoras initialized')
  def test_gather_squares(self):
    """ Indirect measure the accuracy of squares generation """ 
    logging.info("test_gather_squares()")
    squares,_ = tasks.pythagoras.gather_squares_triangles((1.0,0.0),(0.0,0.0),1)
    logging.info("Point of Square : {}".format(squares[0]))
    measure = sum(x+y for x,y in squares[0])
    self.assertAlmostEqual(measure,4.0)
  def test_gather_triangles(self):
    """ Indirect measure the accuracy of triangle generation """ 
    logging.info("test_gather_triangles()")
    _,triangles = tasks.pythagoras.gather_squares_triangles((1.0,0.0),(0.0,0.0),1)
    logging.info("Point of Triangle : {}".format(triangles[0]))
    measure = sum(x+y for x,y in triangles[0])
    self.assertAlmostEqual(measure,5.0)
  def test_gather_size(self):
    """ Direct measure of the ammount of shapes generated """
    logging.info("test_gather_size()")
    sizes = []
    p1,p2 = (1.0,0.0),(0.0,0.0)
    for i in range(5):
      squares,_ = tasks.pythagoras.gather_squares_triangles(p1,p2,i)
      logging.info("Squares made with Depth {} : {}".format(i,squares))
      sizes.append(len(squares))
    self.assertListEqual(sizes,[0,1,3,7,15])
if __name__ == '__main__':
  unittest.main()
