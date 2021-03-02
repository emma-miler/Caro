from game.enums import PType, Color, Move

class Piece:
    def __init__(self, type, x, y, color):
        self.type = type
        self.x = x
        self.y = y
        self.color = color
        self.hasMoved = False

    def generatePseudoLegalMoves(self, board):
        plm = []
        # Pawn
        if self.type == PType.PAWN:
            self.calcPawn(plm, board)
        elif self.type == PType.ROOK:
           self.calcRook(plm, board)
        elif self.type == PType.QUEEN:
            self.calcBishop(plm, board)
            self.calcRook(plm, board)
        elif self.type == PType.BISHOP:
            self.calcBishop(plm, board)
        elif self.type == PType.KNIGHT:
            self.calcKnight(plm, board)
        elif self.type == PType.KING:
            self.calcKing(plm, board)
        return plm

    def calcPawn(self, plm, board):
        # Captures:
        m = 1 if self.color == Color.WHITE else - 1
        # Bounds checks
        if self.x > 0:
            if board.grid[self.x - 1][self.y + m] != 0 and board.grid[self.x - 1][self.y + m].color != self.color:
                plm.append(Move(self.x, self.y, -1, m))
        if self.x < 7:
            if board.grid[self.x + 1][self.y + m] != 0 and board.grid[self.x + 1][self.y + m].color != self.color:
                plm.append(Move(self.x, self.y, 1, m))
        if board.grid[self.x][self.y + m] == 0:
            if self.y == 6:
                plm.append(Move(self.x, self.y, 0, m, isPromotion=True, promoteTo=PType.QUEEN))
                plm.append(Move(self.x, self.y, 0, m, isPromotion=True, promoteTo=PType.KNIGHT))
                plm.append(Move(self.x, self.y, 0, m, isPromotion=True, promoteTo=PType.ROOK))
                plm.append(Move(self.x, self.y, 0, m, isPromotion=True, promoteTo=PType.BISHOP))
            else:
                plm.append(Move(self.x, self.y, 0, m))
        # First move 2 spaces
        if not self.hasMoved and board.grid[self.x][self.y + m] == 0 and board.grid[self.x][self.y + 2*m] == 0 and self.y == (1 if self.color == Color.WHITE else 6):
            plm.append(Move(self.x, self.y, 0, 2*m, enpassantable=True))

        # En Passant
        if self.y == 4 and board.moveList[-1].enpassantable:
            if self.x == 0 and board.moveList[-1].x == 1:
                plm.append(Move(self.x, self.y, 1, m, isEnPassant=True))
            elif self.x == 7 and board.moveList[-1].x == 6:
                plm.append(Move(self.x, self.y, -1, m, isEnPassant=True))
            elif board.moveList[-1].x == self.x + 1:
                plm.append(Move(self.x, self.y, 1, m, isEnPassant=True))
            elif board.moveList[-1].x == self.x - 1:
                plm.append(Move(self.x, self.y, -1, m, isEnPassant=True))

        # TODO: Promotion

    def calcRook(self, plm, board):
        n = 7 - self.x
        e = 7 - self.y
        s = self.x
        w = self.y
        for x in range(1, n + 1):
            if board.grid[self.x + x][self.y] == 0:
                plm.append(Move(self.x, self.y, x, 0))
            elif board.grid[self.x + x][self.y].color != self.color:
                plm.append(Move(self.x, self.y, x, 0))
                break
            else:
                break
        for y in range(1, e + 1):
            if board.grid[self.x][self.y + y] == 0:
                plm.append(Move(self.x, self.y, 0, y))
            elif board.grid[self.x][self.y + y].color != self.color:
                plm.append(Move(self.x, self.y, 0, y))
                break
            else:
                break
        for x in range(1, s + 1):
            if board.grid[self.x - x][self.y] == 0:
                plm.append(Move(self.x, self.y, -x, 0))
            elif board.grid[self.x - x][self.y].color != self.color:
                plm.append(Move(self.x, self.y, -x, 0))
                break
            else:
                break
        for y in range(1, w + 1):
            if board.grid[self.x][self.y - y] == 0:
                plm.append(Move(self.x, self.y, 0, -y))
            elif board.grid[self.x][self.y - y].color != self.color:
                plm.append(Move(self.x, self.y, 0, -y))
                break
            else:
                break

    def calcBishop(self, plm, board):
        for x in range(1, 8):
            if self.x + x <= 7 and self.y + x <= 7:
                if board.grid[self.x + x][self.y + x] == 0:
                    plm.append(Move(self.x, self.y, x, x))
                elif board.grid[self.x + x][self.y + x].color != self.color:
                    plm.append(Move(self.x, self.y, x, x))
                    break
                else:
                    break
        for x in range(1, 8):
            if self.x - x >= 0 and self.y - x >= 0:
                if board.grid[self.x - x][self.y - x] == 0:
                    plm.append(Move(self.x, self.y, -x, -x))
                elif board.grid[self.x - x][self.y - x].color != self.color:
                    plm.append(Move(self.x, self.y, -x, -x))
                    break
                else:
                    break
        for x in range(1, 8):
            if self.x - x >= 0 and self.y + x <= 7:
                if board.grid[self.x - x][self.y + x] == 0:
                    plm.append(Move(self.x, self.y, -x, x))
                elif board.grid[self.x - x][self.y + x].color != self.color:
                    plm.append(Move(self.x, self.y, -x, x))
                    break
                else:
                    break
        for x in range(1, 8):
            if self.x + x <= 7 and self.y - x >= 0:
                if board.grid[self.x + x][self.y - x] == 0:
                    plm.append(Move(self.x, self.y, x, -x))
                elif board.grid[self.x + x][self.y - x].color != self.color:
                    plm.append(Move(self.x, self.y, x, -x))
                    break
                else:
                    break

    def calcKnight(self, plm, board):
        if self.x > 1:
            if self.y + 1 <= 7 and (board.grid[self.x - 2][self.y + 1] == 0 or board.grid[self.x - 2][self.y + 1].color != self.color):
                plm.append(Move(self.x, self.y, -2, 1))
            if self.y - 1 >= 0 and (board.grid[self.x - 2][self.y - 1] == 0 or board.grid[self.x - 2][self.y - 1].color != self.color):
                plm.append(Move(self.x, self.y, -2, -1))
        if self.x > 0:
            if self.y + 2 <= 7 and (board.grid[self.x - 1][self.y + 2] == 0 or board.grid[self.x - 1][self.y + 2].color != self.color):
                plm.append(Move(self.x, self.y, -1, 2))
            if self.y - 2 >= 0 and (board.grid[self.x - 1][self.y - 2] == 0 or board.grid[self.x - 1][self.y - 2].color != self.color):
                plm.append(Move(self.x, self.y, -1, -2))
        if self.x < 6:
            if self.y + 1 <= 7 and (board.grid[self.x + 2][self.y + 1] == 0 or board.grid[self.x + 2][self.y + 1].color != self.color):
                plm.append(Move(self.x, self.y, 2, 1))
            if self.y - 1 >= 0 and (board.grid[self.x + 2][self.y - 1] == 0 or board.grid[self.x + 2][self.y - 1].color != self.color):
                plm.append(Move(self.x, self.y, 2, -1))
        if self.x < 7:
            if self.y + 2 <= 7 and (board.grid[self.x + 1][self.y + 2] == 0 or board.grid[self.x + 1][self.y + 2].color != self.color):
                plm.append(Move(self.x, self.y, 1, 2))
            if self.y - 2 >= 0 and (board.grid[self.x + 1][self.y - 2] == 0 or board.grid[self.x + 1][self.y - 2].color != self.color):
                plm.append(Move(self.x, self.y, 1, -2))

    def calcKing(self, plm, board):
        top = [[-1, 1], [0,1], [1,1]]
        mid = [[-1, 0], [1,0]]
        bottom = [[-1, -1], [0, -1], [1, -1]]
        if self.y == 7:
            top = []
        elif self.y == 0:
            bottom = []
        if self.x == 0:
            top = top[1:]
            mid = mid[1:]
            bottom = bottom[1:]
        elif self.x == 7:
            top = top[:-1]
            mid = mid[:-1]
            bottom = bottom[:-1]
        local = []
        for item in top: local.append(item)
        for item in mid: local.append(item)
        for item in bottom: local.append(item)
        for move in local:
            if board.grid[self.x + move[0]][self.y + move[1]] == 0 or board.grid[self.x + move[0]][self.y + move[1]].color != self.color:
                plm.append(Move(self.x, self.y, move[0], move[1]))

        # Castling
        if not self.hasMoved:
            # White
            if self.color == Color.WHITE:
                # Short
                maybeRook = board.grid[7][0]
                if maybeRook.type == PType.ROOK and maybeRook.hasMoved == False and maybeRook.color == self.color:
                    if board.grid[5][0] == 0 and board.grid[6][0] == 0:
                        plm.append(Move(self.x, self.y, 2, 0, isCastleShort=True))

                # Long
                maybeRook = board.grid[0][0]
                if maybeRook.type == PType.ROOK and maybeRook.hasMoved == False and maybeRook.color == self.color:
                    if board.grid[1][0] == 0 and board.grid[2][0] == 0 and board.grid[3][0] == 0:
                        plm.append(Move(self.x, self.y, -2, 0, isCastleLong=True))

            # Black
            elif self.color == Color.BLACK:
                # Short
                maybeRook = board.grid[7][7]
                if maybeRook.type == PType.ROOK and maybeRook.hasMoved == False and maybeRook.color == self.color:
                    if board.grid[5][7] == 0 and board.grid[6][7] == 0:
                        plm.append(Move(self.x, self.y, 2, 0, isCastleShort=True))

                # Long
                maybeRook = board.grid[0][7]
                if maybeRook.type == PType.ROOK and maybeRook.hasMoved == False and maybeRook.color == self.color:
                    if board.grid[1][7] == 0 and board.grid[2][7] == 0 and board.grid[3][7] == 0:
                        plm.append(Move(self.x, self.y, -2, 0, isCastleLong=True))
