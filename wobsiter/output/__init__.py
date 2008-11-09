from urlparse import urlparse
from functools import partial
from ..util import Path

from file_handler import *

class Output(object):
    """Output class.

    Collects the output actions called in a SourceHandler's build method and
    commits them if all went well."""

    _queue = list()
    _created_items = set()
    _dir = Path('')

    def __init__(self, url, *opts):
        type = urlparse(url)[0]
        self.handler = globals()[type.capitalize() + "Handler"](url, *opts)

    def __enter__(self):
        return self

    def __exit__(self, type, value, traceback):
        if type is None:
            self.commit()

    def _enqueue_action(self, name, *args, **kwargs):
        """Append an action to the action queue."""
        self._queue.append(partial(getattr(self.handler, name), *args, **kwargs))

    def get_directory(self):
        """Return the current working directory."""
        return self._dir

    def set_directory(self, path):
        """Set current working directory in the output structure."""
        self._enqueue_action('create_directory', path)
        self._created_items.add(path)
        self._dir = Path(path)
        return self._dir

    directory = property(get_directory, set_directory)

    def write_file(self, name, data):
        """Make a file from data in the current working directory."""
        path = self._dir / name
        self._created_items.add(path)
        self._enqueue_action('write_file', path, data)
        return path

    # TODO Keine Pfade erlauben, nur Dateinamen angeben, auch Verzeichnisse
    #      kopieren.
    def copy_file(self, from_path, to_path=None):
        """Copy a file to to_path in the working directory."""
        path = self._dir / (to_path or Path(from_path).base)
        self._created_items.add(path)
        self._enqueue_action('copy_file', from_path, path)
        return path

    def commit(self):
        """Commit the changes in the queue."""
        for action in self._queue:
            action()
            # TODO
            # self._created_items.add(created)
#        for i in self._created_items:
#        for i in self.handler.existing_items.difference(self._created_items):
#            print "Removing ", i
#            self.handler.remove_item(i)
        self.handler.existing_items = self._created_items

