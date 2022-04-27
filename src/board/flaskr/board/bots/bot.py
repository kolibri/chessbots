import hashlib


class Bot:
    def __init__(self, host_name, data=None):
        self.host_name = host_name
        self.id = hashlib.sha256(self.host_name.encode('utf-8')).hexdigest()
        if data is None:
            self.data = {}
        else:
            self.data = data
