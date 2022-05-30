import pytest

from lazyutils import lazy, lazy_shared, lazy_classattribute, delegate_to, delegate_ro, readonly, alias


#
# Lazy attribute
#
@pytest.fixture
def A():
    class A(object):
        L = []

        @lazy
        def b(self):
            self.L.append(1)
            return 2

        @lazy_shared
        def c(self):
            return 3.0

    return A


def test_lazy_attribute_is_cached(A):
    a = A()
    assert a.b == 2
    assert A.L == [1]
    assert a.b == 2
    assert A.L == [1]


def test_lazy_attribute_is_writable(A):
    a = A()
    a.b = 1
    assert a.b == 1
    assert A.L == []


def test_lazy_works_with_lambdas():
    class A:
        x = lazy(lambda self: 42)

    a = A()
    assert a.x == 42


def test_shared_lazy_accessor(A):
    a = A()
    b = A()
    assert a.c is b.c


def test_lazy_class_attribute():
    class A(object):
        @lazy_classattribute
        def b(self):
            return 1

        @lazy_classattribute
        def c(self):
            return 2
    a = A()
    assert a.b == 1
    assert A.c == 2
    assert a.c == 2

#
# Delegate to
#
@pytest.fixture
def B():
    class B(object):
        x = delegate_to('data')
        y = delegate_to('data', readonly=True)
        z = delegate_ro('data')

        def __init__(self, data):
            self.data = data

    return B


@pytest.fixture
def data_cls():
    class Data:
        def __init__(self, x, y, z):
            self.x = x
            self.y = y
            self.z = z

    return Data


def test_delegate_to_reads_data(B, data_cls):
    data = data_cls(1, 2, 3)
    b = B(data)
    assert b.x == 1
    assert b.y == 2


def test_delegate_ro_reads_data(B, data_cls):
    data = data_cls(1, 2, 3)
    b = B(data)
    assert b.z == 3


def test_delegate_to_can_write(B, data_cls):
    data = data_cls(1, 2, 3)
    b = B(data)
    b.x = 42
    assert b.x == 42


def test_delegate_ro_cannot_write(B, data_cls):
    data = data_cls(1, 2, 3)
    b = B(data)

    with pytest.raises(AttributeError):
        b.y = 42

    with pytest.raises(AttributeError):
        b.z = 42

    assert b.y == 2
    assert b.z == 3


#
# Aliases
#
@pytest.fixture
def C():
    class C(object):
        x = 1
        y = alias('x')
        z = readonly('y')

    return C


def test_alias_read(C):
    obj = C()
    assert obj.x == obj.y
    assert obj.y == obj.z


def test_alias_write(C):
    obj = C()
    obj.y = 42
    assert obj.x == obj.y
    assert obj.x == 42
    assert obj.y == 42


def test_readonly_cannot_write(C):
    obj = C()
    with pytest.raises(AttributeError):
        obj.z = 42

    assert obj.z == obj.x