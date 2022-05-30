from math import pi, sqrt

from smallshapes import Convex, mConvex
from smallvectors.core.mutability import Immutable
from smallshapes.functions import simplify_number
from smallvectors import dot, Vec

SQRT_HALF = 1 / sqrt(2)


class CircleAny(Convex):
    """
    Base class for Circle and mCircle
    """

    __slots__ = ('_radius', '_x', '_y')
    _vec = Vec[2, float]

    @property
    def radius(self):
        return self._radius

    @property
    def pos(self):
        return self._vec(self._x, self._y)

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def aabb(self):
        r, x, y = self._radius, self._x, self._y
        return self._aabb(x - r, x + r, y - r, y + r)

    @property
    def xmin(self):
        return self._x - self._radius

    @property
    def xmax(self):
        return self._x + self._radius

    @property
    def ymin(self):
        return self._y - self._radius

    @property
    def ymax(self):
        return self._y + self._radius

    @property
    def cbb(self):
        return self.immutable()

    @property
    def cbb_radius(self):
        return self._radius

    def __init__(self, radius, pos=(0, 0)):
        self._radius = radius
        self._x, self._y = pos

    def __len__(self):
        return 2

    def __iter__(self):
        yield self._radius
        yield self._vec(self._x, self._y)

    def __repr__(self):
        tname = type(self).__name__
        r, x, y = map(simplify_number, self.flat)
        return '%s(%s, (%s, %s))' % (tname, r, x, y)

    def __flatgetitem__(self, key):
        if key == 0:
            return self._radius
        elif key == 1:
            return self._x
        elif key == 2:
            return self._y
        else:
            raise IndexError(key)

    def __flatlen__(self):
        return 3

    def __flatiter__(self):
        yield self._radius
        yield self._x
        yield self._y

    def move_to_vec(self, vec):
        return type(self)(self._radius, vec)

    def area(self):
        return pi * self._radius * self._radius

    def ROG_sqr(self):
        return self._radius * self._radius / 2

    def ROG(self):
        return self._radius * SQRT_HALF

    def SAT_directions(self, n):
        return []

    def shadow(self, n):
        p0 = dot(self.pos, n)
        r = self._radius
        return p0 - r, p0 + r

    def distance_circle(self, other):
        distance = self.pos.distance(other.pos)
        sum_radius = self._radius + other.radius
        return max(distance - sum_radius, 0)

    def contains_circle(self, other):
        d_center = abs(other.pos - self.pos)
        return self._radius - other._radius - d_center > 0

    def contains_point(self, point):
        return self.pos.distance(point) <= self._radius


class Circle(CircleAny, Immutable):
    """
    A circle of given radius and position `pos`.
    """

    __slots__ = ()


class mCircle(CircleAny, mConvex):
    """
    A mutable circle.
    """

    __slots__ = ()

    def __flatsetitem__(self, key, value):
        if key == 0:
            self._radius = value
        elif key == 1:
            self._x = value
        elif key == 2:
            self._y = value
        else:
            raise IndexError(key)

    @Circle.radius.setter
    def radius(self, value):
        self._radius = float(value)

    @Circle.pos.setter
    def pos(self, value):
        self._x, self._y = value

    def imove_to_vec(self, vec):
        self._x, self._y = vec
