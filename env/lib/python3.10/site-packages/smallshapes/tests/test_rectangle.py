from smallshapes.tests import test_poly_convex as base
from smallshapes import Rectangle, mRectangle


class TestRectangle(base.TestPolyConvex):
    base_cls = Rectangle
    base_args = 0, 2, 0, 1

    def test_immutable_serialize_to_args(self):
        pass

    def test_mutable_serialize_to_args(self):
        pass

    def test_inplace_displacement_using_pos(self, args):
        #TODO: fixme
        pass
