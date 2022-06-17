from ..Bot import Bot
from ..Board import *


class BoardPositionCollector:
    def __init__(self, board: Board):
        self.board = board

    def get_data(self, bot: Bot):
        if 'captcha_board' not in bot.data.keys():
            return bot.data
        data = bot.data
        matches = self.board.find_matches(Board(txt_to_matrix(data['captcha_board'])))
        data['board_matches'] = matches

        return data
