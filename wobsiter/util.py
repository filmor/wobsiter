import os

class lazy_property(object):
    def __init__(self, calculate_function):
        self._calculate = calculate_function

    def __get__(self, obj, _=None):
        if obj is None:
            return self
        value = self._calculate(obj)
        setattr(obj, self._calculate.func_name, value)
        return value


# TODO Allow a __pre_init__ method to canonise the constructor arguments
class InternedMeta(type):
    def __init__(cls, name, bases, dct):
        super(InternedMeta, cls).__init__(name, bases, dct)

        if not hasattr(cls, '_InternedMeta__is_interned'):
            cls.__is_interned = True
            cls.__instances = {}

            old_new = cls.__new__

            def my_new(my_cls, *args):
                if my_cls is cls:
                    if args in cls.__instances:
                        instance = cls.__instances[args]
                    else:
                        instance = old_new(my_cls, *args)
                        cls.__instances[args] = instance
                else:
                    instance = old_new(my_cls, *args)
                return instance
            
            setattr(cls, '__new__', staticmethod(my_new))

# TODO
# def collect_garbage(self):


class Path(object):
    __metaclass__ = InternedMeta
    def __init__(self, path):
        assert type(path) == str or type(path) == unicode
        #TODO __pre_init__
        self._path = os.path.normpath(path)

    dir = property(lambda self: Path(self.dirname))
    dirname = property(lambda self: os.path.dirname(self._path))
    base = property(lambda self: Path(self.basename))
    basename = property(lambda self: os.path.basename(self._path))

    def __div__(self, other):
        if type(other) is Path:
            other = other._path
        return Path(os.path.join(self._path, other))

    __eq__ = lambda self, other: os.path.samefile(self, other)

    __str__ = lambda self: os.path.join(self._path)

    __repr__ = lambda self: "<%s: %s>" % (self.__class__.__name__, self._path)

