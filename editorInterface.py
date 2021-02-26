from PyQt5 import QtGui, QtWidgets, QtCore, Qt

from game.player import Player
from game.enums import Color, renderSources, Move
from math import floor

class QEditorWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setMaximumSize(10000, 10000)
        policy = QtWidgets.QSizePolicy()
        policy.setHorizontalStretch(0)
        self.setSizePolicy(policy)
        self.lightBrush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
        self.noBrush =  QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        self.selected = [0, 0]
        #self.show()

    def resizeEvent(self, e):
        self.resize(self.parent.width() - self.parent.height() - 20, int((self.parent.width() - self.parent.height() - 20) / 3.5))
        self.move(self.parent.height() +20, self.parent.height() - self.height() + 10)
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        w = self.size().width() - 20
        h = self.size().height() - 20
        sx = w / 7
        sy = h / 2
        self.selected[0] = floor((event.x() - 10) / sx)
        self.selected[1] = floor((event.y() - 10) / sy)
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        w = self.size().width() - 20
        h = self.size().height() - 20
        sx = w / 7
        sy = h / 2
        qp.setPen(QtGui.QColor(0,0,0,0))
        qp.setBrush(self.lightBrush)
        qp.drawRect(0, 0, w, h)

        imageArray = QtGui.QImage("ChessPiecesArray.png")
        source = QtCore.QRectF(0, 0, 1050, 300)
        target = QtCore.QRectF(0, 0, w, h)
        qp.drawImage(target, imageArray, source)

        qp.setPen(QtGui.QColor(200, 200, 200, 255))
        qp.setBrush(self.noBrush)
        qp.drawRect(self.selected[0] * sx, self.selected[1] * sy, sx, sy)

        qp.end()