from smallvectors import Immutable
from smallshapes import ConvexPolyAny, mConvexPoly


class TriangleAny(ConvexPolyAny):
    """
    Base class for Triangle and mTriangle.
    """
    __slots__ = ()


class Triangle(TriangleAny, Immutable):
    """
    A triangle.
    """

    __slots__ = ()


class mTriangle(TriangleAny, mConvexPoly):
    """
    A mutable triangle.
    """

    __slots__ = ()
