from urlparse import urlsplit
from ..util import Path, rw_lazy_property, mkdir, file, remove, copy
import cPickle as pickle
from shutil import rmtree

class FileHandler(object):
    """Handler for filesystem output."""
    TYPE = 'file'
    EXISTING_FILES_NAME = '.wobsite_files'
    def __init__(self, url):
        _, host, path, _, _ = urlsplit(url)
        path = Path(host) / path
        self._path = lambda p: path / p

    def get_existing_items(self):
        """Load the last written items in the directory structure."""
        try:
            return pickle.load(file(self._path(self.EXISTING_FILES_NAME)))
        except IOError:
            return set()

    def set_existing_items(self, new_set):
        """Rewrite the set of items."""
        assert type(new_set) is set
        pickle.dump(new_set, file(self._path(self.EXISTING_FILES_NAME), 'w'))

    existing_items = rw_lazy_property(get_existing_items, set_existing_items)

    def copy_file(self, from_path, to_path):
        """Copy a file into the output directory."""
        copy(from_path, self._path(to_path))
        return to_path

    def write_file(self, path, data):
        """Write a file from data to path."""
        file(self._path(path), 'w').write(data)
        return path

    def create_directory(self, path):
        """Create the directory at path and wipe out anything that stands
        prevents us from doing that."""
        if not self._path(path).exists:
            self.create_directory(path.dir)
            mkdir(self._path(path))
        elif not self._path(path).isdir:
            self.remove_item(path)
            mkdir(self._path(path))

    def remove_item(self, path):
        """Remove item at path, regardless if it's a file or directory."""
        path = self._path(path)
        if path.isfile:
            remove(str(path))
        elif path.isdir:
            rmtree(str(path))

