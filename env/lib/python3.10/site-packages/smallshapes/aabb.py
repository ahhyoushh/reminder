from smallshapes import Convex
from smallvectors import dot, Vec
from smallvectors.core.mutability import Mutable, Immutable

direction_x = Vec(1, 0)
direction_y = Vec(0, 1)


class AABBAny(Convex):
    """
    Base class for AABB and mAABB.
    """

    __slots__ = ('xmin', 'xmax', 'ymin', 'ymax')

    _vec = Vec[2, float]

    @property
    def pos(self):
        x = (self.xmin + self.xmax) / 2
        y = (self.ymin + self.ymax) / 2
        return self._vec(x, y)

    @property
    def vertices(self):
        vec = self._vec
        return (
            vec(self.xmin, self.ymin), vec(self.xmax, self.ymin),
            vec(self.xmax, self.ymax), vec(self.xmin, self.ymax)
        )

    @property
    def cbb_radius(self):
        dx = self.xmax - self.xmin
        dy = self.ymax - self.ymin
        return self._sqrt(dx * dx + dy * dy) / 2

    @property
    def aabb(self):
        return self.immutable()

    @classmethod
    def from_coords(cls, xmin, xmax, ymin, ymax):
        """
        Creates a new AABB from xmin, xmax, ymin, ymax coordinates.

        This constructor do not accept alternative signatures and is slightly
        faster than the default one.
        """

        new = AABB.__new__(cls)
        new.xmin = xmin
        new.xmax = xmax
        new.ymin = ymin
        new.ymax = ymax
        if xmin > xmax:
            raise ValueError('xmax < xmin')
        if ymin > ymax:
            raise ValueError('ymax < ymin')
        return new

    def __init__(self, *args,
                 xmin=None, xmax=None, ymin=None, ymax=None,
                 bbox=None, rect=None, shape=None, pos=None):

        if args:
            self.xmin, self.xmax, self.ymin, self.ymax = args
        else:
            self.xmin, self.xmax, self.ymin, self.ymax = aabb_coords(
                xmin, xmax, ymin, ymax, rect, shape, pos
            )

    def __flatgetitem__(self, key):
        if key == 0:
            return self.xmin
        elif key == 1:
            return self.xmax
        elif key == 2:
            return self.ymin
        elif key == 3:
            return self.ymax
        else:
            raise IndexError(key)

    def __flatlen__(self):
        return 4

    def __flatiter__(self):
        yield self.xmin
        yield self.xmax
        yield self.ymin
        yield self.ymax

    def __repr__(self):
        data = '%.1f, %.1f, %.1f, %.1f' % self.rect_coords
        return '%s([%s])' % (type(self).__name__, data)

    def __iter__(self):
        yield self.xmin
        yield self.xmax
        yield self.ymin
        yield self.ymax

    def __len__(self):
        return 4

    def _eq(self, other):
        return (
            other.xmin == self.xmin and other.xmax == self.xmax and
            other.ymin == self.ymin and other.ymax == self.ymax
        )

    def area(self):
        return (self.xmax - self.xmin) * (self.ymax - self.ymin)

    def ROG_sqr(self):
        A, B = self.rect_shape
        return (A * A + B * B) / 12

    def SAT_directions(self, n):
        return [direction_x, direction_y]

    def SAT_shadows(self, n):
        points = [dot(n, p) for p in self.vertices]
        return min(points), max(points)

    def move_vec(self, vec):
        dx, dy = vec
        new = self.from_coords(self.xmin, self.xmax, self.ymin, self.ymax)
        new.xmin += dx
        new.xmax += dx
        new.ymin += dy
        new.ymax += dy
        return new

    def move_to_vec(self, vec):
        return self.move_vec(self.pos - vec)

    def rescale(self, scale):
        new = self.from_coords(self.xmin, self.xmax, self.ymin, self.ymax)
        x, y = self.pos
        dx, dy = self.shape
        dx *= scale / 2
        dy *= scale / 2
        new.xmin, new.xmax = x - dx, x + dx
        new.ymin, new.ymax = y - dy, y + dy
        return new

    def contains_point(self, point):
        x, y = point
        return ((self.xmin <= x <= self.xmax)
                and (self.ymin <= y <= self.ymax))

    def contains_aabb(self, other):
        return (
            self.xmin <= other.xmin and self.ymin <= other.ymin and
            self.xmax >= other.xmax and self.ymax <= other.ymax
        )

    def contains_circle(self, other):
        cpoint = self.contains_point
        x, y, xm, ym = other
        return (cpoint(x, y) and cpoint(x, ym)
                and cpoint(xm, y) and cpoint(xm, ym))

    def shadow_x(self):
        return (self.xmin, self.xmax)

    def shadow_y(self):
        return (self.ymin, self.ymax)


