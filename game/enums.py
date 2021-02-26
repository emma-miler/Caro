from enum import Enum
from PyQt5.QtCore import QRectF
from collections import namedtuple

class PType(Enum):
    QUEEN = 0
    KING = 1
    ROOK = 2
    KNIGHT = 3
    BISHOP = 4
    PAWN = 5

class Color(Enum):
    WHITE = 0
    BLACK = 1

renderSources = [
    QRectF(0.0, 0.0, 150.0, 150.0),
    QRectF(150.0, 0.0, 150.0, 150.0),
    QRectF(300.0, 00.0, 150.0, 150.0),
    QRectF(450.0, 00.0, 150.0, 150.0),
    QRectF(600.0, 00.0, 150.0, 150.0),
    QRectF(750.0, 00.0, 150.0, 150.0),
    QRectF(0.0, 150.0, 150.0, 150.0),
    QRectF(150.0, 150.0, 150.0, 150.0),
    QRectF(300.0, 150.0, 150.0, 150.0),
    QRectF(450.0, 150.0, 150.0, 150.0),
    QRectF(600.0, 150.0, 150.0, 150.0),
    QRectF(750.0, 150.0, 150.0, 150.0)
]

Move = namedtuple("move", "piece dx dy")