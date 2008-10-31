from ..util import Path
from os import walk
from file import FileHandler
from . import Source

from Cheetah.Template import Template
from Cheetah.Filters import Filter

class EncodeUnicode(Filter):
    def filter(self, val, **kw):
        if type(val) == type(u''):
            return val.encode(kw.get('encoding', 'utf-8'))
        else:
            return str(val)

class TemplateHandler(object):
    def __init__(self, path):
        self._path = path
        self.deps = []
        for p, _, f in walk(str(self._path.dir)):
            new_p = p[p.find('/'):]
            new_p = new_p[1:]
            self.deps += [Source(Path(p) / file, handler=FileHandler, dir=new_p)
                          for file in f
                          if Path(file).ext != 'tmpl']
            
    def build(self, _):
        return Template(file=str(self._path), filter=EncodeUnicode)

