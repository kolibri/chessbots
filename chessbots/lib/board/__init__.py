from chessbots.lib.point_helper import Point
from chessbots.lib.bot import *
from typing import NamedTuple
import chess


class BoardField:
    FILES = ['z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'x']
    RANKS = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']

    def __init__(self, file: str, rank: str):
        if file not in self.FILES:
            raise RuntimeError('Invalid file for BoardField: ' + file)
        if rank not in self.RANKS:
            raise RuntimeError('Invalid rank for BoardField: ' + rank)

        self.file = file
        self.rank = rank

    @staticmethod
    def from_square(square: chess.Square):
        return BoardField(
            BoardField.FILES[chess.square_file(square)+1],
            BoardField.RANKS[chess.square_rank(square)+1],
        )

    def to_json(self):
        return [self.file, self.rank]

    def get_grid_area(self):
        point = Point(self.FILES.index(self.file), self.RANKS.index(self.rank))

        area_start = point.mult(20)
        area_end = area_start.add(Point(19, 19))
        return area_start, area_end


class PieceCheckResult:
    def __init__(self, piece: str, field: BoardField, bots: [Bot]):
        self.piece = piece
        self.field = field

        self.found = False
        self.multiple = False
        self.bot = None
        bots_on_field = [b for b in bots if b.captcha_data and b.captcha_data.pos.in_area(field.get_grid_area()) and b.http_data.piece == piece]
        print('bof', piece, bots_on_field, bots, [f.txt for f in field.get_grid_area()])
        if 1 == len(bots_on_field):
            self.found = True
            self.bot = bots_on_field[0]
        elif 0 != len(bots_on_field):
            self.multiple = True

    def to_json(self):
        return {
            'piece': self.piece,
            'field': self.field.to_json(),
            'found': self.found,
            'multiple': self.multiple,
            'bot': self.bot.to_json() if self.bot else None,
        }


class Game: # Wrapper around https://python-chess.readthedocs.io/en/latest/
    def __init__(self):
        self.fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'
        self.chess_board = chess.Board(self.fen)

    def get_expected_piece_fields(self) -> [int, bool, chess.SquareSet]:
        pieces = []
        for color in chess.COLORS:
            for piece in [chess.KING, chess.QUEEN, chess.BISHOP, chess.KNIGHT, chess.ROOK, chess.PAWN]:
                piece_name = chess_piece_color_to_piecename(piece, color)
                squares = self.chess_board.pieces(piece, color)
                for sq in squares:
                    pieces.append([piece_name, BoardField.from_square(sq)])
        return pieces


class Board:
    def __init__(self, bot_repo: BotRepository, game: Game):
        self.bot_repo = bot_repo
        self.game = game
        self.pieces = [PieceCheckResult(piece, field, self.bot_repo.get()) for piece, field in self.game.get_expected_piece_fields()]
        self.rest_bots = [b for b in self.bot_repo.get() if b.url not in [pb.bot.url for pb in self.pieces if pb.found]]
        self.playable = 0 == len([r for r in self.pieces if not r.found])


def chess_piece_color_to_piecename(piece: chess.PieceType, color: chess.Color) -> str:
    pm = ['p', 'n', 'b', 'r', 'q', 'k']
    cm = 'w' if color else 'b'
    return cm + pm[piece - 1]
