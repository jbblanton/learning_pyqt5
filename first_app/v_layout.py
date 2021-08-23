# Filename: v_layout.py
''' PyQt5 tutorial, cont. from h_layout.py '''

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('QVBoxLayout')  # Same as before, but now vertical

window.setGeometry(100, 100, 280, 80)
window.move(60, 15)

layout = QVBoxLayout()  # Create the vertical layout object
layout.addWidget(QPushButton('Top'))  # Add a button widget with a label
layout.addWidget(QPushButton('Middle'))
layout.addWidget(QPushButton('Bottom'))
window.setLayout(layout)  # Set new layout into the window

window.show()

sys.exit(app.exec_())