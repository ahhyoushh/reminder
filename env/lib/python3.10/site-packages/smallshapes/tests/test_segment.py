from smallshapes.tests import abstract as base
from smallshapes.segment import Segment, mSegment


class TestSegment(base.TestMutability, base.TestShape):
    base_cls = Segment
    base_args = (0, 1), (1, 2)
    aabb_args = (0, 1), (1, 2)
