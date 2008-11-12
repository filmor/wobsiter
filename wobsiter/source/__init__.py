from contextlib import contextmanager
from .. import util

class Source(object):
    __metaclass__ = util.InternedMeta
    
    _is_built = False

    @staticmethod
    def __id_args__(path, dir='', handler=None, *args, **kwargs):
        return (util.normalize(path), util.normalize(dir))

    def __init__(self, path, dir='', handler=None, *args, **kwargs):
        self._dir = util.normalize(dir)
        self._path = util.normalize(path)
        if not handler:
            handler = _handlers[util.ext(self._path)]
        self.handler = handler(self._path, *args, **kwargs)

    def __call__(self, output):
        if not self._is_built:
            if hasattr(self.handler, 'deps'):
                for source in self.handler.deps:
                    source(output)
            print 'Building %s using %s' \
                    % (self._path, self.handler.__class__.__name__)
            output.set_directory(self._dir)
            self.result = self.handler.build(output)
            self._is_built = True

    def __repr__(self):
        return "<Source: '%s' with %s>" \
                    % (self._path, self.handler.__class__.__name__)


from rst import RstHandler
from template import TemplateHandler
from menu import MenuHandler

_handlers = {
        'tmpl' : TemplateHandler,
        'txt' : RstHandler,
        'menu' : MenuHandler,
        }

