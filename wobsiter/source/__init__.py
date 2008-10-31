from contextlib import contextmanager
from ..util import InternedMeta, Path, lazy_property

class Source(object):
    __metaclass__ = InternedMeta
    def __init__(self, path, dir='', handler=None, *args, **kwargs):
        self._dir = Path(dir)
        self._path = path
        self._is_built = False
        if not handler:
            handler = _handlers[path.ext]
        self.handler = handler(path, *args, **kwargs)

    def __call__(self, output):
        if not self._is_built:
            if hasattr(self.handler, 'deps'):
                for source in self.handler.deps:
                    source(output)
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

