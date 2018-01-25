import os
import tempfile

class File:
    def __init__(self, filename):
        self.filename = filename
        if not os.path.exists(filename):
            open(filename, 'w+').close()
    
    def read(self):
        with open(self.filename, 'r') as f:
            return f.read()
        
    def write(self, line):
        with open(self.filename, "a") as f:
            return f.write(line)
    
    def __str__(self):
        return self.filename
    
    def __iter__(self):
        return self.open_file
    
    def __next__(self):
        return next(open(self.filename, 'r'))
    
    def __add__(self, obj):
        base_name = os.path.basename(self.filename)+ "_" + os.path.basename(obj.filename)
        composed_file_name = File.get_filename(base_name)
        
        new_obj = File(composed_file_name)
        new_obj.write(self.read() + obj.read())
        return new_obj
    
    @staticmethod
    def get_filename(name):
        return os.path.join(tempfile.gettempdir(), name)