from ..Bot import Bot
from ..Captcha import Captcha


class CaptchaDataCollector:
    def __init__(self, cache_path, pattern_path):
        self.cache_path = cache_path
        self.pattern_path = pattern_path
        self.templates = [
            [self.pattern_path + 'pattern_WO.png', 0],
            [self.pattern_path + 'pattern_WX.png', 1],
            [self.pattern_path + 'pattern_BO.png', 0],
            [self.pattern_path + 'pattern_BX.png', 1]
        ]

    def get_data(self, bot: Bot):
        if 'position_local_filename' not in bot.data.keys():
            return bot.data
        data = bot.data
        captcha = Captcha(data['position_local_filename'], self.templates)
        angle, board = captcha.resolve()
        data['captcha_angle'] = angle
        data['captcha_board'] = board.txt()

        return data
