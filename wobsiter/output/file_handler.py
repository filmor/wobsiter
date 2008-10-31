from urlparse import urlsplit
from ..util import Path, rw_lazy_property, mkdir, file, rmdir, remove, copy
import cPickle as pickle
from shutil import rmtree

class FileHandler(object):
    TYPE = 'file'
    EXISTING_FILES_NAME = '.wobsite_files'
    def __init__(self, url):
        _, host, path, _, _ = urlsplit(url)
        path = Path(host) / path
        self._path = lambda p: path / p

    def get_existing_items(self):
        try:
            return pickle.load(file(self._path(self.EXISTING_FILES_NAME)))
        except:
            return set()

    def set_existing_items(self, new_set):
        assert type(new_set) is set
        pickle.dump(new_set, file(self._path(self.EXISTING_FILES_NAME), 'w'))

    existing_items = rw_lazy_property(get_existing_items, set_existing_items)

    copy_file = lambda self, from_, to: copy(from_, self._path(to)) and to
    write_file = lambda self, to, data: file(self._path(to), 'w').write(data) and to

    def create_directory(self, path):
        if not self._path(path).exists:
            self.create_directory(path.dir)
            mkdir(self._path(path))
        elif not self._path(path).isdir:
            self.remove_item(path)
            mkdir(self._path(path))

    def remove_item(self, path):
        print path
        rmtree(str(self._path(path)))

    make_dir = lambda self, path: mkdir(self._path(path)) and path
    remove_dir = lambda self, path: rmdir(self._path(path)) and path

    def type_of(self, path):
        if not path.exists:
            return None
        elif path.isdir:
            return DIRECTORY
        elif path.isfile:
            return FILE
        else:
            return OTHER

