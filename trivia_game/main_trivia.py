# Filename: trivia_game.py

'''PyQt5-based app. 
    Based on the video tutorial found here
    - https://youtu.be/9iZLDnW_vwU
    - "Create GUI App with PyQt5 - PART 1" by Python Simplified
'''


import sys

from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QVBoxLayout, QWidget, QFileDialog, QGridLayout
from PyQt5.QtGui import QCursor, QPixmap
from PyQt5 import QtGui, QtCore

from trivia_logic import frame1, frame2, grid, winning_frame, losing_frame


game = QApplication(sys.argv)


# class TriviaGameUI(QMainWindow):

    # def __init__(self):
    #     super().__init__()
    #     self.setWindowTitle('Who Wants to be a Programmer?')
    #     self.setFixedWidth(1000)
    #     #window.move(700, 200)

    #     self.grid = QGridLayout()
    #     self.window = QWidget(self)
    #     self.setCentralWidget(self.window)
    #     self.window.setLayout(self.grid)
    #     self.setStyleSheet('background: #271d2e;') 

# def main():
    # Initialize the app
    
    #window = TriviaGameUI()

    # TODO - Make this a class to be consistent!
window = QWidget()
window.setWindowTitle('Who Wants to be a Programmer?')
window.setFixedWidth(1000)
    #window.move(700, 200)
window.setStyleSheet('background: #271d2e;') 



window.setLayout(grid)

window.show()
    #play = Frame1()





frame1()
sys.exit(game.exec_()) # Exit the app


# if __name__ == '__main__':
#     main()