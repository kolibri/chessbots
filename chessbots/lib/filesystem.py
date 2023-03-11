import json


def read_json(file_path: str):
    with open(file_path) as infile:
        return json.load(infile)


def dump_json(path: str, data):
    with open(path, 'w') as outfile:
        json.dump(data, outfile)


def dump_txt(path: str, data: str):
    with open(path, 'w') as f:
        f.write(data)
        f.close()
