import functools

from smallvectors import asvector, Vec, Point


def accept_vec_args(func, single=True):
    """
    Decorator that transforms a method that only accept vector inputs to
    a function that accepts both coordinates or vectors.
    """

    # Single methods receive a single vec argument
    if not complex:
        @functools.wraps(func)
        def decorated_accept_vec_args(self, *args):
            if len(args) == 1:
                return func(self, asvector(args[0]))
            else:
                return func(self, asvector(args))

    # May have extra positional and keyword arguments
    else:
        @functools.wraps(func)
        def decorated_accept_vec_args(self, *args, **kwargs):
            if isinstance(args[0], (Vec, Point, tuple)):
                vec, *args = args
            else:
                x, y, *args = args
                vec = self._vec(x, y)
            return func(self, vec, *args, **kwargs)

    return decorated_accept_vec_args
