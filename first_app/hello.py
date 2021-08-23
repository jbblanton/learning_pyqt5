# Filename: hello.py
''' PyQt5 Tutorial from realpython.com/python-pyqt-gui-calculator '''

import sys  # Allows for exiting the app

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QWidget

app = QApplication(sys.argv)  # Create an application instance; 
#   Pass sys.argv to allow the app to handle command line arguments
#   If the app will NOT allow command line args, pass an empty list

window = QWidget()
window.setWindowTitle('First PyQt5 App')  # Shown in the top bar
window.setGeometry(100, 100, 280, 80)  # Define placement & size of window
#                   x, y, width, height
window.move(60, 15)
helloMsg = QLabel('<h1>Hello World!</h1>', parent=window)
# A widget without a window is a parent / main window
# A widget with a window is shown within the parent
# Parentage prevents memory leaks; children will be deleted along with parent
helloMsg.move(60, 15)  # Msg placement within window

window.show()  # This schedules the paint event

sys.exit(app.exec_())