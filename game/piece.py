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
            """
            # Captures:
            if self.y < 6:
                # Bounds checks
                if self.x > 0:
                    if board.grid[self.x - 1][self.y + 1] != 0 and board.grid[self.x - 1][self.y + 1].color != self.color:
                        plm.append(Move(self, -1, 1))
                if self.x < 6:
                    if board.grid[self.x + 1][self.y + 1] != 0 and board.grid[self.x + 1][self.y + 1].color != self.color:
                        plm.append(Move(self, 1, 1))
            # First move 2 spaces
            if board.grid[self.x][self.y + 1] == 0:
                if not self.hasMoved and board.grid[self.x][self.y + 2] == 0:
                    pass
                    plm.append(Move(self, 0, 2))
                pass
                plm.append(Move(self, 0, 1))

            # TODO: Promotion and En Passant
        """
        elif self.type == PType.ROOK:
            n = 7 - self.x
            e = 7 - self.y
            s = self.x
            w = self.y
            for x in range(1,n+1):
                if board.grid[self.x + x][self.y] == 0 or board.grid[self.x + x][self.y].color != self.color:
                    plm.append(Move(self, x, 0))
                else:
                    break
            for y in range(1,e+1):
                if board.grid[self.x][self.y + y] == 0 or board.grid[self.x][self.y + y].color != self.color:
                    plm.append(Move(self, 0, y))
                else:
                    break
            for x in range(1,s+1):
                if board.grid[self.x - x][self.y] == 0 or board.grid[self.x - x][self.y].color != self.color:
                    plm.append(Move(self, -x, 0))
                else:
                    break
            for y in range(1,w+1):
                if board.grid[self.x][self.y - y] == 0 or board.grid[self.x][self.y - y].color != self.color:
                    plm.append(Move(self, 0, -y))
                else:
                    break
        return plm