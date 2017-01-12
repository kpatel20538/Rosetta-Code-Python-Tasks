from PIL import Image, ImageDraw
import sys

def gather_squares_triangles(p1,p2,depth):
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
  # Break Recursion if depth is met
  if depth == 0:
    return [],[]
  
  # Generate Points 
  pd = (p2[0] - p1[0]),(p1[1] - p2[1]) 
  p3 = (p2[0] - pd[1]),(p2[1] - pd[0])
  p4 = (p1[0] - pd[1]),(p1[1] - pd[0])
  p5 = (p4[0] + (pd[0] - pd[1])/2),(p4[1] - (pd[0] + pd[1])/2)
  
  # Gather Points further down the tree
  squares_left,triangles_left = gather_squares_triangles(p4,p5,depth-1)
  squares_right,triangles_right = gather_squares_triangles(p5,p3,depth-1)
  
  # Merge and Return
  squares = [[p1,p2,p3,p4]]+squares_left+squares_right
  triangles = [[p3,p4,p5]]+triangles_left+triangles_right
  return squares,triangles

def task(argv):
  """ Draw a Depth-7 Pytagoras Tree without the use of Trig Functions """
  # Init Canvas
  width,height = 800,500
  img = Image.new("RGBA",(width,height),(0,0,0))
  draw = ImageDraw.Draw(img)

  # Collect and Draw Vertices for squares and right triangles
  p1,p2 = (width/2.3, height),(width/1.8, height)
  squares,triangles = gather_squares_triangles(p1,p2,7)
  for i in range(len(squares)):
    square_color = (int(256*(1-i/len(squares))),0,0)
    triangle_color = (0,0,int(256*(1-i/len(triangles))))
    draw.polygon(squares[i],fill=square_color,outline=(256,0,0))
    draw.polygon(triangles[i],fill=triangle_color,outline=(0,0,256))
  
  # Commit Canvas
  img.save("./out/pythagoras.png","PNG")
  return 0
  
if __name__ == "__main__":
  sys.exit(task(sys.argv))
