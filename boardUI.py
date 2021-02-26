from PyQt5 import QtGui, QtWidgets, QtCore, Qt

from game.player import Player
from game.enums import Color, renderSources, Move
from math import floor

class QBoardWidget(QtWidgets.QWidget):
    def __init__(self, board, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setMaximumSize(10000, 10000)
        policy = QtWidgets.QSizePolicy()
        policy.setHorizontalStretch(0)
        self.setSizePolicy(policy)
        self.setStyleSheet("background-color: red")
        self.darkBrush = QtGui.QBrush(QtGui.QColor(152, 77, 255))
        self.lightBrush = QtGui.QBrush(QtGui.QColor(230, 230, 230))
        self.moveBrush = QtGui.QBrush(QtGui.QColor(32, 32, 32, 128))
        self.testBrush = QtGui.QBrush(QtGui.QColor(32, 128, 32, 128))
        self.board = board
        self.possibleMoves = []
        self.tp = [0, 0]
        #self.show()

    def resizeEvent(self, e):
        self.resize(self.parent.height(), self.parent.height())
        #self.setMinimumWidth(self.height())

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        h = self.size().height() - 20
        s = h / 8
        self.tp[0] = floor((event.x() - 10) / s)
        self.tp[1] = floor((event.y() - 10) / s)
        if True:
            p = self.board.pieces[0]
            self.parent.board.performMove(Move(p, self.tp[0] - p.x, 7 - self.tp[1] - p.y))
            print(p.x, p.y)
        self.possibleMoves = self.parent.engine.calculate()
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        w = self.size().width() - 20
        h = self.size().height() - 20
        s = h/8
        qp.setPen(QtGui.QColor(0,0,0,0))
        qp.setBrush(self.lightBrush)
        qp.drawRect(0+10, 0+10, w-1, h-1)
        qp.setBrush(self.darkBrush)
        sp = 60 / s
        for x in range(4):
            for y in range(8):
                if y % 2 == 0:
                    o = s
                else:
                    o = 0
                qp.drawRect(s*2*x+o + 10, s*y + 10, s, s)

        imageArray = QtGui.QImage("ChessPiecesArray.png")
        for piece in self.board.pieces:
            source = renderSources[piece.type.value + 6*piece.color.value]
            target = QtCore.QRectF(piece.x * s + 10, (7-piece.y) * s + 10, 60 / sp, 60 / sp)
            qp.drawImage(target, imageArray, source)

        qp.setBrush(self.moveBrush)
        for move in self.possibleMoves:
            x = move.piece.x + move.dx
            y = move.piece.y + move.dy
            qp.drawEllipse(s*x + 10 + 15/sp, (7-y) * s + 10 + 15/sp, 30/sp, 30/sp)

        qp.setBrush(self.testBrush)
        qp.drawEllipse(s * self.tp[0] + 10 + 15 / sp, self.tp[1] * s + 10 + 15 / sp, 30 / sp, 30 / sp)

        qp.end()