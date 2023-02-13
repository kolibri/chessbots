from os.path import isfile, join
from werkzeug.datastructures import MultiDict
from os import listdir

from .Bot import Bot

class Bot:
    def __init__(self, host_name, data=None):
        self.host_name = host_name
        self.id = hashlib.sha256(self.host_name.encode('utf-8')).hexdigest()[0:8]
        if data is None:
            self.data = {}
        else:
            self.data = data
        self.data['id'] = self.id
        self.data['url'] = self.host_name

    @staticmethod
    def from_file(filename):
        data = read_json(filename)
        # print(filename, data)
        return Bot(data.get('url'), data)

    def save(self, path):
        with open((path + '/' + self.id + '.json'), 'w') as outfile:
            json.dump(self.data, outfile)


class BotManager:
    def __init__(self, cache_dir, collectors):
        self.cache_dir = cache_dir
        self.bots = self.__load(self.cache_dir)
        self.collectors = collectors

    def add(self, urls: [str]) -> [Bot]:
        bots = [Bot(url, {}) for url in urls]
        # self.bots = self.bots + bots
        for bot in bots:
            bot.save(self.cache_dir)
        return bots

    def update(self, filters: "MultiDict[str, str]") -> [Bot]:
        bots = []
        for bot in self.filter(filters):
            for c in self.collectors:
                try:
                    bot = Bot(bot.host_name, c.get_data(bot))
                # @todo: Yes, the ugly stuff right here. DataCollectors are maybe available
                except:
                    pass
            bots.append(bot)
            bot.save(self.cache_dir)
        return bots

    def filter(self, filters: "MultiDict[str, str]") -> [Bot]:
        def compare(bot: Bot, asserts) -> bool:
            for k, v in asserts.items():
                if bot.data.get(k) != v:
                    return False
            return True

        if 0 == len(filters):
            return self.bots
        return [bot for bot in self.bots if (compare(bot, filters))]

    @staticmethod
    def __load(base_dir: str) -> [Bot]:
        files = [f for f in listdir(base_dir) if isfile(base_dir + f)]
        return [Bot.from_file(join(base_dir, f)) for f in files if f.endswith('.json')]
