from game.player import Player
from game.enums import Color, PType

class Engine:
    def __init__(self, players, board, parent=None):
        self.parent = parent
        self.board = board

    def calculate(self):
        plm = []
        for piece in self.board.pieces:
            if piece.color == Color.WHITE:
                pieceMoves =  piece.generatePseudoLegalMoves(self.board)
                for move in pieceMoves:
                    plm.append(move)
        self.parent.moveLabel.setText("Move amount: " + str(len(plm)))
        return plm

    def calcPins(self):
        attacks = []
        for piece in self.board.pieces:
            piece.pinned = False
        for piece in self.board.pieces:
            if piece.color == Color.WHITE and piece.type == PType.KING:
                piece.calcRookPin(attacks, self.board)
                piece.calcBishopPin(attacks, self.board)
        return attacks

    def calcCheckDefenseSquares(self):
        test = []
        checks = []
        next =  Color(self.board.turn.value + 1 if self.board.turn.value + 1 < len(Color) else 0)
        if not self.board.checks[next.value]:
            for piece in self.board.pieces:
                if piece.color == next:
                    pieceMoves =  piece.generatePseudoLegalMoves(self.board, ignoreCheck=True)
                    for move in pieceMoves:
                        if move.isCapture and move.captureType == PType.KING:
                            checks.append(move)
            if len(checks) > 0:
                self.board.checks[self.board.turn.value] = True
            for a in range(len(checks)):
                move = checks[a]
                test.append([])
                if move.dx != 0 and move.dy != 0:
                    # Diagonal
                    #print("diagonal")
                    if move.dx > 0 and move.dy > 0:
                        # Up Right
                        for z in range(1, move.dx):
                            test[a].append([move.x + z, move.y + z])
                    elif move.dx < 0 and move.dy < 0:
                        # Down Left
                        for z in range(1, abs(move.dx)):
                            test[a].append([move.x - z, move.y - z])
                    elif move.dx > 0 and move.dy < 0:
                        # Down Right
                        for z in range(1, abs(move.dx)):
                            test[a].append([move.x + z, move.y - z])
                    elif move.dx < 0 and move.dy > 0:
                        # Up Left
                        for z in range(1, abs(move.dx)):
                            test[a].append([move.x - z, move.y + z])
                elif move.dx != 0:
                    # Horizontal:
                    #print("horizontal")
                    m = -1 if move.dx < 0 else 1
                    for z in range(1, abs(move.dx)):
                        test[a].append([move.x + (m * z), move.y])
                elif move.dy != 0:
                    # Vertical
                    #print("vertical")
                    m = -1 if move.dy < 0 else 1
                    for z in range(1, abs(move.dy)):
                        test[a].append([move.x, move.y + (m * z)])
            if len(checks) > 1:
                return []
            else:
                defenseSquares= []
                for x in test:
                    for move in x:
                        defenseSquares.append(move)
                self.board.checkPieces = checks
                print("defense", defenseSquares)
                return defenseSquares

        else:
            return []