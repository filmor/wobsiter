from ..util import Path

class MenuHandler(object):
    def __init__(self, path):
        self._path = path

    def build(self, output):
        from ConfigParser import ConfigParser
        cfg = ConfigParser()
        cfg.read(str(self._path))

        self.title = cfg.sections()[0]
        self.items = \
            ((n.capitalize(), Path(fn).without_ext + '.html')
                    for n, fn in cfg.items(self.title))
        return self

