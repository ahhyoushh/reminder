from smallshapes.tests import abstract as base
from smallshapes import Circle, mCircle


class TestCircle(base.TestMutability, base.TestSolid):
    base_cls = Circle
    base_args = (2.5, (0, 1))
    aabb_args = (0.5, (0.5, 1.5))

    def test_circle_construction(self):
        assert Circle(1) == Circle(1, (0, 0))
        assert Circle(1, (2, 3)).radius == 1
        assert Circle(1, (2, 3)).x == 2
        assert Circle(1, (2, 3)).y == 3

    def test_circle_repr(self):
        assert repr(Circle(1, (2, 3))) == 'Circle(1, (2, 3))'
        assert repr(mCircle(1, (2, 3))) == 'mCircle(1, (2, 3))'

