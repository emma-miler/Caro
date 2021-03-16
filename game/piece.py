from game.enums import PType, Color, Move, Direction

class Piece:
    def __init__(self, type, x, y, color, hasMoved=False):
        self.type = type
        self.x = x
        self.y = y
        self.color = color
        self.hasMoved = hasMoved
        self.pinned = False
        self.pinDirection = None

    def generatePseudoLegalMoves(self, board, ignoreCheck=False):
        plm = []
        # Pawn
        if self.type == PType.PAWN:
            capLeft, capRight = False, False
            if self.pinned:
                if self.pinDirection == Direction.DIAGONALRIGHT:
                    capRight = True
                if self.pinDirection == Direction.DIAGONALLEFT:
                    capLeft = True
            self.calcPawn(plm, board, capLeft, capRight)
        elif self.type == PType.ROOK:
            if self.pinned and (self.pinDirection == Direction.DIAGONALLEFT or self.pinDirection == Direction.DIAGONALRIGHT):
                return plm
            else:
               self.calcRook(plm, board)
        elif self.type == PType.QUEEN:
            self.calcBishop(plm, board)
            self.calcRook(plm, board)
        elif self.type == PType.BISHOP:
            if self.pinned and (self.pinDirection == Direction.HORIZONTAL or self.pinDirection == Direction.VERTICAL):
                return plm
            else:
                self.calcBishop(plm, board)
        elif self.type == PType.KNIGHT:
            if self.pinned:
                return plm
            else:
                self.calcKnight(plm, board)
        elif self.type == PType.KING:
            self.calcKing(plm, board)

        if not ignoreCheck and not self.type == PType.KING:
            if board.checks[board.turn.value]:
                checkStop = []
                for move in plm:
                    x = move.x + move.dx
                    y = move.y + move.dy
                    for square in board.checkStopSquares:
                        if square[0] == x and square[1] == y:
                            checkStop.append(move)
                    for checkingPiece in board.checkPieces:
                        if checkingPiece[0] == x and checkingPiece[1] == y:
                            checkStop.append(move)
                return checkStop
            else:
                return plm
        else:
            return plm

    def calcPawn(self, plm, board, capLeft, capRight):
        m = 1 if self.color == Color.WHITE else - 1

        # Captures
        if self.x > 0:
            if board.grid[self.x - 1][self.y + m] != 0 and board.grid[self.x - 1][self.y + m].color != self.color:
                if (not self.pinned) or self.pinDirection == Direction.DIAGONALLEFT:
                    plm.append(Move(self.x, self.y, -1, m, isCapture=True, captureType=board.grid[self.x - 1][self.y + m].type))
        if self.x < 7:
            if board.grid[self.x + 1][self.y + m] != 0 and board.grid[self.x + 1][self.y + m].color != self.color:
                if (not self.pinned) or self.pinDirection == Direction.DIAGONALRIGHT:
                    plm.append(Move(self.x, self.y, 1, m, isCapture=True, captureType=board.grid[self.x + 1][self.y + m].type))

        if board.grid[self.x][self.y + m] == 0:
            if self.y == (6 if self.color == Color.WHITE else 1):
                if (not self.pinned) or self.pinDirection == Direction.VERTICAL:
                    plm.append(Move(self.x, self.y, 0, m, isPromotion=True, promoteTo=PType.QUEEN))
                    plm.append(Move(self.x, self.y, 0, m, isPromotion=True, promoteTo=PType.KNIGHT))
                    plm.append(Move(self.x, self.y, 0, m, isPromotion=True, promoteTo=PType.ROOK))
                    plm.append(Move(self.x, self.y, 0, m, isPromotion=True, promoteTo=PType.BISHOP))
            else:
                if (not self.pinned) or self.pinDirection == Direction.VERTICAL:
                    plm.append(Move(self.x, self.y, 0, m))
        # First move 2 spaces
        if not self.hasMoved and board.grid[self.x][self.y + m] == 0 and board.grid[self.x][self.y + 2*m] == 0 and self.y == (1 if self.color == Color.WHITE else 6):
            if (not self.pinned) or self.pinDirection == Direction.VERTICAL:
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

    def calcRook(self, plm, board):
        n = 7 - self.x
        e = 7 - self.y
        s = self.x
        w = self.y

        hor, ver = True, True
        if self.pinned:
            if self.pinDirection == Direction.VERTICAL:
                hor = False
            elif self.pinDirection == Direction.HORIZONTAL:
                ver = False

        if hor:
            for x in range(1, n + 1):
                if board.grid[self.x + x][self.y] == 0:
                    plm.append(Move(self.x, self.y, x, 0))
                elif board.grid[self.x + x][self.y].color != self.color:
                    plm.append(Move(self.x, self.y, x, 0, isCapture=True, captureType=board.grid[self.x + x][self.y].type))
                    break
                else:
                    break
            for x in range(1, s + 1):
                if board.grid[self.x - x][self.y] == 0:
                    plm.append(Move(self.x, self.y, -x, 0))
                elif board.grid[self.x - x][self.y].color != self.color:
                    plm.append(Move(self.x, self.y, -x, 0, isCapture=True, captureType=board.grid[self.x - x][self.y].type))
                    break
                else:
                    break
        if ver:
            for y in range(1, e + 1):
                if board.grid[self.x][self.y + y] == 0:
                    plm.append(Move(self.x, self.y, 0, y))
                elif board.grid[self.x][self.y + y].color != self.color:
                    plm.append(Move(self.x, self.y, 0, y, isCapture=True, captureType=board.grid[self.x][self.y + y].type))
                    break
                else:
                    break
            for y in range(1, w + 1):
                if board.grid[self.x][self.y - y] == 0:
                    plm.append(Move(self.x, self.y, 0, -y))
                elif board.grid[self.x][self.y - y].color != self.color:
                    plm.append(Move(self.x, self.y, 0, -y, isCapture=True, captureType=board.grid[self.x][self.y - y].type))
                    break
                else:
                    break

    def calcBishop(self, plm, board):
        right, left = True, True
        if self.pinned:
            if self.pinDirection == Direction.DIAGONALRIGHT:
                left = False
            elif self.pinDirection == Direction.DIAGONALLEFT:
                right = False
        if right:
            for x in range(1, 8):
                if self.x + x <= 7 and self.y + x <= 7:
                    if board.grid[self.x + x][self.y + x] == 0:
                        plm.append(Move(self.x, self.y, x, x))
                    elif board.grid[self.x + x][self.y + x].color != self.color:
                        plm.append(Move(self.x, self.y, x, x, isCapture=True, captureType=board.grid[self.x + x][self.y + x].type))
                        break
                    else:
                        break
            for x in range(1, 8):
                if self.x - x >= 0 and self.y - x >= 0:
                    if board.grid[self.x - x][self.y - x] == 0:
                        plm.append(Move(self.x, self.y, -x, -x))
                    elif board.grid[self.x - x][self.y - x].color != self.color:
                        plm.append(Move(self.x, self.y, -x, -x, isCapture=True, captureType=board.grid[self.x - x][self.y - x].type))
                        break
                    else:
                        break
        if left:
            for x in range(1, 8):
                if self.x - x >= 0 and self.y + x <= 7:
                    if board.grid[self.x - x][self.y + x] == 0:
                        plm.append(Move(self.x, self.y, -x, x))
                    elif board.grid[self.x - x][self.y + x].color != self.color:
                        plm.append(Move(self.x, self.y, -x, x, isCapture=True, captureType=board.grid[self.x - x][self.y + x].type))
                        break
                    else:
                        break
            for x in range(1, 8):
                if self.x + x <= 7 and self.y - x >= 0:
                    if board.grid[self.x + x][self.y - x] == 0:
                        plm.append(Move(self.x, self.y, x, -x))
                    elif board.grid[self.x + x][self.y - x].color != self.color:
                        plm.append(Move(self.x, self.y, x, -x, isCapture=True, captureType=board.grid[self.x + x][self.y - x].type))
                        break
                    else:
                        break

    def calcKnight(self, plm, board):
        #TODO: fix this shit
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
        # TODO: make sure king doesnt walk into check
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
        # TODO: fix castling into/out of/through checks
        if not self.hasMoved:
            # White
            if self.color == Color.WHITE:
                # Short
                maybeRook = board.grid[7][0]
                if type(maybeRook) != int:
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
                if type(maybeRook) != int:
                    if maybeRook.type == PType.ROOK and maybeRook.hasMoved == False and maybeRook.color == self.color:
                        if board.grid[5][7] == 0 and board.grid[6][7] == 0:
                            plm.append(Move(self.x, self.y, 2, 0, isCastleShort=True))

                    # Long
                    maybeRook = board.grid[0][7]
                    if maybeRook.type == PType.ROOK and maybeRook.hasMoved == False and maybeRook.color == self.color:
                        if board.grid[1][7] == 0 and board.grid[2][7] == 0 and board.grid[3][7] == 0:
                            plm.append(Move(self.x, self.y, -2, 0, isCastleLong=True))

    def calcRookPin(self, pinnedSquares, board):
        n = 7 - self.x
        e = 7 - self.y
        s = self.x
        w = self.y
        for x in range(1, n + 1):
            if board.grid[self.x + x][self.y] != 0 and board.grid[self.x + x][self.y].color != self.color and (board.grid[self.x + x][self.y].type == PType.QUEEN or board.grid[self.x + x][self.y].type == PType.ROOK):
                counter = 0
                temp = []
                for z in range(1, x):
                    if board.grid[self.x + z][self.y] != 0:
                        counter += 1
                        if board.grid[self.x + z][self.y].color == self.color:
                            temp.append(board.grid[self.x + z][self.y])
                if counter == 1 and len(temp) > 0:
                    temp[0].pinned = True
                    temp[0].pinDirection = Direction.HORIZONTAL
                    pinnedSquares.append([temp[0].x, temp[0].y])
        for x in range(1, s + 1):
            if board.grid[self.x - x][self.y] != 0 and board.grid[self.x - x][self.y].color != self.color and (board.grid[self.x - x][self.y].type == PType.QUEEN or board.grid[self.x - x][self.y].type == PType.ROOK):
                counter = 0
                temp = []
                for z in range(1, x):
                    if board.grid[self.x - z][self.y] != 0:
                        counter += 1
                        if board.grid[self.x - z][self.y].color == self.color:
                            temp.append(board.grid[self.x - z][self.y])
                if counter == 1 and len(temp) > 0:
                    temp[0].pinned = True
                    temp[0].pinDirection = Direction.HORIZONTAL
                    pinnedSquares.append([temp[0].x, temp[0].y])

        for y in range(1, e + 1):
            if board.grid[self.x][self.y + y] != 0 and board.grid[self.x][self.y + y].color != self.color and (board.grid[self.x][self.y + y].type == PType.QUEEN or board.grid[self.x][self.y + y].type == PType.ROOK):
                counter = 0
                temp = []
                for z in range(1, y):
                    if board.grid[self.x][self.y + z] != 0:
                        counter += 1
                        if board.grid[self.x][self.y + z].color == self.color:
                            temp.append(board.grid[self.x][self.y + z])
                if counter == 1 and len(temp) > 0:
                    temp[0].pinned = True
                    temp[0].pinDirection = Direction.VERTICAL
                    pinnedSquares.append([temp[0].x, temp[0].y])


        for y in range(1, w + 1):
            if board.grid[self.x][self.y - y] != 0 and board.grid[self.x][self.y - y].color != self.color and (board.grid[self.x][self.y - y].type == PType.QUEEN or board.grid[self.x][self.y - y].type == PType.ROOK):
                counter = 0
                temp = []
                for z in range(1, y):
                    if board.grid[self.x][self.y - z] != 0:
                        counter += 1
                        if board.grid[self.x][self.y - z].color == self.color:
                            temp.append(board.grid[self.x][self.y - z])
                if counter == 1 and len(temp) > 0:
                    temp[0].pinned = True
                    temp[0].pinDirection = Direction.VERTICAL
                    pinnedSquares.append([temp[0].x, temp[0].y])

    def calcBishopPin(self, pinnedSquares, board):
        for x in range(1, 8):
            if self.x + x <= 7 and self.y + x <= 7:
                if board.grid[self.x + x][self.y + x] != 0 and board.grid[self.x + x][self.y + x].color != self.color and (board.grid[self.x + x][self.y + x].type == PType.QUEEN or board.grid[self.x + x][self.y + x].type == PType.BISHOP):
                    counter = 0
                    temp = []
                    for z in range(1, x):
                        if board.grid[self.x + z][self.y + z] != 0:
                            counter += 1
                            if board.grid[self.x + z][self.y + z].color == self.color:
                                temp.append(board.grid[self.x + z][self.y + z])
                    if counter == 1 and len(temp) > 0:
                        temp[0].pinned = True
                        temp[0].pinDirection = Direction.DIAGONALRIGHT
                        pinnedSquares.append([temp[0].x, temp[0].y])
        for x in range(1, 8):
            if self.x - x >= 0 and self.y - x >= 0:
                if board.grid[self.x - x][self.y - x] != 0 and board.grid[self.x - x][self.y - x].color != self.color and (board.grid[self.x - x][self.y - x].type == PType.QUEEN or board.grid[self.x - x][self.y - x].type == PType.BISHOP):
                    counter = 0
                    temp = []
                    for z in range(1, x):
                        if board.grid[self.x - z][self.y - z] != 0:
                            counter += 1
                            if board.grid[self.x - z][self.y - z].color == self.color:
                                temp.append(board.grid[self.x - z][self.y - z])
                    if counter == 1 and len(temp) > 0:
                        temp[0].pinned = True
                        temp[0].pinDirection = Direction.DIAGONALRIGHT
                        pinnedSquares.append([temp[0].x, temp[0].y])
        for x in range(1, 8):
            if self.x - x >= 0 and self.y + x <= 7:
                if board.grid[self.x - x][self.y + x] != 0 and board.grid[self.x - x][self.y + x].color != self.color and (board.grid[self.x - x][self.y + x].type == PType.QUEEN or board.grid[self.x - x][self.y + x].type == PType.BISHOP):
                    counter = 0
                    temp = []
                    for z in range(1, x):
                        if board.grid[self.x - z][self.y + z] != 0:
                            counter += 1
                            if board.grid[self.x - z][self.y + z].color == self.color:
                                temp.append(board.grid[self.x - z][self.y + z])
                    if counter == 1 and len(temp) > 0:
                        temp[0].pinned = True
                        temp[0].pinDirection = Direction.DIAGONALLEFT
                        pinnedSquares.append([temp[0].x, temp[0].y])
        for x in range(1, 8):
            if self.x + x <= 7 and self.y - x >= 0:
                if board.grid[self.x + x][self.y - x] != 0 and board.grid[self.x + x][self.y - x].color != self.color and (board.grid[self.x + x][self.y - x].type == PType.QUEEN or board.grid[self.x + x][self.y - x].type == PType.BISHOP):
                    counter = 0
                    temp = []
                    for z in range(1, x):
                        if board.grid[self.x + z][self.y - z] != 0:
                            counter += 1
                            if board.grid[self.x + z][self.y - z].color == self.color:
                                temp.append(board.grid[self.x + z][self.y - z])
                    if counter == 1 and len(temp) > 0:
                        temp[0].pinned = True
                        temp[0].pinDirection = Direction.DIAGONALLEFT
                        pinnedSquares.append([temp[0].x, temp[0].y])