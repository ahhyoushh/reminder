from smallshapes import Solid, CircuitAny, Circuit, mCircuit, ROG_sqr, area, \
    mSolid
from smallvectors import Vec

Vec = Vec[2, float]


class PolyAny(CircuitAny, Solid):
    """
    Base class for Poly and mPoly.
    """

    __slots__ = ()

    def is_simple(self):
        True

    def ROG_sqr(self, axis=None):
        return ROG_sqr(self, axis)

    def area(self):
        return area(self)


class Poly(PolyAny, Circuit):
    """
    Generic polygon class.

    The sides of a simple polygon never cross each other.
    """

    __slots__ = ()


class mPoly(PolyAny, mCircuit, mSolid):
    """
    A mutable simple polygon.
    """

    __slots__ = ()
