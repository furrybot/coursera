import os

class FileReader:
    
    def __init__(self, filename):
        self.filename = filename
        
    def read(self) -> str :
        try :
            with open(self.filename) as f:
                return f.read()
        except IOError:
            return ""