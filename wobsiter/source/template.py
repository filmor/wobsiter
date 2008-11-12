from .. import util
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
        for p, _, files in walk(util.dirname(self._path)):
            new_p = p[p.find('/'):]
            new_p = new_p[1:]
            self.deps += [Source(util.join(p, f), handler=FileHandler,
                                 dir=new_p)
                          for f in files
                          if util.ext(f) != 'tmpl']

    def build(self, _):
        return Template(file=self._path, filter=EncodeUnicode)
