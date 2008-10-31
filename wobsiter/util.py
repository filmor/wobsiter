import os, shutil

class lazy_property(object):
    def __init__(self, calculate_function):
        self._calculate = calculate_function

    def __get__(self, obj, _=None):
        if not hasattr(obj, '_lazy_property__value'):
            obj.__value = self._calculate(obj)
        return obj.__value

class rw_lazy_property(lazy_property):
    def __init__(self, calc, set_function):
        self._set = set_function
        super(rw_lazy_property, self).__init__(calc)

    def __set__(self, obj, val):
        self._set(obj, val)


# TODO Allow a __pre_init__ method to canonise the constructor arguments
class InternedMeta(type):
    def __init__(cls, name, bases, dct):
        super(InternedMeta, cls).__init__(name, bases, dct)

        if not hasattr(cls, '_InternedMeta__is_interned'):
            cls.__is_interned = True
            cls.__instances = {}

            old_new = cls.__new__

            def my_new(my_cls, *args, **kwargs):
                if my_cls is cls:
                    if args in cls.__instances:
                        instance = cls.__instances[args]
                    else:
                        instance = old_new(my_cls, *args, **kwargs)
                        cls.__instances[args] = instance
                else:
                    instance = old_new(my_cls, *args, **kwargs)
                return instance
            
            setattr(cls, '__new__', staticmethod(my_new))

# TODO
# def collect_garbage(self):


class Path(object):
    __metaclass__ = InternedMeta
    def __init__(self, path):
        if type(path) == Path:
            self._path = path._path
        else:
            assert type(path) == str or type(path) == unicode
            #TODO __pre_init__
            self._path = os.path.normpath(path)

    dir = property(lambda self: Path(self.dirname))
    dirname = property(lambda self: os.path.dirname(self._path))
    base = property(lambda self: Path(self.basename))
    basename = property(lambda self: os.path.basename(self._path))

    exists = property(lambda self: os.path.exists(self._path))
    isdir = property(lambda self: os.path.isdir(self._path))
    isfile = property(lambda self: os.path.isfile(self._path))
    ext = property(lambda self: os.path.splitext(self._path)[1][1:])
    without_ext = property(lambda self: os.path.splitext(self._path)[0])

    def __div__(self, other):
        if type(other) is Path:
            other = other._path
        return Path(os.path.join(self._path, other))

    __eq__ = lambda self, other: os.path.samefile(self, other)
    __str__ = lambda self: os.path.join(self._path)
    __repr__ = lambda self: "<%s: %s>" % (self.__class__.__name__, self._path)

def _mkfunc(sys_func, ret=None):
    def res(*args):
        new_args = (str(i) if type(i) == Path else i for i in args)
        return sys_func(*new_args)
    try:
        res.func_name = sys_func.func_name
        res.func_doc = sys_func.func_doc
    except AttributeError:
        pass
    return res

remove = _mkfunc(os.remove)
mkdir = _mkfunc(os.mkdir)
makedirs = _mkfunc(os.makedirs)
rmdir = _mkfunc(os.rmdir)
copy = _mkfunc(shutil.copyfile)
file = _mkfunc(file)
open = _mkfunc(open)

def glob(path):
    from glob import glob as std_glob
    return [ Path(i) for i in std_glob(str(path)) ]

