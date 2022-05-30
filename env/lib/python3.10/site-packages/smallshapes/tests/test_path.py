from smallshapes.tests import abstract as base
from smallshapes import Path, mPath


class TestPath(base.TestMutability, base.TestShape):
    base_cls = Path
    base_args = (0, 0), (1, 1), (2, 0)

