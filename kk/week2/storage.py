import json
import os
import tempfile
import argparse
from pathlib import Path

STORAGE_NAME = 'storage.data'


def storage_empty():
    return {}


def storage_empty_key():
    return []


def storage_serialize(data):
    return json.dumps(data)


def storage_deserialize(string):
    return json.loads(string)


def storage_get_path(name=STORAGE_NAME):
    return os.path.join(tempfile.gettempdir(), name)


def storage_load(name):
    path = storage_get_path(name)
    if not Path(path).is_file():
        return storage_empty()
    with open(path, 'r') as file:
        content = file.read()
    if content is None or content == "":
        return storage_empty()
    else:
        return storage_deserialize(content)


def storage_save(name, data):
    with open(storage_get_path(name), 'w') as file:
        return file.write(storage_serialize(data))


def storage_set(name, key, value):
    storage_data = storage_load(name)
    if key not in storage_data or type(storage_data[key]) != list:
        storage_data[key] = storage_empty_key()
    storage_data[key].append(value)
    storage_save(name, storage_data)


def storage_get(name, key):
    storage_data = storage_load(name)
    return storage_data[key] if key in storage_data else storage_empty_key()


parser = argparse.ArgumentParser()
parser.add_argument("--key", help="key to set/lookup value under", type=str, required=True)
parser.add_argument("--val", help="value to set under the key", type=str)
args = parser.parse_args()

if args.val is not None and args.val != "":
    storage_set(STORAGE_NAME, args.key, args.val)
else:
    print(', '.join(storage_get(STORAGE_NAME, args.key)))
