# -*- coding: utf-8 -*-
"""
pyxmem
~~~~~~


:copyright: (c) 2014 by Daniel Hennes
:license: TBD
"""

import hashlib
import pickle
import functools

import logging
logging.basicConfig(level=logging.INFO)  # DEBUG)
logger = logging.getLogger(__name__)


class Memorizer(object):
    """Caches a function's return value. If called with the
    same arguments, the cached value is returned and the function is
    not reevaluated.

    Uses a standard dictionary for caching.
    """

    _cache = dict()

    def __init__(self, cache=None):
        if cache is not None:
            self._cache = cache
        logger.debug("Created Memorizer with cache: %s : %s" %
                     (type(self._cache), self._cache))

    def __call__(self, func):
        """Returns cached result or calls functions and caches value."""
        self._func = func

        @functools.wraps(func)  # reset docstring and name
        def decorated(*args, **kwargs):
            key = self._get_key(*args, **kwargs)
            if key in self._cache:
                logger.debug("Retrieved result from cache: %s" % key)
                return self._cache[key]
            else:
                value = self._func(*args, **kwargs)
                self._cache[key] = value
                logger.debug("Stored result in cache: %s" % key)
                return value

        # FIXME: should the user have access to the cache like this?
        decorated._cache = self._cache
        return decorated

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


def memorize(*args, **kwargs):
    """Decorator short handle.
    Works for @memorize and @memorize() and @memorize(args, kwargs) alike.
    """
    if not kwargs and len(args) == 1 and callable(args[0]):
        return Memorizer()(args[0])
    else:
        return Memorizer(*args, **kwargs)
