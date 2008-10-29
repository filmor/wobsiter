from glob import glob
import os

from docutils import core

import util

from handlers import SourceHandler


# TODO - SourceHandler statt abgeleiteter Klasse
#      - SourceHandler handhabt den Kram dann anständig
class Source(object):
    __metaclass__ = util.InternedMeta
    def __init__(self, path, handler=SourceHandler):
        self._handler = handler(path)
        self._deps = self._handler.deps

    def has_changed(self):
        return True # self._handler.has_changed()

    def build(output):
        for i in self._deps:
            i.build(output)
        try:
            self.handler.build(output)
        except AttributeError:
            pass

