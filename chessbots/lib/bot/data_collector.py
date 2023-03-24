from __future__ import annotations
import requests
import os
from chessbots.lib.bot import Bot, BotDataCollector
from chessbots.lib.captcha import Captcha


class ChainDataCollector(BotDataCollector):
    def __init__(self, collectors: [BotDataCollector]):
        self.collectors = collectors

    def get_data(self, bot: Bot):
        data = bot.data
        for collector in self.collectors:
            data = data | collector.get_data(bot)
        return data


class RobotApiCollector(BotDataCollector):
    def __init__(self, cache_path: str):
        self.cache_path = cache_path

    def get_data(self, bot: Bot):
        try:
            data = requests.get(bot.host_name).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            data = {'state': 'offline', 'url': bot.host_name}
            print('robot sensor: failed to load bot info', data, e)

        if 'image_live' in data:
            img_cache_path = os.path.join(self.cache_path, bot.id + '_position.jpeg')
            try:
                r = requests.get(data.get('live_image'))
                open(img_cache_path, 'wb').write(r.content)
                data['position_local_filename'] = img_cache_path
            except requests.exceptions.RequestException as e:
                print('robot sensor: failed to load image: ', data['live_image'])
        return data


class CaptchaReaderCollector(BotDataCollector):
    def get_data(self, bot: Bot):
        if 'position_local_filename' not in bot.data.keys():
            return bot.data
        data = bot.data
        captcha = Captcha(data['position_local_filename'])
        data['captcha_angle'] = captcha.angle
        data['captcha_board'] = captcha.result.txt()
        data['position'] = captcha.result

        return data
