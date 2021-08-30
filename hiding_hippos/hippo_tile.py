from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *


IMG_FLAG = QImage('./images/grass.png')
IMG_HIPPO = QImage('./images/happy_hippo.png')
IMG_START = QImage('./images/red_alien.png')
IMG_TIME = QImage('./images/hourglass.png')





NUM_COLORS = {
    1: QColor('#f44336'),
    2: QColor('#9C27B0'),
    3: QColor('#3F51B5'),
    4: QColor('#03A9F4'),
    5: QColor('#00BCD4'),
    6: QColor('#4CAF50'),
    7: QColor('#E91E63'),
    8: QColor('#FF9800')
}



class Tile(QWidget):
  """A Tile object
      Info includes type, revealed, flagged, num_hippos nearby
      Signals include clicked, revealed, expandable
  """

  clicked = pyqtSignal()
  expandable = pyqtSignal(int,int)
  expose_hippo = pyqtSignal()
  

  def __init__(self, x, y, *args, **kwargs):
    super(Tile, self).__init__(*args, **kwargs)

    self.setFixedSize(QSize(23, 23))
    self.x = x
    self.y = y


  def reset(self):
    self.is_start = False
    self.is_hippo = False
    self.adjacent_n = 0
    self.is_revealed = False
    self.is_flagged = False

    self.update()


  def paintEvent(self, event):
    ''' Tiles are shown as a start position, hippo, or empty '''
    print('painted tiles')
    p = QPainter(self)
    p.setRenderHint(QPainter.Antialiasing)

    r = event.rect()

    if self.is_revealed:
      color = self.palette().color(QPalette.Background)
      outer, inner = color, color
    else:
      outer, inner = Qt.gray, Qt.lightGray

    p.fillRect(r, QBrush(inner))
    pen = QPen(outer)
    pen.setWidth(1)
    p.setPen(pen)
    p.drawRect(r)

    if self.is_revealed:
      if self.is_start:
        p.drawPixmap(r, QPixmap(IMG_START))

      elif self.is_hippo:
        p.drawPixmap(r, QPixmap(IMG_HIPPO))

      elif self.adjacent_n > 0:
        pen = QPen(NUM_COLORS[self.adjacent_n])
        p.setPen(pen)
        f = p.font()
        f.setBold(True)
        p.setFont(f)
        p.drawText(r, Qt.AlignHCenter | Qt.AlignVCenter, str(self.adjacent_n))
    elif self.is_flagged:
      p.drawPixmap(r, QPixmap(IMG_FLAG))
    

  def flag(self):
    self.is_flagged = not self.is_flagged
    self.update()
    self.clicked.emit()
  

  def reveal(self, emit=True):
    self.is_revealed = True
    #self.on_reveal()
    self.update()


  def click(self):
    ''' Action from a left-button click '''

    if not self.is_revealed:
      self.reveal()
      if self.adjacent_n == 0:
        self.expandable.emit(self.x, self.y)

    self.clicked.emit()


  def mouseReleaseEvent(self, e):
    ''' Right click = toggle grass on/off
        Left click = click() (unless it's already grass)
    '''

    if (e.button() == Qt.RightButton and not self.is_revealed):
      self.flag()
    elif (e.button() == Qt.LeftButton):
      self.click()

      if self.is_hippo:
        self.expose_hippo.emit()
    

  def on_reveal(self):
    ''' Check for losing / winning condition '''

    if w.is_hippo:
      self.game_lost()
    else:
      self.end_game_n -= 1
      if self.end_game_n == 0:
        self.game_won()


