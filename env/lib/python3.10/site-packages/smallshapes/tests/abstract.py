from numbers import Number

import pytest

import smallvectors.tests.base
from smallshapes import Circle, CircleAny
from smallvectors import simeq, Vec
from smallvectors.tests import abstract as base


def can_find_anytype():
    c = Circle(5, (0, 0))
    assert c.__anytype__ == CircleAny


class TestMutability(base.TestMutability):
    def test_mutable_serialize_to_args(self, mutable):
        assert tuple(mutable) == self.base_args

    def test_immutable_serialize_to_args(self, immutable):
        assert tuple(immutable) == self.base_args


class DisableMutabilityTests(base.DisableMutabilityTests):
    test_mutable_serialize_to_args = test_immutable_serialize_to_args = None


class TestBase(base.TestMutability,
               base.TestSequentiable,
               base.TestFlatable):
    @pytest.fixture
    def examples(self, mutable, immutable):
        return [mutable, immutable]


class TestLocatable(smallvectors.tests.base.ClassTester):
    @pytest.fixture
    def examples(self, obj):
        return [obj]

    def test_displacement_creates_a_new_object(self, obj):
        new = obj.move(1, 1)
        assert new is not obj

    def test_vec_displacement_creates_a_new_object(self, obj):
        new = obj.move_vec(Vec(1, 1))
        assert new is not obj

    def test_zero_displacement_does_not_change_type(self, examples):
        for x in examples:
            new = x.move(0, 0)
            assert type(x) is type(new)

    def test_zero_displacement_does_not_change_object(self, examples):
        for x in examples:
            assert x == x.move(0, 0)

    def test_displaced(self, obj):
        new = obj.move(10, 5)
        newpos = obj.pos + (10, 5)
        assert simeq(new.pos, newpos)

    def test_inplace_displacement_using_pos(self, mutable):
        newpos = mutable.pos + (10, 5)
        mutable.pos += (10, 5)
        assert simeq(mutable.pos, newpos)


class TestShape(TestLocatable):
    aabb_args = None

    def test_rect_coords(self, obj):
        xmin, xmax, ymin, ymax = obj.xmin, obj.xmax, obj.ymin, obj.ymax
        assert isinstance(xmin, Number), xmin
        assert isinstance(xmax, Number), xmax
        assert isinstance(ymin, Number), ymin
        assert isinstance(ymax, Number), ymax
        assert (xmin, xmax, ymin, ymax) == obj.rect_coords

    def test_aabb_consistency(self, obj):
        assert obj.xmin <= obj.xmax
        assert obj.ymin <= obj.ymax
        A, B = obj.rect_shape
        assert A >= 0
        assert B >= 0
        assert obj.cbb_radius > 0


class TestSolid(TestShape):
    def test_geometry_consistency(self, obj, tol):
        assert obj.area() > 0
        assert obj.ROG() > 0
        assert abs(obj.ROG_sqr() - obj.ROG() ** 2) < tol


        # def test_aabb_test(self):
        #     assert simeq(self.aabb_example.aabb, AABB(0, 1, 1, 2))
        #     assert simeq(self.aabb_mexample.aabb, AABB(0, 1, 1, 2))
        #
        # def test_displace_bounds(self):
        #     assert simeq(self.aabb_displaced.xmin, 1)
        #     assert simeq(self.aabb_displaced.xmax, 2)
        #     assert simeq(self.aabb_displaced.ymin, 2)
        #     assert simeq(self.aabb_displaced.ymax, 3)
        #
        # def test_mdisplace_bounds(self):
        #     assert simeq(self.aabb_mdisplaced.xmin, 1)
        #     assert simeq(self.aabb_mdisplaced.xmax, 2)
        #     assert simeq(self.aabb_mdisplaced.ymin, 2)
        #     assert simeq(self.aabb_mdisplaced.ymax, 3)
        #
        # def test_displace_shape(self):
        #     assert simeq(self.aabb_displaced.shape, (1, 1))
        #     assert simeq(self.aabb_displaced.width, 1)
        #     assert simeq(self.aabb_displaced.height, 1)
        #
        # def test_mdisplace_shape(self):
        #     assert simeq(self.aabb_mdisplaced.shape, (1, 1))
        #     assert simeq(self.aabb_mdisplaced.width, 1)
        #     assert simeq(self.aabb_mdisplaced.height, 1)
        #
        # def test_displace_points(self):
        #     assert simeq(self.aabb_displaced.pos_sw, (1, 2))
        #     assert simeq(self.aabb_displaced.pos_se, (2, 2))
        #     assert simeq(self.aabb_displaced.pos_nw, (1, 3))
        #     assert simeq(self.aabb_displaced.pos_ne, (2, 3))
        #
        # def test_mdisplace_points(self):
        #     assert simeq(self.aabb_mdisplaced.pos_sw, (1, 2))
        #     assert simeq(self.aabb_mdisplaced.pos_se, (2, 2))
        #     assert simeq(self.aabb_mdisplaced.pos_nw, (1, 3))
        #     assert simeq(self.aabb_mdisplaced.pos_ne, (2, 3))
