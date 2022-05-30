from smallshapes.tests import abstract as base
from smallshapes import AABB, mAABB


class TestAABB(base.TestMutability, base.TestSolid):
    base_cls = AABB
    base_args = (0, 1, 0, 2)
    aabb_args = (0, 1, 1, 2)
