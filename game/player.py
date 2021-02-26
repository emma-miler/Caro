from game.piece import Piece
from game.enums import PType, Color

class Player:
    def __init__(self, name, color, pieces=None):
        self.name = name
        self.color = color
        if pieces is None:
            if self.color == Color.WHITE:
                self.pieces = [
                    Piece(PType.PAWN, 0, 1, Color.WHITE),
                    Piece(PType.PAWN, 1, 1, Color.WHITE),
                    Piece(PType.PAWN, 2, 1, Color.WHITE),
                    Piece(PType.PAWN, 3, 1, Color.WHITE),
                    Piece(PType.PAWN, 4, 1, Color.WHITE),
                    Piece(PType.PAWN, 5, 1, Color.WHITE),
                    Piece(PType.PAWN, 6, 1, Color.WHITE),
                    Piece(PType.PAWN, 7, 1, Color.WHITE),
                    Piece(PType.ROOK, 0, 0, Color.WHITE),
                    Piece(PType.KNIGHT, 1, 0, Color.WHITE),
                    Piece(PType.BISHOP, 2, 0, Color.WHITE),
                    Piece(PType.QUEEN, 3, 0, Color.WHITE),
                    Piece(PType.KING, 4, 0, Color.WHITE),
                    Piece(PType.BISHOP, 5, 0, Color.WHITE),
                    Piece(PType.KNIGHT, 6, 0, Color.WHITE),
                    Piece(PType.ROOK, 7, 0, Color.WHITE),
                ]
                self.pieces = [
                    Piece(PType.ROOK, 3, 4, Color.WHITE),
                ]
            else:
                self.pieces = []
                """
                self.pieces = [
                    Piece(PType.PAWN, (0, 6), Color.BLACK),
                    Piece(PType.PAWN, (1, 6), Color.BLACK),
                    Piece(PType.PAWN, (2, 6), Color.BLACK),
                    Piece(PType.PAWN, (3, 6), Color.BLACK),
                    Piece(PType.PAWN, (4, 6), Color.BLACK),
                    Piece(PType.PAWN, (5, 6), Color.BLACK),
                    Piece(PType.PAWN, (6, 6), Color.BLACK),
                    Piece(PType.PAWN, (7, 6), Color.BLACK),
                    Piece(PType.ROOK, (0, 7), Color.BLACK),
                    Piece(PType.KNIGHT, (1, 7), Color.BLACK),
                    Piece(PType.BISHOP, (2, 7), Color.BLACK),
                    Piece(PType.QUEEN, (3, 7), Color.BLACK),
                    Piece(PType.KING, (4, 7), Color.BLACK),
                    Piece(PType.BISHOP, (5, 7), Color.BLACK),
                    Piece(PType.KNIGHT, (6, 7), Color.BLACK),
                    Piece(PType.ROOK, (7, 7), Color.BLACK),
                    Piece(PType.QUEEN, (4, 1), Color.BLACK),
                ]"""
        else:
            self.pieces = pieces