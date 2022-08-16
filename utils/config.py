import json


def load_config(path):

    with open(path, 'r') as f:
        data = json.load(f)
    return data
