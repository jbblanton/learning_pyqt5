# Filename: hiding_hippos.py

'''PyQt5-based single-player game 
    Based on the tutorial found here 
      - https://www.pythonguis.com/examples/python-minesweeper/
      - https://github.com/pythonguis/15-minute-apps/tree/master/minesweeper
'''

from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from hippo_tile import *

import random
import time


# Easy, Med, Hard: dimension squared, # of hippos
LEVELS = [
  (8, 10),
  (16, 40),
  (24, 99)
]

STATUS_READY = 0
STATUS_PLAYING = 1
STATUS_FAILED = 2
STATUS_SUCCESS = 3

STATUS_ICONS = {
  STATUS_READY: './images/alien_ship.png',
  STATUS_PLAYING: './images/crocodile.png',
  STATUS_FAILED: './images/angry_hippo.png',
  STATUS_SUCCESS: './images/red_alien.png'
}


class MainWindow(QMainWindow):
  """docstring for MainWindow"""
  def __init__(self, *args, **kwargs):
    super(MainWindow, self).__init__(*args, **kwargs)
    
    self.board_size, self.num_hippos = LEVELS[0]

    w = QWidget()
    hb = QHBoxLayout()

    # Track the numbers of hidden hippos
    self.hippos = QLabel()
    self.hippos.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)

    # Track the duration of play
    self.clock = QLabel()
    self.clock.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
    
    f = self.hippos.font()
    f.setPointSize(24)
    f.setWeight(75)
    self.hippos.setFont(f)
    self.clock.setFont(f)

    self._timer = QTimer()
    self._timer.timeout.connect(self.update_timer)
    self._timer.start(1000)  # 1 second timer

    self.hippos.setText("%03d" % self.num_hippos)
    self.clock.setText('000')

    # Status bar
    self.button = QPushButton()
    self.button.setFixedSize(QSize(40, 40))
    self.button.setIconSize(QSize(40, 40))
    self.button.setIcon(QIcon('./images/crocodile.png'))
    self.button.setFlat(True)

    self.button.pressed.connect(self.button_pressed)

    # Icon for remaining hippos
    hippos = QLabel()
    hippo_pix = QPixmap.fromImage(IMG_HIPPO).scaledToHeight(55)
    hippos.setPixmap(hippo_pix)
    hippos.setAlignment(Qt.AlignRight | Qt.AlignVCenter)

    hb.addWidget(hippos)

    # Top bar of game
    hb.addWidget(self.hippos)
    hb.addWidget(self.button)
    hb.addWidget(self.clock)

    # Icon for time since start
    timer = QLabel()
    timer_pix = QPixmap.fromImage(IMG_TIME).scaledToHeight(38)
    timer.setPixmap(timer_pix)
    timer.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    hb.addWidget(timer)

    vb = QVBoxLayout()
    vb.addLayout(hb)

    self.grid = QGridLayout()
    self.grid.setSpacing(5)

    vb.addLayout(self.grid)
    w.setLayout(vb)
    self.setCentralWidget(w)

    self.init_map()
    self.update_status(STATUS_READY)

    self.reset_map()
    self.update_status(STATUS_READY)

    self.show()


  def init_map(self):
    '''Add positions to a game board '''

    for x in range(0, self.board_size):
      for y in range(0, self.board_size):
        w = Tile(x, y)
        self.grid.addWidget(w, x, y)
        
        # Connect the signals
        w.clicked.connect(self.trigger_start)
        w.expose_hippo.connect(self.game_lost)
        w.expandable.connect(self.expand_reveal)

    # The singleShot timer is required to ensure the resize runs after we've returned to the event loop and Qt is aware of the new contents.
    # QTimer.singleShot(0, lambda: self.resize(1,1))


  def reset_map(self):
    ''' Clear the board and set up a new game '''

    self._reset_position_data()
    self._reset_add_hippos()
    self._reset_calculate_adjacency()
    #self._reset_add_starting_marker()
    self.update_timer()


  def _reset_position_data(self):
    ''' Go through each Tile widget and clear all data '''

    for x in range(0, self.board_size):
      for y in range(0, self.board_size):
        w = self.grid.itemAtPosition(y, x).widget()
        w.reset()


  def _reset_add_hippos(self):
    ''' Add new hippos for a new game '''

    positions = []

    while len(positions) < self.num_hippos:
      x, y = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
      
      if (x, y) not in positions:
        w = self.grid.itemAtPosition(y,x).widget()
        w.is_hippo = True
        positions.append((x, y))

    self.end_game_n = (self.board_size * self.board_size) - (self.num_hippos + 1)
    return positions


  def _reset_calculate_adjacency(self):
    ''' Count number of hippos around a given x,y tile '''

    def get_adjacency_n(x, y):
      positions = self.get_surrounding(x, y)
      return sum(1 for w in positions if w.is_hippo)

    for x in range(0, self.board_size):
      for y in range(0, self.board_size):
        w = self.grid.itemAtPosition(y, x).widget()
        w.adjacent_n = get_adjacency_n(x, y)


  def _reset_add_starting_marker(self):
    '''Place the starting marker
        Initial move placed by game to prevent starting with a hippo
    '''

    self.update_status(STATUS_READY)

    while True:
      x, y = random.randint(0, self.board_size - 1), random.randint(0, self.board_size - 1)
      w = self.grid.itemAtPosition(y, x).widget()
      if not w.is_hippo:
        w.is_start = True
        w.is_revealed = True
        w.update()

        # Reveal safe tiles around initial start point
        for w in self.get_surrounding(x, y):
          if not w.is_hippo:
            w.click()

        break

    self.update_status(STATUS_READY)


  def update_timer(self):
    if self.status == STATUS_PLAYING:
      n_secs = int(time.time()) - self.timer_start_nsecs
      self.clock.setText('%03d' % n_secs)


  def get_surrounding(self, x, y):
    ''' Check the 3x3 space around a clicked Tile 
            Return a list of surrounding Tile widgets
    '''  

    positions = []

    for xi in range(max(0, x - 1), min(x + 2, self.board_size)):
      for yi in range(max(0, y - 1), min(y + 2, self.board_size)):
        if not (xi == x and yi == y):
          positions.append(self.grid.itemAtPosition(yi, xi).widget())

    return positions  


