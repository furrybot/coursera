
class FileReader:
    def __init__(self, src):
        self.src = src

    def read(self):
        try:
            with open(self.src, 'r') as file:
                return file.read()
        except IOError:
            return ''


reader = FileReader('solution21312.py')
print(reader.read())