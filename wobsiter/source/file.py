
class FileHandler(object):
    def __init__(self, path, dir=None):
        self._path = path
        self._dir = dir

    def build(self, output):
        directory = output.directory
        if self._dir:
            output.directory = self._dir
        self.result = output.copy_file(self._path)
        output.directory = directory

