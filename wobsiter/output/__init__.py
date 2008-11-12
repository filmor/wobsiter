# 
# Copyright 2008 Benedikt Sauer
# 
# This file is part of Wobsiter.
#
# Wobsiter is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Wobsiter is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Wobsiter. If not, see <http://www.gnu.org/licenses/>.
# 
from urlparse import urlparse
from functools import partial
from .. import util

from file_handler import *

class Output(object):
    """Output class.

    Collects the output actions called in a SourceHandler's build method and
    commits them if all went well.
    It is /not/ atomic in commit!"""

    _queue = list()
    _created_items = set()
    _dir = ''

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
        self._dir = path
        return self._dir

    directory = property(get_directory, set_directory)

    def write_file(self, name, data):
        """Make a file from data in the current working directory."""
        path = util.join(self._dir, name)
        self._created_items.add(path)
        self._enqueue_action('write_file', path, data)
        return path

    # TODO Keine Pfade erlauben, nur Dateinamen angeben, auch Verzeichnisse
    #      kopieren.
    def copy_file(self, from_path, to_path=None):
        """Copy a file to to_path in the working directory."""
        path = util.join(self._dir, to_path or util.basename(from_path))
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

