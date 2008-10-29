import cPickle as pickle

from exceptions import Exception

class FileExistsError(Exception):
    def __init__(self, name):
        self.message = name


# TODO - Atomic, don't do anything before commit! (Append actions(!) to queue)
#      - Handle directories properly
class Output(object):
    _queue = list()
    _file_set = set()
    def __init__(self, path):
        self._path = path
        try:
            self._existing_files = pickle.load(path / '.wobsite_files')
        except:
            self._existing_files = set()

        assert type(self._existing_files) is set

    def __enter__(self):
        return self

    def __exit__(self):
        self.commit()

    def _make_dirs(self, path):
        path = self._path / path
        if path.exists and not path.isdir:
            path.remove()
        if not path.exists:
            self._make_dirs(path.dir)
            path.mkdir()

    def write(self, to_path, data):
        self._make_dirs(to_path.dir)
        path = self._path / to_path
        if path in self._file_set:
            raise FileExistsError(name)
        else:
            self._file_set.add(path)
            file(str(path), 'w').write(data)

    def copy_file(self, from_path, to_path):
        self._make_dirs(to_path.dir)
        path = self._path / to_path
        if path.exists:
            path.remove()
        from_path.copy_to(path)

    def copy_dir(self, from_path, to_path):
        # Walk from_path, copy_file für jedes Element
        pass

    def commit(self):
        # for i in self._queue:
        #    self._file_set.update(set(i()))
        for i in self._existing_files.difference(self._file_set):
            i.remove()
        pickle.dump(str(self._path / '.wobsite_files'), self._file_set)

