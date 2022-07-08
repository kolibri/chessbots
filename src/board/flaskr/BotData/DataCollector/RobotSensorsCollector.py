import requests

from ..Bot import Bot


class RobotSensorsCollector:
    def __init__(self, cache_path):
        self.cache_path = cache_path

    def get_data(self, bot: Bot):
        try:
            print(requests.get(bot.host_name).json())
            data = requests.get(bot.host_name).json()
        except requests.exceptions.RequestException as e:  # This is the correct syntax
            data = {'state': 'offline', 'url': bot.host_name}
            print('error', data, e)

        if 'live_image' in data:
            img_cache_path = self.cache_path + bot.id + '_position.jpeg'
            try:
                r = requests.get(data.get('live_image'))
                open(img_cache_path, 'wb').write(r.content)
                data['position_local_filename'] = img_cache_path
            except requests.exceptions.RequestException as e:
                print('failed to load image: ' + data['live_image'])

        return data
