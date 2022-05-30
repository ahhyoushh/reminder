from abc import abstractproperty, abstractmethod

from smallshapes.core import SmallshapesBase
from smallshapes.utils import accept_vec_args
from smallvectors import aspoint


class Locatable(SmallshapesBase):
    """
    Base class for all geometric objects that have a location in space.

    Subclasses must define a `pos` attribute as a vector with the center point
    coordinates and a few methods that implement space translations.

    displaced_by_vector_to (abstract):
        Return a copy of with the center point move to the given position
        vector. This method can assume that the input is a Vec[n, float] object
        and may perform any optimizations based in this assumption. Users should
        generally use the locatable.displaced_to() method.
    move_vec:
        Similar to `displaced_by_vector_to`, but uses relative displacements.
    """

    __slots__ = ()

    @property
    def center(self):
        """
        Object's center point.

        Similar to obj.pos, but while the first is a Vec, obj.center is a Point.
        """

        return aspoint(self.pos)

    @abstractproperty
    def pos(self):
        """
        Vector to object's center position.
        """

        raise NotImplementedError

    @accept_vec_args
    def move(self, vec):
        """
        Return a copy displaced by the given amount.

        Accepts a vector input or coordinates.
        """

        return self.move_vec(vec)

    def move_vec(self, vec):
        """
        Return a copy displaced by the given amount.
        """

        return self.move_to(vec + self.pos)

    @accept_vec_args
    def move_to(self, vec):
        """
        Return a copy displaced to reach the given final position.

        Accepts a vector input or coordinates.
        """

        return self.move_to_vec(vec)

    @abstractmethod
    def move_to_vec(self, vec):
        """
        Return a copy displaced to reach the given final position.
        """

        self.imove_vec(vec - self.pos)


class mLocatable(Locatable):
    """
    Mutable interface for Locatable elements.
    """

    __slots__ = ()

    @accept_vec_args
    def imove(self, vec):
        """
        Displace object position by vec. Changes are done *INPLACE*.

        Accepts a vector input or coordinates.
        """

        self.imove_vec(self.pos + vec)

    def imove_vec(self, vec):
        """
        Displace object position by vec. Changes are done *INPLACE*.
        """

        self.imove_to_vec(self.pos + vec)

    @accept_vec_args
    def imove_to(self, vec):
        """
        Sets new object position *INPLACE*.
        """

        self.imove_to_vec(vec)

    @abstractmethod
    def imove_to_vec(self, vec):
        """
        Sets new object position *INPLACE*.
        """

        return NotImplemented