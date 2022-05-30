from smallshapes.core import Solid, mSolid


class Convex(Solid):
    """
    Base class for all convex shapes.
    """

    __slots__ = ()

    def contains_segment(self, segment):
        pt_test = self.contains_point
        pt1, pt2 = segment
        return pt_test(pt1) and pt_test(pt2)


class mConvex(Convex, mSolid):
    """
    Mutable convex.
    """

    __slots__ = ()