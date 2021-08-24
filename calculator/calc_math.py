# Filename: calc_math.py

''' The math end of the calculator app '''

'''Calculator's MODEL'''


ERROR_MSG = 'ERROR'

def evaluateExpression(expression):
  print(expression)
  try:
# TODO: Rewrite this to be better!
    result = str(eval(expression, {}, {}))
  except Exception:
    result = ERROR_MSG

  return result