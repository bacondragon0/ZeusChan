import wget
import config

class Zeus:
    def __init__(self):
        self.url = config.URL
        self.filepath = config.FILE_PATH
    
    def download(self):
        wget.download(self.url, self.filepath)
        print(f"\nICS File retrieved to path {self.filepath}\n ")
        return self.filepath
