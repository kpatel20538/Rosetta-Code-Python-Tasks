from PIL import Image, ImageDraw, ImageColor

import math
import random
import sys

def random_point_triangle(p0,p1,p2):
  """ Uniformally Picks a point in a triangle 
  
  args:
    p0,p1,p2 (float,float) : absolute position of triangle vertex
  return:
    pr (float,float) : absolute position inside triangle
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
  # Calculating Associated Point
  xr = a0*(x1-x0)+a1*(x2-x0)+x0
  yr = a0*(y1-y0)+a1*(y2-y0)+y0
  return (xr,yr)
  
def chaos_game(reference_point,starting_point,timeout=10000):
  """ Generates points with a chaotic procedure
  
  args:
    reference_point [(float,float)...] : absolute positions
    starting_point  (float,float) : absolute positions
  kwargs:
    timeout (int) : iteration count for procedure
  return:
    generated_points [(float,float)...] : absolute positions
  """
  xi,yi = starting_point
  generated_points = [starting_point]
  for _ in range(timeout):
    # Pick Reference Point and compute midpoint with Current Point
    xj,yj = random.choice(reference_point)
    xi,yi = (xi+xj)/2,(yi+yj)/2
    generated_points.append((xi,yi))
  return generated_points

def task(argv):
  """ Task Description """
  # Initialize Canvas
  img = Image.new("RGBA",(800,600),ImageColor.getrgb("#FFFFFF"))
  draw = ImageDraw.Draw(img)
  
  # Playing Chaos Game in an Equilateral Triangle
  reference_points = [(100,550),(700,550),(400,550-300*math.sqrt(3))]
  starting_point = random_point_triangle(*reference_points)
  generated_points = chaos_game(reference_points,starting_point)
  
  # Draw Generated Points and Boundary Lines
  draw.point(generated_points,fill=ImageColor.getrgb("#FF0000"))
  draw.polygon(reference_points,outline=ImageColor.getrgb("#000000"))

  # Commit Canvas
  img.save("./out/chaos.png","PNG")
  return 0
  
if __name__ == "__main__":
  sys.exit(task(sys.argv))
