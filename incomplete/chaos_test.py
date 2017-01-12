import tasks.chaos

import unittest
import logging

class TestChaos(unittest.TestCase):
  def setUp(self):
    """ Test Case Enviroment """
    logging.basicConfig(filename="./logs/chaos_test.log",level=logging.DEBUG)
    logging.info('TestChaos initialized')
  def test_point_in_triangle(self):
    """ Testing if random point is bounded by triangle  """ 
    logging.info("test_point_in_triangle()")
    p0,p1,p2 = (0.0,0.0),(1.0,0.0),(0.0,1.0)
    logging.info("Generating Point in Region: [{},{},{}]".format(p0,p1,p2))
    xr,yr = tasks.chaos.random_point_triangle(p0,p1,p2)
    logging.info("Random Point Generated: ({},{})".format(xr,yr))
    self.assertLessEqual(xr+yr,1)
  def test_chaos_game(self):
    """ Testing if chaos_game changes current position properly """
    logging.info("test_chaos_game()")
    staring_point = (16.0,0.0)
    reference_points = [(0.0,0.0)]
    logging.info("Referneces @ {}, Starting @ {} ".format(reference_points,staring_point))
    generated_points = tasks.chaos.rasterize(tasks.chaos.chaos_game(reference_points,staring_point,timeout = 3))
    logging.info("Points Generated: {}".format(generated_points))
    self.assertListEqual(generated_points,[(16,0),(8,0),(4,0),(2,0)])
  def test_rasterize(self):
    """ Testing if rasterize rounds numbers cleanly"""
    logging.info("test_rasterize()")
    points = [(1.9,3.9),(1.1,3.9),(1.9,3.2),(1.5,3.5)]
    logging.info("Rasterizing Points: {}".format(points))
    rastered = tasks.chaos.rasterize(points)
    logging.info("Post Rasterized Points: {}".format(rastered))
    self.assertListEqual(rastered,[(2,4),(1,4),(2,3),(2,4)])
if __name__ == '__main__':
  unittest.main()
