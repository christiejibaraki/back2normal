import json


def read_json_to_dict(file_path):
    with open(file_path) as f:
        data_dict = json.load(f)
    return data_dict
