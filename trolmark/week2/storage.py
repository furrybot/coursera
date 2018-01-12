import os
import tempfile
import argparse
import json
import functools


# Utils
def get_file_path() -> str:
    return os.path.join(tempfile.gettempdir(), 'storage.data')
    
def load_storage_from_file(file_name) -> dict: 
    if not os.path.isfile(file_name) or os.path.getsize(file_name) == 0:
        return dict()
    
    with open(file_name) as f:
        d = json.load(f)
        return d

def save_storage_to_file(file_name, storage):
    with open(file_name, "w") as f:
        f.write(json.dumps(storage))
  
def save_value_to_storage(key, value, storage) -> dict:
    if key not in storage:
        storage[key] = [value]
        return storage
    
    storage[key] +=[value]
    return storage

def get_value_from_storage(key, storage) -> list:
    return storage.get(key, [])

def format_values(values) -> str:
    if len(values) == 0:
        return ""
    elif len(values) == 1:
        return values[0]
    return ', '.join([str(x) for x in values])


# Actions
def make_argument_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser()
    parser.add_argument("--key", help='Key')
    parser.add_argument("--value", help ='Value')
    return parser

def get_storage() -> (str, dict):
    file = get_file_path()
    return (file, load_storage_from_file(file))

def save(key, value):
    (file, storage) = get_storage()
    updated_storage = save_value_to_storage(key, value, storage)
    save_storage_to_file(file, updated_storage)
    
def load(key) -> str:
    (_, storage) = get_storage()
    value = get_value_from_storage(key, storage)
    return format_values(value)
    
    
if __name__ == "__main__":
    
    args = make_argument_parser().parse_args()
    if args.value and args.key:
        save(args.key, args.value)
    elif args.key:
        print(load(args.key))
    else:
        print("Put some arguments")