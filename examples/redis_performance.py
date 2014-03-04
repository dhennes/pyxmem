#!/usr/bin/env python
from pyxmem.redisdb import memorize as redmem
from pyxmem import memorize
from utils import Timer


@redmem
def fibonacci_redis(n):
    """Returns the n-th fibonacci number."""
    if n in (0, 1):
        return n
    return fibonacci_redis(n-1) + fibonacci_redis(n-2)


@memorize
def fibonacci(n):
    """Returns the n-th fibonacci number."""
    if n in (0, 1):
        return n
    return fibonacci(n-1) + fibonacci(n-2)


fibonacci_redis._cache.clear()
with Timer(verbose=True) as t:
    for n in xrange(1000):
        fibonacci_redis(n)

with Timer(verbose=True) as t:
    for n in xrange(1000):
        fibonacci_redis(n)

with Timer(verbose=True) as t:
    for n in xrange(1000):
        fibonacci(n)

with Timer(verbose=True) as t:
    for n in xrange(1000):
        fibonacci(n)
