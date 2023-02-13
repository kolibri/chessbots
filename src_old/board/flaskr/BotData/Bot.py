import hashlib
import json


def read_json(file_path: str):
    with open(file_path) as infile:
        return json.load(infile)


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
