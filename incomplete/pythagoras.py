import sys

def gather_squares_triangles(p1,p2,depth)
  """ Draw Square and Right Triangle given 2 points, 
  Recurse on new points
  
  args:
    p1,p2 (float,float) : absolute position on base vertices
    depth (int) : decrementing counter that terminates recursion
  return:
    squares [(float,float,float,float)...] : absolute positions of 
      vertices of squares
    triangles [(float,float,float)...] : absolute positions of 
      vertices of right triangles
  """
  if depth == 0:
    return [],[]
  
  pd = (p2[0] - p1[0]),(p1[1] - p2[1]) 
  p3 = (p2[0] - pd[1]),(p2[1] - pd[0])
  p4 = (p1[0] - pd[1]),(p1[1] - pd[0])
  p5 = (p4[0] + (pd[0] - pd[1])/2),(p4[1] - (pd[0] + pd[1])/2)
  
  squares_left,triangles_left = gather_squares_triangles(p4,p5,depth-1)
  squares_right,triangles_right = gather_squares_triangles(p5,p3,depth-1)

  squares = [[p1,p2,p3,p4]]+squares_left+squares_right
  triangles = [[p3,p4,p5]]+triangles_left+triangles_right
  return squares,triangles

def task(argv):
  """ Draw a Depth-7 Pytagoras Tree without the use of Trig Functions """
  # Init Canvas
  # Collect Vertices for squares and right triangles
  # Draw Points
  # Commit Canvas
  return 0
  
if __name__ == "__main__":
  sys.exit(task(sys.argv))
