# Filename: signals.py

''' Signals & slots '''

import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QLabel
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QWidget

import functools


# Create a slot, to be used later
def greeting(who):
  '''Slot function'''

  if msg.text():
    msg.setText('')
  else:
    msg.setText(f'Hello {who}!')


# Now create the app, including the signal-emitter (button)
app = QApplication(sys.argv)

window = QWidget()
window.setWindowTitle('Signals & Slots')
layout = QVBoxLayout()

btn = QPushButton('Say hello')
# btn.clicked.connect(greeting)  # Connect clicking btn to greeting()
btn.clicked.connect(functools.partial(greeting, 'World')) # Can pass args


layout.addWidget(btn)
msg = QLabel('')
layout.addWidget(msg)
window.setLayout(layout)
window.show()
sys.exit(app.exec_())

