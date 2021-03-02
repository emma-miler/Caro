from PyQt5 import QtGui, QtWidgets, QtCore, Qt

from math import floor
from game.enums import Mode

class QGamemodeButton(QtWidgets.QRadioButton):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.parent = parent

        self.setMaximumSize(10000, 10000)
        policy = QtWidgets.QSizePolicy()
        policy.setHorizontalStretch(1)
        policy.setVerticalStretch(0)
        self.setSizePolicy(policy)
        self.activeBrush = QtGui.QBrush(QtGui.QColor(32, 32, 32))
        self.inactiveBrush = QtGui.QBrush(QtGui.QColor(64, 64, 64))
        self.noBrush =  QtGui.QBrush(QtGui.QColor(0, 0, 0, 0))

        #self.show()

    #def resizeEvent(self, e):
    #    self.resize(self.width(), int(self.width() / 3))
    #    self.move(10, self.parent.height() - self.height() +10)
    #    self.update()

    #def mousePressEvent(self, event: QtGui.QMouseEvent) -> None:
    #    w = self.size().width() - 20
    #    h = self.size().height() - 20
    #    sx = w / 7
    #    sy = h / 2
    #    self.selected[0] = floor((event.x() - 10) / sx)
    #    self.selected[1] = floor((event.y() - 10) / sy)
    #    self.update()
    def mousePressEvent(self, e: QtGui.QMouseEvent) -> None:
        self.click()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setRenderHint(QtGui.QPainter.SmoothPixmapTransform)
        w = self.size().width() - 10
        h = self.size().height() - 20
        sx = w / 7
        sy = h / 2
        if self.isChecked():
            qp.setBrush(self.activeBrush)
        else:
            qp.setBrush(self.inactiveBrush)

        qp.drawRect(0, 0, w, h)
        font = qp.font()
        font.setPixelSize(48)
        qp.setFont(font)
        qp.drawText(QtCore.QRect(0,0,w,h), QtCore.Qt.AlignCenter |QtCore.Qt.TextWordWrap, self.text())
        qp.end()