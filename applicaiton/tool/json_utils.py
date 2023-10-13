import json
import os


def read_josn(name):
    with open(file=os.getcwd() + '/' + name, mode='r', encoding='utf-8') as f:
        json_str = f.read()
        return json.loads(json_str)
