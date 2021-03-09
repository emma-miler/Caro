from game.enums import Move, Color

class Board:
    def __init__(self, pieces, turn=Color.WHITE):
        self.pieces = pieces
        self.turn = turn
        self.checks = [False, False]
        self.checkStopSquares = []
        self.moveList = [Move]
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
        piece = self.grid[move.x][move.y]
        print(move)
        newSquare = self.grid[move.x + move.dx][move.y + move.dy]
        if move.isPromotion:
            piece.type = move.promoteTo
        if newSquare != 0:
            self.removePiece([newSquare.x, newSquare.y])
        if move.isEnPassant:
            self.removePiece([move.x + move.dx, move.y + move.dy - (1 if self.turn == Color.WHITE else -1)])
        if move.isCastleShort:
            if piece.color == Color.WHITE:
                self.grid[7][0].x = 5
            elif piece.color == Color.BLACK:
                self.grid[7][7].x = 5
        if move.isCastleLong:
            if piece.color == Color.WHITE:
                self.grid[0][0].x = 3
            elif piece.color == Color.BLACK:
                self.grid[0][7].x = 3
        piece.x = move.x + move.dx
        piece.y = move.y + move.dy
        piece.hasMoved = True
        self.moveList.append(move)
        self.updateBoard()

    def removePiece(self, p):
        piece = self.grid[p[0]][p[1]]
        y = None
        for x in range(len(self.pieces)):
            if self.pieces[x] == piece:
                y = x
        if type(y) == int:
            del self.pieces[y]
        self.updateBoard()