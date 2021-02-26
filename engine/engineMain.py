from game.player import Player
from game.enums import Color

class Engine:
    def __init__(self, players, board):
        self.board = board

    def calculate(self):
        plm = []
        for piece in self.board.pieces:
            if piece.color == Color.WHITE:
                pieceMoves =  piece.generatePseudoLegalMoves(self.board)
                for move in pieceMoves:
                    plm.append(move)
        return plm