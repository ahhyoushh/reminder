from abc import abstractproperty

from smallvectors import Vec
from smallvectors.core.mutability import Mutable
from smallshapes.core import Locatable, mLocatable


class Shape(Locatable):
    """
    Base class for all objects that have a definite shape.

    The shape does not have to be solid, e.g., a line can be a shape.
    """

    __slots__ = ()

    @abstractproperty
    def xmin(self):
        return NotImplemented

    @abstractproperty
    def xmax(self):
        return NotImplemented

    @abstractproperty
    def ymin(self):
        return NotImplemented

    @abstractproperty
    def ymax(self):
        return NotImplemented

    @property
    def pos_sw(self):
        return self._vec(self.xmin, self.ymin)

    @property
    def pos_se(self):
        return self._vec(self.xmax, self.ymin)

    @property
    def pos_nw(self):
        return self._vec(self.xmin, self.ymax)

    @property
    def pos_ne(self):
        return self._vec(self.xmax, self.ymax)

    @property
    def pos_right(self):
        return self._vec(self.xmax, self.pos.y)

    @property
    def pos_left(self):
        return self._vec(self.xmin, self.pos.y)

    @property
    def pos_top(self):
        return self._vec(self.pos.x, self.ymax)

    @property
    def pos_bottom(self):
        return self._vec(self.pos.x, self.ymin)

    # Vector setters: set the value of the given reference point
    pos_sw = pos_sw.setter(lambda obj, v: obj.imove(v - obj.pos_sw))
    pos_nw = pos_nw.setter(lambda obj, v: obj.imove(v - obj.pos_nw))
    pos_se = pos_se.setter(lambda obj, v: obj.imove(v - obj.pos_se))
    pos_ne = pos_ne.setter(lambda obj, v: obj.imove(v - obj.pos_ne))
    pos_top = pos_top.setter(lambda obj, v: obj.imove(v - obj.pos_up))
    pos_bottom = pos_bottom.setter(lambda obj, v: obj.imove(v - obj.pos_down))
    pos_right = pos_right.setter(lambda obj, v: obj.imove(v - obj.pos_right))
    pos_left = pos_left.setter(lambda obj, v: obj.imove(v - obj.pos_left))

    @property
    def aabb(self):
        return self._aabb(self.xmin, self.xmax, self.ymin, self.ymax)

    @property
    def rect_coords(self):
        return self.xmin, self.xmax, self.ymin, self.ymax

    @property
    def rect_shape(self):
        return self.xmax - self.xmin, self.ymax - self.ymin

    @property
    def rect(self):
        x, y = self.xmin, self.ymin
        return x, y, self.xmax - x, self.ymax - y

    @property
    def width(self):
        return self.xmax - self.xmin

    @property
    def height(self):
        return self.ymax - self.ymin

    @property
    def cbb(self):
        return self._circle(self.cbb_radius, self.pos)

    @abstractproperty
    def cbb_radius(self):
        return NotImplemented

    def rotate(self, rotation):
        """
        Return a copy of rotated by the given rotation.
        """

        if rotation:
            tname = type(self).__name__
            raise TypeError('%r objects do not implement rotations' % tname)
        return self.copy()

    def rotate_axis(self, rotation, axis):
        """
        Return a copy rotated by the given rotation.
        """

        rotated = self.rotate(rotation)
        delta = (axis - self.pos).irotate(rotation)
        return rotated.move_vec(delta)

    def rescale(self, scale, point=None):
        """
        Return a copy rescaled by the given scale factor around the center
        point.
        """

        tname = type(self).__name__
        raise TypeError('%r objects cannot be rescaled' % tname)

    def distance_point(self, point):
        """
        Return the distance of object to the given point. Return 0 if they
        intercept.
        """

        raise NotImplementedError

    def distance_circle(self, circle):
        """
        Return the distance to the given circle. Return 0 if both shapes
        intercept.
        """

        raise NotImplementedError

    def distance(self, other):
        """
        Return the distance between two objects. Return 0.0 if they intercept.
        """

        if isinstance(other, (Vec, tuple)):
            return self.distance_point(other)
        elif isinstance(other, self._circle):
            return self.distance_circle(other)
        else:
            t1 = type(self).__name__
            t2 = type(other).__name__
            raise TypeError('invalid distance test: %s vs %s' % (t1, t2))


class mShape(Shape, mLocatable, Mutable):
    """
    Mutable shape.
    """

    __slots__ = ()