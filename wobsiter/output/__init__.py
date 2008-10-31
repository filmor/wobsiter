from exceptions import Exception
from urlparse import urlparse
from functools import partial
from ..util import Path

from file_handler import *

class FileExistsError(Exception):
    def __init__(self, name):
        self.message = name

class Output(object):
    _queue = list()
    _created_items = set()
    _dir = Path('')

    def __init__(self, url, *opts):
        type = urlparse(url)[0]
        self.handler = globals()[type.capitalize() + "Handler"](url)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            self.commit()

    def _enqueue_action(self, name, *opts):
        self._queue.append(partial(getattr(self.handler, name), *opts))

    def set_directory(self, path):
        self._enqueue_action('create_directory', path)
        self._created_items.add(path)
        self._dir = Path(path)

    def write_file(self, name, data):
        path = self._dir / name
        print 'Writing File to ', path
        self._created_items.add(path)
        self._enqueue_action('write_file', path, data)

    def copy_file(self, from_, to=None):
        path = self._dir / (to if to else Path(from_).base)
        self._created_items.add(path)
        self._enqueue_action('copy_file', from_, path)

    def commit(self):
        for action in self._queue:
            created = action()
            # self._created_items.add(created)
        for i in self._created_items:
            print "Created ", i
#        for i in self.handler.existing_items.difference(self._created_items):
#            print "Removing ", i
#            self.handler.remove_item(i)
        self.handler.existing_items = self._created_items

