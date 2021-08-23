# Filename: main_window.py
''' PyQt5 tutorial, learning main windows '''

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QStatusBar
from PyQt5.QtWidgets import QToolBar


class Window(QMainWindow):
  '''Create a Main Window, inheriting from QMainWindow'''

  def __init__(self, parent=None):
    '''Initializer'''
    super().__init__(parent)

    self.setWindowTitle('QMainWindow demo')
    self.setGeometry(200, 300, 280, 200)
    self.move(400, 400)

    self.setCentralWidget(QLabel('Here is the required central widget!'))
    # QLabel == CentralWidget
    #   "You can’t create a main window without first setting a central widget. You must have a central widget, even if it’s just a placeholder. When this is the case, you can use a QWidget object as your central widget. You can set the main window’s central widget with .setCentralWidget(). The main window’s layout will allow you to have only one central widget, but it can be a single or a composite widget." -https://realpython.com/python-pyqt-gui-calculator/

    self._createMenu() # At top of window, holds main menu
    self._createToolBar() # On sides, hold tool buttons and widgets
    self._createStatusBar() # At bottom of window, shows general app status


  def _createMenu(self):
    self.menu = self.menuBar().addMenu('&Menu')
    self.menu.addAction('&Exit', self.close)

  def _createToolBar(self):
    tools = QToolBar()
    self.addToolBar(tools)
    tools.addAction('Exit', self.close)

  def _createStatusBar(self):
    status = QStatusBar()
    status.showMessage('This is a status bar')
    self.setStatusBar(status)


if __name__ == '__main__':
  app = QApplication(sys.argv)
  win = Window()
  win.show()
  sys.exit(app.exec_())
