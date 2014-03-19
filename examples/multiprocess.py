#!/usr/bin/env python
from pyxmem import memorize
from multiprocessing import Pool, Manager
from utils import Timer


manager = Manager()
shared_cache = manager.dict()

@memorize(cache=shared_cache)
def foo(n):
    return n


@memorize(cache=shared_cache)
def bar(n):
    return n


N = 100000

print "Pool with shared dictionary"
pool = Pool(processes=4)
with Timer(verbose=True):
    pool.map(foo, xrange(N))

print "Single process with shared dictionary"
shared_cache.clear()
with Timer(verbose=True):
    map(foo, xrange(N))

print "Single process with standard dictionary"
with Timer(verbose=True):
    map(bar, xrange(N))
