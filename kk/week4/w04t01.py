import tempfile


class File:
    @staticmethod
    def temp_path():
        return tempfile.mkstemp()[1]

    def __init__(self, path):
        self.path = path

    def __add__(self, other: 'File'):
        sum_file = self.__class__(self.temp_path())
        sum_file.write(self.contents() + other.contents())
        return sum_file

    def __iter__(self):
        with open(self.path) as f:
            for line in f:
                yield line

    def __str__(self):
        return self.path

    def contents(self):
        with open(self.path) as f:
            return f.read()

    def write(self, line):
        with open(self.path, 'w') as f:
            f.write(line)
