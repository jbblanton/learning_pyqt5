# Filename: calc_work.py

'''The functional end of the calculator app'''

from functools import partial


class CalculatorWork:
  '''Calculator's CONTROLLER
        making the buttons clickable 
        and the text visable'''

  def __init__(self, model, view):
    self._evaluate = model
    self._view = view
    self._connectSignals()


  def _connectSignals(self):
    '''Connect the button signals with display slots'''

    for btnText, btn in self._view.buttons.items():
      if btnText not in {'=', 'C'}:
        btn.clicked.connect(partial(self._buildExpressions, btnText))

    self._view.buttons['C'].clicked.connect(self._view.clearDisplay)
    self._view.buttons['='].clicked.connect(self._evaluateExpressions)
    self._view.display.returnPressed.connect(self._evaluateExpressions)


  def _buildExpressions(self, sub_exp):
    '''Display the clicked buttons'''

    if self._view.displayText() == 'ERROR':
      self._view.clearDisplay()

    expression = self._view.displayText() + sub_exp
    self._view.setDisplayText(expression)


  def _evaluateExpressions(self):
    '''Do the math, display results'''

    result = self._evaluate(expression=self._view.displayText())
    self._view.setDisplayText(result)
  
    