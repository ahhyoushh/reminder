from smallshapes import aabb_coords
from smallshapes.poly_convex import ConvexPolyAny
from smallvectors import Immutable
from smallvectors.core.mutability import Mutable


class RectangleAny(ConvexPolyAny):
    """
    Base class for Rectangle and mRectangle.
    """

    __slots__ = ('theta',)

    def __init__(self, *args, **kwds):
        self.theta = 0.0
        theta = kwds.pop('theta', 0.0)
        xmin, xmax, ymin, ymax = aabb_coords(*args, **kwds)
        vertices = [(xmax, ymin), (xmax, ymax), (xmin, ymax), (xmin, ymin)]
        super().__init__(*vertices)
        if theta:
            self.rotate(theta)


class Rectangle(RectangleAny, Immutable):
    """
    A rectangle.
    """

    __slots__ = ()


class mRectangle(RectangleAny, Mutable):
    """
    A mutable rectangle.
    """

    __slots__ = ()