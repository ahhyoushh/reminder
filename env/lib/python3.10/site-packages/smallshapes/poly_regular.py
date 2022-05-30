from math import pi, sin

from smallshapes.poly_convex import ConvexPolyAny
from smallvectors import Rotation2d, Vec, Immutable
from smallvectors.core.mutability import Mutable


class RegularPolyAny(ConvexPolyAny):
    """
    Base class for RegularPoly and mRegularPoly.
    """

    __slots__ = ()

    def __init__(self, N, length, theta=None, pos=None):
        alpha = pi / N
        R = Rotation2d(2 * alpha)
        p = Vec(length / (2 * sin(alpha)), 0)
        vertices = []
        for _ in range(N):
            vertices.append(p)
            p = R * p
        super(RegularPolyAny, self).__init__(vertices)

        # Altera posição e ângulo
        if pos is not None:
            self += pos
        if theta is not None:
            self.rotate(theta)


class RegularPoly(RegularPolyAny, Immutable):
    """
    A regular polygon with N sides.
    """

    __slots__ = ()


class mRegularPoly(RegularPolyAny, Mutable):
    """
    A mutable regular polygon.
    """

    __slots__ = ()