# Filename: calculator.py

'''A simple calculator made with PyQt5
      Using the M-V-C approach '''

# Guide:  https://realpython.com/python-pyqt-gui-calculator/


import sys

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, 
                              QMainWindow, 
                              QWidget, 
                              QGridLayout, 
                              QLineEdit, 
                              QPushButton, 
                              QVBoxLayout)

from calc_work import *
from calc_math import *


class CalculatorUI(QMainWindow):
  '''Calculator's VIEW'''

  def __init__(self):
    super().__init__()
    self.setWindowTitle('Calculate It!')
    self.setFixedSize(435, 435)  # setFixedSize stops a user from resizing

    self.gen_layout = QVBoxLayout()
    self._centralWidget = QWidget(self)
    self.setCentralWidget(self._centralWidget)  # Parent for everything else
    self._centralWidget.setLayout(self.gen_layout)

    self._createDisplay()
    self._createButtons()


  def _createDisplay(self):
    '''See the inputs & calculations'''

    self.display = QLineEdit()

    self.display.setFixedHeight(50)
    self.display.setAlignment(Qt.AlignRight)
    self.display.setReadOnly(True)

    self.gen_layout.addWidget(self.display)


  def _createButtons(self):
    '''A grid of buttons'''

    self.buttons = {}
    btns_layout = QGridLayout()

    buttons = {'7': (0, 0),
               '8': (0, 1),
               '9': (0, 2),
               '/': (0, 3),
               'C': (0, 4),
               '4': (1, 0),
               '5': (1, 1),
               '6': (1, 2),
               '*': (1, 3),
               '(': (1, 4),
               '1': (2, 0),
               '2': (2, 1),
               '3': (2, 2),
               '-': (2, 3),
               ')': (2, 4),
               '0': (3, 0),
               '00': (3, 1),
               '.': (3, 2),
               '+': (3, 3),
               '=': (3, 4),
              }

    for btnText, pos in buttons.items():
      self.buttons[btnText] = QPushButton(btnText)
      self.buttons[btnText].setFixedSize(45, 45)
      btns_layout.addWidget(self.buttons[btnText], pos[0], pos[1])

    self.gen_layout.addLayout(btns_layout)


  def setDisplayText(self, text):
    self.display.setText(text)
    self.display.setFocus()


  def displayText(self):
    return self.display.text()


  def clearDisplay(self):
    self.setDisplayText('')


def main():
  '''Main function'''

  # Make the calculator object
  calc = QApplication(sys.argv)
  view = CalculatorUI()

  # Show it
  view.show()

  model = evaluateExpression
  CalculatorWork(model=model, view=view)  
  # Pass the ability to do math and the calculator gui to the controller

  sys.exit(calc.exec_())


if __name__ == '__main__':
  main()