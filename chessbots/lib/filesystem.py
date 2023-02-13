import json


def read_json(file_path: str):
    with open(file_path) as infile:
        return json.load(infile)


def dump_json(path: str, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)
