from game.enums import Move

class Board:
    def __init__(self, pieces):
        self.pieces = pieces
        self.updateBoard()

    def updateBoard(self):
        self.grid = [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
        ]
        for piece in self.pieces:
            self.grid[piece.x][piece.y] = piece

    def performMove(self, move):
        move.piece.x = move.piece.x + move.dx
        move.piece.y = move.piece.y + move.dy
        self.updateBoard()