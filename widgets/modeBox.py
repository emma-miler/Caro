from PyQt5 import QtGui, QtWidgets, QtCore, Qt

from math import floor
from game.enums import Mode
from widgets.modeButton import QGamemodeButton

class QGamemodeWidget(QtWidgets.QWidget):
    def __init__(self, boardUI, parent=None):
        super().__init__(parent)

        self.parent = parent
        self.boardUI = boardUI

        self.setMaximumSize(10000, 10000)
        policy = QtWidgets.QSizePolicy()
        policy.setHorizontalStretch(1)
        policy.setVerticalStretch(1)
        self.setSizePolicy(policy)
        self.lightBrush = QtGui.QBrush(QtGui.QColor(25, 25, 25))
        self.noBrush =  QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))
        self.selected = [0, 0]

        self.modeGroup = QtWidgets.QButtonGroup()

        self.playModeBox = QGamemodeButton("Play Mode")
        self.modeGroup.addButton(self.playModeBox)
        self.playModeBox.clicked.connect(lambda: self.boardUI.setMode(Mode.PLAY))
        self.playModeBox.click()

        self.placeModeBox = QGamemodeButton("Placement Mode")
        self.modeGroup.addButton(self.placeModeBox)
        self.placeModeBox.clicked.connect(lambda: self.boardUI.setMode(Mode.PLACE))

        self.moveModeBox = QGamemodeButton("Move Mode")
        self.modeGroup.addButton(self.moveModeBox)
        self.moveModeBox.clicked.connect(lambda: self.boardUI.setMode(Mode.MOVE))

        self.layout = QtWidgets.QHBoxLayout()
        self.setLayout(self.layout)

        self.layout.addWidget(self.playModeBox)
        self.layout.addWidget(self.placeModeBox)
        self.layout.addWidget(self.moveModeBox)

        #self.show()

    #def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    #    w = self.size().width() - 20
    #    h = self.size().height() - 20
    #    sx = w / 7
    #    sy = h / 2
    #    self.selected[0] = floor((event.x() - 10) / sx)
    #    self.selected[1] = floor((event.y() - 10) / sy)
    #    self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        w = self.size().width() - 10
        h = self.size().height() - 20
        sx = w / 7
        sy = h / 2
        qp.setBrush(self.lightBrush)
        qp.drawRect(0, 0, w, h)
        qp.end()