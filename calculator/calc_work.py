# Filename: calc_work.py

'''The math end of the calculator app'''

from functools import partial

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (QApplication, 
                              QMainWindow, 
                              QWidget, 
                              QGridLayout, 
                              QLineEdit, 
                              QPushButton, 
                              QVBoxLayout)

class CalculatorWork:
  '''Calculator's CONTROLLER
        doing the math behind the app'''

  def __init__(self, view):
    self.view = view
    self._connectSignals()


  def _buildExpressions(self, sub_exp):
    
    