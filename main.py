from PyQt5 import QtWidgets, QtCore, QtGui
import sys, signal
from engine.engineMain import Engine

from game.player import Player
from game.enums import Color, Mode
from game.board import Board

from widgets.editorInterface import QEditorWidget
from widgets.boardUI import QBoardWidget
from widgets.modeBox import QGamemodeWidget
from sidebarUI import QSideBarWidget

class MainWindow(QtWidgets.QMainWindow):
    # Create settings for the software
    settings = QtCore.QSettings('Emma Miller', 'Caro')
    settings.setFallbacksEnabled(False)
    version = 'Alpha 0.1'

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        # Load the ui

        self.newWidget = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout()
        self.newWidget.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.sidebarWidget = QSideBarWidget(self)
        self.sidebar = QtWidgets.QVBoxLayout()
        self.sidebarWidget.setLayout(self.sidebar)

        self.players = [Player("White", Color.WHITE), Player("Black", Color.BLACK)]
        self.board = Board(self.players[0].pieces + self.players[1].pieces)
        self.engine = Engine(self.players, self.board, self)


        self.boardUI = QBoardWidget(self.board, self)
        self.layout.addWidget(self.boardUI)
        self.layout.addWidget(self.sidebarWidget)
        self.setCentralWidget(self.newWidget)

        self.calcButton = QtWidgets.QPushButton("Calculate")
        self.sidebar.addWidget(self.calcButton)
        self.calcButton.clicked.connect(self.engine.calculate)

        self.moveList = QtWidgets.QTableView()
        self.moveList.setStyleSheet("background-color:black")
        self.moveModel = QtGui.QStandardItemModel()
        self.moveList.setModel(self.moveModel)
        self.moveModel.insertColumns(0, 2)
        self.moveModel.insertRows(0, 20546)
        self.moveModel.setData(self.moveModel.index(0,0), "test")

        self.sidebar.addWidget(self.moveList)


        # Set up mode buttons
        self.modeBox = QGamemodeWidget(self.boardUI, self)
        self.sidebar.addWidget(self.modeBox)

        self.moveLabel = QtWidgets.QLabel("Move amount: ")
        self.sidebar.addWidget(self.moveLabel)
        self.editor = QEditorWidget(self)
        self.sidebar.addWidget(self.editor)
        self.setStyleSheet("background-color: rgb(16, 16, 16); color: #dde")

        self.test = QtWidgets.QPushButton("Debug")
        self.layout.addWidget(self.test)
        self.test.clicked.connect(self.engine.calcCheckDefenseSquares)

        plm = self.engine.calculate()
        self.boardUI.possibleMoves = plm
        self.boardUI.update()

        # Set the MainWindow Title
        self.setWindowTitle('Caro - ' + self.version)
        # When the software are closed on console the software are closed
        signal.signal(signal.SIGINT, signal.SIG_DFL)
        # Show the form
        self.showMaximized()



def main():
    # Start the software
    app = QtWidgets.QApplication(sys.argv)
    #MainWindow_ = QtWidgets.QMainWindow()
    ui = MainWindow()
    ui.show()
    #ui.setupUi(MainWindow)
    # Add the close feature at the program with the X
    sys.exit(app.exec_())


# Execute the software
main()