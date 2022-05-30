from smallshapes import Shape, mShape
from smallvectors import asvector
from smallvectors.core.mutability import Immutable


class SegmentAny(Shape):
    """
    Base class for Segment and mSegment.
    """

    __slots__ = ('_start', '_end')

    @property
    def start(self):
        return self._start

    @property
    def end(self):
        return self._end

    @property
    def pos(self):
        return (self._start + self._end) / 2

    @property
    def xmin(self):
        return min(self._start.x, self._end.x)

    @property
    def xmax(self):
        return max(self._start.x, self._end.x)

    @property
    def ymin(self):
        return min(self._start.y, self._end.y)

    @property
    def ymax(self):
        return max(self._start.y, self._end.y)

    @property
    def direction(self):
        return self.end - self.start

    @property
    def rect_shape(self):
        return (abs(self._start.x - self._end.x),
                abs(self._start.y - self._end.y))

    @property
    def cbb_radius(self):
        dx = (self._start.x - self._end.x) / 2
        dy = (self._start.y - self._end.y) / 2
        return self._sqrt(dx * dx + dy * dy)

    def __init__(self, start, end):
        self._start = asvector(start)
        self._end = asvector(end)

    def __iter__(self):
        yield self._start
        yield self._end

    def __len__(self):
        return 2

    def __flatiter__(self):
        yield self._start.x
        yield self._start.y
        yield self._end.x
        yield self._end.y

    def __flatlen__(self):
        return 4

    def __flatgetitem__(self, idx):
        if idx == 0:
            return self._start.x
        elif idx == 1:
            return self._start.y
        elif idx == 2:
            return self._end.x
        elif idx == 3:
            return self._end.y
        else:
            raise IndexError(idx)

    def move_to_vec(self, pos):
        u, v = self
        delta = pos - (u + v) / 2
        return type(self)(u + delta, v + delta)


class Segment(SegmentAny, Immutable):
    """
    A directed line segment from `start` point to `end` point.

    A segment is initialized from its end points:

    >>> obj = Segment((-1, 1), (1, 1))
    >>> obj.direction
    Vec(2, 0)
    """

    __slots__ = ()


class mSegment(SegmentAny, mShape):
    """
    A mutable Segment.
    """

    __slots__ = ()

    @SegmentAny.start.setter
    def start(self, value):
        self._start = self._asvector(value)

    @SegmentAny.end.setter
    def end(self, value):
        self._end = self._asvector(value)

    @SegmentAny.direction.setter
    def direction(self, value):
        self._end = self.start + self._asvector(value)

    @SegmentAny.pos.setter
    def pos(self, value):
        start, end = self
        pos = (start + end) / 2
        delta = value - pos
        self._start += delta
        self._end += delta

    def imove_vec(self, vec):
        self._start += vec
        self._end += vec

    def imove_to_vec(self, vec):
        self.imove_vec(vec - self.pos)
