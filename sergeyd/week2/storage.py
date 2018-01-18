import argparse
import json

storage_path = 'storage.data'


def read_file_data(path):
    with open(path, 'r') as f:
        data = f.read()
        return json.loads(data) if data != '' else {}


def update_model(data, args):
    if data.get(args.key, False):
        data[args.key].append(args.value)
    else:
        data[args.key] = [args.value]

    return json.dumps(data)


def args_parse():
    parser = argparse.ArgumentParser()
    parser.add_argument("-k", "--key")
    parser.add_argument("-v", "--value")
    return parser.parse_args()


def storage_write(f, data):
    f.write(data)
    f.seek(0)
    print(f.read())


def get_value(data, key):
    value = data.get(key, 'None')
    return ", ".join(value) if isinstance(value, list) else value


cmd_args = args_parse()
model = read_file_data(storage_path)

if cmd_args.value:
    with open(storage_path, 'r+') as file:
        model = update_model(model, cmd_args)
        storage_write(file, model)
else:
    print(get_value(model, cmd_args.key))


