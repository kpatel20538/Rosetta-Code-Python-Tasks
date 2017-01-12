import sys

OPERATIONS = {
  "^": (4, True),
  "*": (3, False),
  "/": (3, False),
  "+": (2, False),
  "-": (2, False)
}

def rpn_to_infix(rpn):
  """ Converts Rpn String to Infix String 
  args:
    rpn (str): reverse polish notation formatted string
  return:
    infix (str): infix notation formatted string
  """
  stack = []
  # Tokenize input and iterate 
  for token in rpn.split(" "):
    if token in OPERATIONS.keys():
      # Operator Case:
      # Pop Left and Right Operands off stack and unwrap
      prec_right, infix_right = stack.pop()
      prec_left, infix_left = stack.pop()

      # Unwrap Operator Info
      op_prec, op_right_assoc = OPERATIONS[token]

      # Deterimine if bracing is needed
      brace_left = prec_left < op_prec or (prec_left == op_prec and op_right_assoc)
      brace_right = prec_right < op_prec or (prec_right == op_prec and not op_right_assoc)

      # Constructing new expression string with ternary expressions
      infix = "( "+infix_left+" )" if brace_left else infix_left
      infix += " " + token + " "
      infix += "( "+infix_right+" )" if brace_right else infix_right

      # Wrap and Push precedence and expression to the stack
      stack.append((op_prec, infix))
    else:
      # Base Case:
      # Wrap and Push default precedence and token
      stack.append((9, token))
  # The stack should have one element, Unwrap it to retrieve the
  # completed infix expression
  _, infix = stack[0]
  return infix
  

def task(argv):
  """ Parse a rpn strings and return their corresponding infix strings """
  rpns = ["3 4 2 * 1 5 - 2 3 ^ ^ / +","1 2 + 3 4 + ^ 5 6 + ^"]
  for rpn in rpns:
    infix = rpn_to_infix(rpn)
    print(rpn)
    print(infix)
  return 0
  
if __name__ == "__main__":
  sys.exit(task(sys.argv))
