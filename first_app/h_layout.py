# Filename: h_layout.py
''' PyQt5 tutorial, cont. from hello.py '''

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QHBoxLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('QHBoxLayout')

window.setGeometry(100, 100, 280, 80)
window.move(60, 15)

layout = QHBoxLayout()  # Create the horizontal layout object
layout.addWidget(QPushButton('Left'))  # Add a button widget with a label
layout.addWidget(QPushButton('Center'))
layout.addWidget(QPushButton('Right'))
window.setLayout(layout)  # Set new layout into the window

window.show()

sys.exit(app.exec_())