# Which button?  Add info
  def button_pressed(self):
    
    if self.status == STATUS_PLAYING:
      self.update_status(STATUS_FAILED)
      self.reveal_map()
    elif self.status == STATUS_FAILED:
      self.update_status(STATUS_READY)
      self.reset_map()


# reveal() is in the Tile class; may need to modify how this is called
  def reveal_map(self):
    for x in range(0, self.board_size):
      for y in range(0, self.board_size):
        w = self.grid.itemAtPosition(y, x).widget()
        w.reveal()


  def expand_reveal(self, x, y):
    ''' When player clicks on Tile with 0 adjacent hippos '''
    
    for xi in range(max(0, x - 1), min(x + 2, self.board_size)):
      for yi in range(max(0, y - 1), min(y + 2, self.board_size)):
        w = self.grid.itemAtPosition(yi, xi).widget()
        if not w.is_hippo:
          w.click()


  def trigger_start(self, *args):
    if self.status != STATUS_PLAYING:
      self.update_status(STATUS_PLAYING)
      self.timer_start_nsecs = int(time.time())


  def update_status(self, status):
    self.status = status
    self.button.setIcon(QIcon(STATUS_ICONS[self.status]))


  def game_lost(self):
    self.reveal_map()
    self.update_status(STATUS_FAILED)


  def game_won(self):
    self.reveal_map()
    self.update_status(STATUS_SUCCESS)


# def setLevel(self, level):
#   self.level_name, self.board_size, self.num_hippos = LEVELS[level]

#   self.setWindowTitle('Hiding Hippos - %s' % (self.level_name))
#   self.hippos.setText('%03d' % self.num_hippos)

#   self.clear_map()
#   self.init_map()
#   self.reset_map()


if __name__ == '__main__':
  app = QApplication([])
  window = MainWindow()
  app.exec_()




