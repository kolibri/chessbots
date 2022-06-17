import os
import cv2
from ..Bot import Bot
from ..Captcha import Captcha
from ..Board import Board, txt_to_matrix


class PositionDataCollector:
    def __init__(self, cache_path, pattern_path):
        self.cache_path = cache_path
        self.pattern_path = pattern_path

    def get_data(self, bot: Bot):
        # print(bot.data)
        if 'position_local_filename' not in bot.data.keys():
            return bot.data
        captcha = Captcha(bot.data['position_local_filename'], [
            [self.pattern_path + 'pattern_WO.png', 0],
            [self.pattern_path + 'pattern_WX.png', 1],
            [self.pattern_path + 'pattern_BO.png', 0],
            [self.pattern_path + 'pattern_BX.png', 1]
        ])

        data = bot.data

        print(captcha.calculate_angel())
        data['captcha_angle'] = captcha.calculate_angel()[0]

        matches_path = self.cache_path + bot.id + '_matches.png'
        data['captcha_img_matches'] = matches_path
        cv2.imwrite(matches_path, captcha.get_img_matches())

        #data['captcha_txt'] = captcha.get_txt_captcha()
        #data['position_matches'] = captcha.get_txt_captcha()

        #board = Board(txt_to_matrix(create_txt_board_4x4_bin(10)))
        #data['position_matches'] = board.find_matches(data['captcha_txt'])

        return data

"flaskr/static/bot_cache/873adbe1_position.png"
