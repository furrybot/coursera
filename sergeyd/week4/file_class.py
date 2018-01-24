import os
import tempfile


class File:
    def __init__(self, url):
        self.url = url
        self.file_data = self.read_file_data()

    def __add__(self, obj):
        temp_file_url = self.tempfile_dir_and_name('lox.txt')
        with open(temp_file_url, 'w') as f:
            f.write(self.file_data + obj.file_data)
        return temp_file_url

    def __getitem__(self, index):
        return self.read_file_data_line(index)

    def __str__(self):
        return self.url

    def empty_string(self):
        return ''

    def tempfile_dir_and_name(self, name):
        return os.path.join(tempfile.gettempdir(), name)

    def open_file(self, method):
        return open(self.url, method)

    def read_file_data(self):
        with self.open_file('r') as f:
            return f.read()

    def read_file_data_line(self, index):
        with self.open_file('r') as f:
            return f.readlines()[index]

    def write_file(self, str):
        with self.open_file('w') as f:
            f.write(str)


file_one = File('file.txt')
file_two = File('new.txt')

file_one.write_file('LOXL\nXOXOX\nOXO')
file_two.write_file('PO\nTSPO\nSTPO\nTSa\naaa')

new_obj = file_one + file_two

with open(new_obj, 'r') as f:
    print('Read summarized file', f.read())

for line in file_one:
    print('for file_one line: ', line)

for line in file_two:
    print('for file_two line: ', line)

print('file_one', file_one)
print('file_two', file_two)