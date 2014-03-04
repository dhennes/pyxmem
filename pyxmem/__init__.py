# -*- coding: utf-8 -*-
"""
pyxmem
~~~~~~


:copyright: (c) 2014 by Daniel Hennes
:license: TBD
"""

import hashlib
import pickle


class Memorizer(object):
    """Caches a function's return value. If called with the
    same arguments, the cached value is returned and the function is
    not reevaluated.

    Uses a standard dictionary for caching.
    """

    _cache = dict()

    def __init__(self, func):
        self._func = func
        self.__name__ = func.__name__
        self.__doc__ = func.__doc__
        self.__repr__ = func.__repr__

    def __call__(self, *args, **kwargs):
        """Returns cached result or calls functions and caches value."""
        key = self._get_key(*args, **kwargs)
        if key in self._cache:
            return self._cache[key]
        else:
            value = self._func(*args, **kwargs)
            self._cache[key] = value
            return value

    def _get_key(self, *args, **kwargs):
        """Computes a hash using function name, args and kwargs."""
        fname = self._func.__name__

        if not args and not kwargs:
            return fname

        # hash args and sorted list of kwargs
        argskwargs = (args, kwargs.items().sort())
        # TODO: check if hashable
        # TODO: hash source code of function? what if the function calls other
        # functions? do we hash all of it?
        # all good questions for reproducible science
        hash = hashlib.md5(pickle.dumps(argskwargs)).hexdigest()
        return "%s:%s" % (fname, hash)

#    def __get__(self, obj, objtype):
#        '''Support instance methods.'''
#        return functools.partial(self.__call__, obj)


# decorator short handle
memorize = Memorizer
