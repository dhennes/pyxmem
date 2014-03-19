#!/usr/bin/env python
from pyxmem import memorize


@memorize
def fibonacci(n):
    """Returns the n-th fibonacci number."""
    print ".",
    if n in (0, 1):
        return n
    return fibonacci(n-1) + fibonacci(n-2)


d = {}
@memorize(cache=d)
def identity(n):
    """Returns the input."""
    print ".",
    return n


# computer first 10 fibonacci numbers
for n in xrange(10):
    print fibonacci(n)

# same, now loaded from cache
for n in xrange(10):
    print fibonacci(n)

# same, now loaded from cache
for n in xrange(10):
    print identity(n)

# same, now loaded from cache
for n in xrange(10):
    print identity(n)

print d.keys()


# TODO: write tests for:
# * recursion
# * correct caching
# * number of function calls
# * hash consistency
