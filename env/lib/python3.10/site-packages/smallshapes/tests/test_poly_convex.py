from smallshapes.tests import test_poly as base
from smallshapes import ConvexPoly


class TestPolyConvex(base.TestPoly):
    base_cls = ConvexPoly
