
import os.path
import glob
# Importieren und zu bla hinzufügen

_extensions = {}
for i in glob.glob(__file__

class SourceHandler(object):
    def __new__(cls, path):
        _, ext = os.path.splitext(str(path.basename))
        return _extensions[ext].__new__(path)

