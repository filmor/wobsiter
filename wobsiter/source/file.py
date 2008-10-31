
class FileHandler(object):
    def __init__(self, path):
        self._path = path

    def build(self, output):
        output.copy_file(self._path)

