from os import remove, extsep, sep, mkdir
from shutil import rmtree, copyfile as copy
from os.path import *

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

def normalize(path):
    return normcase(normpath(expanduser(path)))

def ext(path):
    _, res = splitext(path)
    return res.lstrip(extsep)

def without_ext(path):
    res, _ = splitext(path)
    return res

def change_ext(path, ext):
    return without_ext(path) + extsep + ext


class InternedMeta(type):
    def __init__(cls, name, bases, dct):
        super(InternedMeta, cls).__init__(name, bases, dct)

        if not hasattr(cls, '_InternedMeta__is_interned'):
            cls.__is_interned = True
            cls.__is_reused = False
            cls.__instances = {}

            old_new = cls.__new__
            old_init = cls.__init__

            def my_init(self, *args, **kwargs):
                if not self.__is_reused:
                    old_init(self, *args, **kwargs)

            def my_new(my_cls, *args, **kwargs):
                if my_cls is cls:
                    identifier = cls.__id_args__(*args, **kwargs)
                    if identifier in cls.__instances:
                        instance = cls.__instances[identifier]
                        instance.__is_reused = True
                    else:
                        instance = old_new(my_cls, *args, **kwargs)
                        cls.__instances[identifier] = instance
                else:
                    instance = old_new(my_cls, *args, **kwargs)
                return instance
            
            setattr(cls, '__new__', staticmethod(my_new))
            setattr(cls, '__init__', my_init)

        def __id_args__(cls, *args, **kwargs):
            return (args, kwargs)

# TODO
# def collect_garbage(self):

