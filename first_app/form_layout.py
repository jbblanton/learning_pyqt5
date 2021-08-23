# Filename: form_layout.py
''' PyQt5 tutorial, cont. from grid_layout.py '''

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QFormLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('QFormLayout')
# Arranges widgets in a 2-column layout
#   First column typically contains labels
#   Second column contains QLineEdit, QComboBox, QSpinBox, etc.

window.setGeometry(100, 100, 280, 80)
window.move(60, 15)

layout = QFormLayout()
layout.addRow('Name:', QLineEdit())
# addRow() auto creates 2 boxes -one for label, one for input
layout.addRow('Pet Type:', QLineEdit())
layout.addRow('Pet Name:', QLineEdit())

window.setLayout(layout)

window.show()

sys.exit(app.exec_())