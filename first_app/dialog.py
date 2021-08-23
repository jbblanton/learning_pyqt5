# Filename: dialog.py
''' PyQt5 tutorial, learning dialogs '''

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QDialog
from PyQt5.QtWidgets import QDialogButtonBox
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QVBoxLayout


class Dialog(QDialog):
  '''Make a Dialog class, which inherits from QDialog'''

  def __init__(self, parent=None):
    '''Initializer'''
    super().__init__(parent)

    self.setWindowTitle('QDialog demo')
    dialogLayout = QVBoxLayout()
    
    formLayout = QFormLayout()
    formLayout.addRow('Name', QLineEdit())
    formLayout.addRow('Pets', QLineEdit())
    formLayout.addRow('Favorite Season', QLineEdit())

    dialogLayout.addLayout(formLayout)
    # Layouts can be nested! 
    #   Call .addLayout() on the container, and pass the nested layout

    btns = QDialogButtonBox()
    btns.setStandardButtons(QDialogButtonBox.Cancel | QDialogButtonBox.Ok)
    dialogLayout.addWidget(btns)
    
    self.setLayout(dialogLayout)


if __name__ == '__main__':
  app = QApplication(sys.argv)
  dlg = Dialog()
  dlg.show()
  sys.exit(app.exec_())