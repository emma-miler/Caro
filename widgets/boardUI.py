from PyQt5 import QtGui, QtWidgets, QtCore, Qt

from game.player import Player
from game.enums import Color, renderSources, Move, PType, Mode, promotionSources
from game.piece import Piece
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
        self.mode = Mode.PLAY
        self.selected = 0
        self.drawPromotionDialog = False
        #self.show()

    def setMode(self, Mode):
        self.mode = Mode
        self.update()

    def resizeEvent(self, e):
        self.resize(self.parent.height(), self.parent.height())
        #self.setMinimumWidth(self.height())
        self.update()

    def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
        h = self.size().height() - 20
        s = h / 8
        self.tp[0] = floor((event.x() - 10) / s)
        self.tp[1] = floor((event.y() - 10) / s)
        if self.mode == Mode.PLACE:
            s = self.parent.editor.selected
            if s[0] == 6:
                if self.board.grid[self.tp[0]][7 - self.tp[1]] == self.selected:
                    self.selected = 0
                self.board.removePiece([self.tp[0], 7 - self.tp[1]])
            else:
                newPiece = Piece(PType(s[0]), self.tp[0], 7 - self.tp[1], Color(s[1]))
                self.board.pieces.append(newPiece)
                self.board.updateBoard()
        # Play Move
        elif self.mode == Mode.PLAY:
            if self.drawPromotionDialog:
                if self.tp[0] == self.selected.x and self.tp[1] < 4:
                    if self.tp[1] == 0:
                        self.parent.board.performMove(Move(self.selected.x, self.selected.y, 0, 1, isPromotion=True, promoteTo=PType.QUEEN))
                    elif self.tp[1] == 1:
                        self.parent.board.performMove(Move(self.selected.x, self.selected.y, 0, 1, isPromotion=True, promoteTo=PType.ROOK))
                    elif self.tp[1] == 2:
                        self.parent.board.performMove(Move(self.selected.x, self.selected.y, 0, 1, isPromotion=True, promoteTo=PType.KNIGHT))
                    elif self.tp[1] == 3:
                        self.parent.board.performMove(Move(self.selected.x, self.selected.y, 0, 1, isPromotion=True, promoteTo=PType.BISHOP))
                    self.selected = 0
                    self.board.turn = Color(self.board.turn.value + 1 if self.board.turn.value + 1 < len(Color) else 0)
                    self.drawPromotionDialog = False
            else:
                # Select a piece if none is selected
                if self.selected == 0:
                    self.selected = self.board.grid[self.tp[0]][7-self.tp[1]]
                    if self.selected != 0 and self.selected.color != self.board.turn:
                        self.selected = 0
                # If something is already selected
                else:
                    x,y = self.selected.x, self.selected.y
                    succes = False
                    # Generate moves and check if clicked square is legal
                    for move in self.selected.generatePseudoLegalMoves(self.board):
                        if self.tp[0] == x + move.dx and 7 - self.tp[1] == y + move.dy:
                            if move.isPromotion:
                                self.drawPromotionDialog = True
                            else:
                                self.parent.board.performMove(move)
                                self.selected = 0
                                self.board.turn = Color(self.board.turn.value + 1 if self.board.turn.value + 1 < len(Color) else 0)
                            succes = True
                            break
                    if not succes:
                        self.selected = self.board.grid[self.tp[0]][7 - self.tp[1]]
                        if self.selected != 0 and self.selected.color != self.board.turn:
                            self.selected = 0
        elif self.mode == Mode.MOVE:
            p = self.board.pieces[0]
            self.parent.board.performMove(Move(p.x, p.y, self.tp[0] - p.x, 7 - self.tp[1] - p.y))
        else:
            raise NotImplementedError("Mode not implemented?")
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
            if piece.x >= 0 and piece.y >= 0:
                source = renderSources[piece.type.value + 6*piece.color.value]
                target = QtCore.QRectF(piece.x * s + 10, (7-piece.y) * s + 10, 60 / sp, 60 / sp)
                qp.drawImage(target, imageArray, source)

        qp.setBrush(self.moveBrush)
        if self.mode == Mode.PLAY:
            if self.selected != 0:
                for move in self.selected.generatePseudoLegalMoves(self.board):
                    x = move.x + move.dx
                    y = move.y + move.dy
                    qp.drawEllipse(s * x + 10 + 15 / sp, (7 - y) * s + 10 + 15 / sp, 30 / sp, 30 / sp)
        else:
            for move in self.possibleMoves:
                x = move.x + move.dx
                y = move.y + move.dy
                qp.drawEllipse(s*x + 10 + 15/sp, (7-y) * s + 10 + 15/sp, 30/sp, 30/sp)

        if self.drawPromotionDialog:
            qp.setBrush(QtGui.QBrush(QtGui.QColor(0,0,0,128)))
            qp.drawRect(0,0,w+10,h+10)
            qp.setBrush(QtGui.QBrush(QtGui.QColor(255, 255, 255, 128)))
            x,y = self.selected.x, self.selected.y

            if self.selected.color == Color.WHITE:
                qp.drawRect(s*x+10, 10, s, 4*s)
                for z in range(4):
                    target = QtCore.QRectF(x * s + 10, 10 + z*s, 60 / sp, 60 / sp)
                    qp.drawImage(target, imageArray, promotionSources[z])
            elif self.selected.color == Color.BLACK:
                qp.drawRect(s * x + 10, self.height() - 10 - 4*s, s, 4 * s)
                for z in range(4):
                    target = QtCore.QRectF(x * s + 10, self.height() - 10 - (z+1)*s, 60 / sp, 60 / sp)
                    qp.drawImage(target, imageArray, promotionSources[z+4])

        qp.setBrush(self.testBrush)
        #qp.drawEllipse(s * self.tp[0] + 10 + 15 / sp, self.tp[1] * s + 10 + 15 / sp, 30 / sp, 30 / sp)

        qp.end()