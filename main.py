from PyQt5 import QtGui, QtWidgets, QtCore
import sys, signal
from engine.engineMain import Engine

from game.player import Player
from game.enums import Color
from game.board import Board

from editorInterface import QEditorWidget
from boardUI import QBoardWidget

class MainWindow(QtWidgets.QMainWindow):
    # Create settings for the software
    settings = QtCore.QSettings('Your Name', 'Name of the software')
    settings.setFallbacksEnabled(False)
    version = 'Your version'

    def __init__(self, parent=None):
        QtWidgets.QMainWindow.__init__(self, parent)
        # Load the ui

        self.newWidget = QtWidgets.QWidget()
        self.layout = QtWidgets.QHBoxLayout()
        self.newWidget.setLayout(self.layout)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.sidebar = QtWidgets.QVBoxLayout()

        self.players = [Player("White", Color.WHITE), Player("Black", Color.BLACK)]
        self.board = Board(self.players[0].pieces + self.players[1].pieces)
        self.engine = Engine(self.players, self.board)


        self.boardUI = QBoardWidget(self.board, self)
        self.layout.addWidget(self.boardUI)
        self.layout.addLayout(self.sidebar)
        self.setCentralWidget(self.newWidget)

        self.calcButton = QtWidgets.QPushButton("Calculate")
        self.sidebar.addWidget(self.calcButton)
        self.calcButton.clicked.connect(self.engine.calculate)

        plm = self.engine.calculate()
        self.boardUI.possibleMoves = plm
        self.boardUI.update()

        self.sidebar.addWidget(QtWidgets.QPushButton("TEST2"))
        self.editor = QEditorWidget(self)
        self.sidebar.addWidget(self.editor)
        self.setStyleSheet("background-color: rgb(16, 16, 16); color: #dde")

        # Set the MainWindow Title
        self.setWindowTitle('name of the software - ' + self.version)
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