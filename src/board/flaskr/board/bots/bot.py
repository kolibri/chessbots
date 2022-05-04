import json
import hashlib
import os


class Bot:
    def __init__(self, host_name, data=None):
        self.host_name = host_name
        self.id = hashlib.sha256(self.host_name.encode('utf-8')).hexdigest()[0:8]
        if data is None:
            self.data = {}
        else:
            self.data = data
        self.data['id'] = self.id


    def get_position(self):
        pass

    def save(self, path):
        with open((path + '/' + self.id + '.json'), 'w') as outfile:
            json.dump(self.data, outfile)
