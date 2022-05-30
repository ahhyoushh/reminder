from smallshapes import PolyAny, Convex, mPoly, mConvex
from smallvectors import Immutable
from smallvectors.core.mutability import Mutable


class ConvexPolyAny(PolyAny, Convex):
    """
    Base class for ConvexPoly and mConvexPoly.
    """

    __slots__ = ()

    def is_convex(self):
        True


class ConvexPoly(ConvexPolyAny, Immutable):
    """
    A convex polygon.
    """

    __slots__ = ()


class mConvexPoly(ConvexPolyAny, mPoly, mConvex):
    """
    A mutable convex polygon.
    """

    __slots__ = ()
