import math
import random
import sys

def random_point_triangle(p0,p1,p2):
  """ Uniformally Picks a point in a triangle 
  
  args:
    p0,p1,p2 (int,int) : absolute position of triangle vertex
  return:
    pr (int,int) : absolute position inside triangle
  """
  # Unwraping Points
  x0,y0 = p0
  x1,y1 = p1
  x2,y2 = p2
  # Picking and Adjusting Uniform Weights
  a0 = random.random()
  a1 = random.random()
  if a0+a1 > 1:
    a0, a1 = 1-a0, 1-a1
  xr = a0*(x1-x0)+a1*(x2-x0)+x0
  yr = a0*(y1-y0)+a1*(y2-y0)+y0
  return (xr,yr)
  
def chaos_game(reference_point,starting_point,timeout=10000):
  """ Generates points with a chaotic procedure
  
  args:
    reference_point [(int,int)...] : absolute positions
    starting_point  (int,int) : absolute positions
  kwargs:
    timeout (int) : iteration count for procedure
  return:
    generated_points [(int,int)...] : absolute positions
  """
  pass


def task(argv):
  """ Task Description """
  # Initialize Canvas
  # Calculate Location of Reference Points (Equilateral Triangle)
  # Pick a random point in bounded by the Reference Points
  # Loop Chaotic Procedure until timeout
  # Draw Generated Points and Boundary Lines
  # Commit Canvas
  return 0
  
if __name__ == "__main__":
  sys.exit(task(sys.argv))
