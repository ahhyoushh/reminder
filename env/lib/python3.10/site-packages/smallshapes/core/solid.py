from abc import abstractmethod

from smallvectors import Vec
from smallshapes.core import Shape, mShape


class Solid(Shape):
    """
    Solid is a closed shape with a definite interior area.
    """

    __slots__ = ()

    @abstractmethod
    def area(self):
        """
        Return object's surface area.
        """

        return NotImplemented

    @abstractmethod
    def ROG_sqr(self):
        """
        Radius of gyration squared.
        """

        return NotImplemented

    def ROG(self):
        """
        Radius of gyration.
        """

        return self._sqrt(self.ROG_sqr())

    def contains_point(self, point):
        """
        Tests if the given point is completely contained by object.
        """

        raise NotImplementedError

    def contains_circle(self, circle):
        """
        Tests if the given circle is completely contained by object.
        """

        raise NotImplementedError

    def contains_segment(self, segment):
        """
        Tests if the given line segment is completely contained by object.
        """

        raise NotImplementedError

    def __contains__(self, other):
        if isinstance(other, (Vec, tuple)):
            return self.contains_point(other)
        elif isinstance(other, self._circle):
            return self.contains_circle(other)
        else:
            t1 = type(self).__name__
            t2 = type(other).__name__
            raise TypeError('invalid containment test: %s vs %s' % (t1, t2))


class mSolid(Solid, mShape):
    """
    Mutable solid.
    """

    __slots__ = ()