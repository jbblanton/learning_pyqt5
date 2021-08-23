# Filename: grid_layout.py
''' PyQt5 tutorial, cont. from v_layout.py '''

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QWidget

app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('QGridLayout')

window.setGeometry(100, 100, 280, 80)
window.move(60, 15)

layout = QGridLayout()
layout.addWidget(QPushButton('Top Left'), 0, 0)
# 2nd & 3rd args: integers that define each button's position
layout.addWidget(QPushButton('Top Middle'), 0, 1)
layout.addWidget(QPushButton('Top Right'), 0, 2)

layout.addWidget(QPushButton('Middle Left'), 1, 0)
layout.addWidget(QPushButton('2 row tall button'), 1, 1, 2, 1)
# 4th arg: rowSpan
# 5th arg: columnSpan
# Used to make a widget occupy more than one row or column
layout.addWidget(QPushButton('Middle Right'), 1, 2)

layout.addWidget(QPushButton('Bottom Left'), 2, 0)
layout.addWidget(QPushButton('Bottom Right'), 2, 2)

layout.addWidget(QPushButton('3 column button'), 3, 0, 1, 3)
# 4th arg: rowSpan
# 5th arg: columnSpan
# Used to make a widget occupy more than one row or column


window.setLayout(layout)

window.show()

sys.exit(app.exec_())