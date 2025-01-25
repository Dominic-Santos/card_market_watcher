import json
import os

def load_json(json_file):
    try:
        with open(json_file) as of:
            data = json.load(of)
    except:
        data = {}
    return data


def save_json(json_file, data):
    path = "/".join(json_file.split("/")[:-1])    
    if not os.path.exists(path):
        os.makedirs(path)

    with open(json_file, "w") as f:
        f.write(json.dumps(data, indent=4))