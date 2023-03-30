from chessbots.lib.point_helper import Point
from chessbots.lib.bot import *


class BoardBot:
    piece: str
    position: Point


class Board:
    def __init__(self, bot_repo: BotRepository):
        self.bots = bot_repo.get([])
        self.expected_fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'

    def add(self, bot: Bot):
        self.bots.append(bot)

    def boot(self):
        pass

    def get_pieces(self):
        pass
