import sys

def rpn_to_infix(rpn):
  """ Converts Rpn String to Infix String 
  args:
    rpn (str): reverse polish notation formatted string
  return:
    infix (str): infix notation formatted string
  """
  pass

def task(argv):
  """ Parse a rpn strings and return their corresponding 
  infix strings
  """
  rpns = ["3 4 2 * 1 5 - 2 3 ^ ^ / +","1 2 + 3 4 + ^ 5 6 + ^"]
  for rpn in rpns:
    infix = rpn_to_infix(rpn)
    print(rpn)
    print(infix)
  return 0
  
if __name__ == "__main__":
  sys.exit(task(sys.argv))
