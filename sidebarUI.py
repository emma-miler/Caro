from PyQt5 import QtGui, QtWidgets, QtCore, Qt

class QSideBarWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.setMaximumSize(10000, 10000)
        policy = QtWidgets.QSizePolicy()
        policy.setHorizontalStretch(0)
        self.setSizePolicy(policy)
        self.possibleMoves = []
        self.tp = [0, 0]
        self.editorWidget = None
        #self.show()

    def setEditorWidget(self, widget):
        self.editorWidget = widget

    def resizeEvent(self, e):
        self.resize(self.parent.width() - self.parent.height(),self.parent.height())
        self.move(self.parent.height(), self.parent.height() - self.height())
        self.update()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        qp = QtGui.QPainter()
        qp.begin(self)
        qp.setBrush(QtGui.QBrush(QtGui.QColor(25, 25, 25)))
        qp.drawRect(0, 0, self.width(), self.height())
        qp.end()