class AABB(AABBAny, Immutable):
    """
    A rectangular  "axis aligned bounding box".

    Attributes:
        xmin, xmax, ymin, ymax (float):
            AABB limits in x and y directions.
        vertices:
            Sequence of vertices that form the AABB. Starts with the 1st
            quadrant and runs counter clockwise.


    Example:
        Create an AABB by specifying its limits in the x and y directions

        >>> a = AABB(0, 50, 0, 100)
        >>> a.pos  # center point
        Vec(25, 50)
    """

    __slots__ = ()


class mAABB(AABBAny, Mutable):
    """
    Mutable version of AABB.
    """

    __slots__ = ()

    @AABBAny.pos.setter
    def pos(self, value):
        x, y = value - self.pos
        self.xmin += x
        self.xmax += x
        self.ymin += y
        self.ymax += y

    def __setitem_simple__(self, idx, value):
        if idx == 0:
            self.xmin = value
        elif idx == 0:
            self.xmax = value
        elif idx == 0:
            self.ymin = value
        elif idx == 0:
            self.ymax = value
        else:
            raise IndexError(idx)

    def copy(self):
        return self.from_coords(self.xmin, self.xmax, self.ymin, self.ymax)

    def imove_vec(self, vec):
        dx, dy = vec
        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymax += dy

    def imove_to_vec(self, vec):
        dx, dy = vec - self.pos
        self.xmin += dx
        self.xmax += dx
        self.ymin += dy
        self.ymin += dy

    def irotate(self, *args):
        raise ValueError('cannot rotate AABBs')


def aabb_coords(xmin=None, xmax=None, ymin=None, ymax=None,
                rect=None, shape=None, pos=None):
    """
    Return AABB's (xmin, xmax, ymin, ymax) from the given parameters.
    """

    if (xmin is not None) and (xmax is None):
        xmin, xmax, ymin, ymax = xmin
    elif shape is not None:
        pos = pos or (0, 0)
        dx, dy = shape
        x, y = pos
        xmin, xmax = x - dx / 2, x + dx / 2
        ymin, ymax = y - dy / 2, y + dy / 2
    elif rect is not None:
        xmin, ymin, dx, dy = rect
        xmax = xmin + dx
        ymax = ymin + dy
    elif None not in (xmin, xmax, ymin, ymax):
        pass
    else:
        msg = 'either shape, rect or AABB coordinates must be defined'
        raise TypeError(msg)

    return xmin, xmax, ymin, ymax


def aabb_rect(xmin=None, xmax=None, ymin=None, ymax=None,
              rect=None, shape=None, pos=None):
    """
    Return AABB's (xmin, ymin, width, height) from given parameters.
    """

    x, xmax, y, ymax = aabb_coords(xmin, xmax, ymin, ymax,
                                   rect, shape, pos)
    return x, y, xmax - x, ymax - y


def aabb_pshape(xmin=None, xmax=None, ymin=None, ymax=None,
                rect=None, shape=None, pos=None):
    """
    Return AABB's (pos, shape) from given parameters.
    """

    x, xmax, y, ymax = aabb_coords(xmin, xmax, ymin, ymax,
                                   rect, shape, pos)
    center = Vec((x + xmax) / 2.0, (y + ymax) / 2.0)
    shape = (xmax - x, ymax - y)
    return center, shape


def aabb_center(xmin=None, xmax=None, ymin=None, ymax=None,
                rect=None, shape=None, pos=None):
    """
    Return AABB's center position vector from given parameters.
    """

    xmin, xmax, ymin, ymax = aabb_coords(xmin, ymin, xmax, ymax,
                                         rect, shape, pos)
    return Vec((xmin + xmax) / 2, (ymin + ymax) / 2)


def aabb_shape(xmin=None, xmax=None, ymin=None, ymax=None,
               rect=None, shape=None, pos=None):
    """
    Return AABB's (width, height) vector from given parameters.
    """

    xmin, xmax, ymin, ymax = aabb_coords(xmin, ymin, xmax, ymax, rect,
                                         shape, pos)
    return xmax - xmin, ymax - ymin
