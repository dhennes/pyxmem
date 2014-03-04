# -*- coding: utf-8 -*-
"""
pyxmem.redis
~~~~~~~~~~~~
Redis backend for pyxmem.

:copyright: (c) 2014 by Daniel Hennes
:license: TBD
"""

from pyxmem import Memorizer
import redis
import pickle  # TODO: investigate if JSON is faster / but limited

REDIS_PREFIX = "pyxmem:"


class RedisCache(object):
    """Redis cache."""

    # TODO: keep interface as close as possible to dictionary
    # TODO: look at redis-collections

    def __init__(self):
        self._redis = redis.Redis()
        self._prefix = REDIS_PREFIX

    def __contains__(self, key):
        return self._redis.exists(self._prefix + key)

    def __setitem__(self, key, value):
        self._redis.set(self._prefix + key, pickle.dumps(value))

    def __getitem__(self, key):
        return pickle.loads(self._redis.get(self._prefix + key))

    def __iter__(self):
        return iter(self._redis.keys())

    def __len__(self):
        return len(self._redis.keys())

    def keys(self):
        return self._redis.keys(self._prefix + "*")

    def values(self):
        return [self[key] for key in self]

    def clear(self):
        for key in self._redis.keys(self._prefix + "*"):
            self._redis.delete(key)


class RedisMemorizer(Memorizer):
    _cache = RedisCache()

# decorator short handle
memorize = RedisMemorizer
