from smallshapes import PathAny, Path, mPath, center_of_mass
from smallshapes import center_of_mass


class CircuitAny(PathAny):
    """
    Base class for Circuit and mCircuit.
    """

    __slots__ = ()

    @property
    def pos(self):
        return center_of_mass(self)


class Circuit(CircuitAny, Path):
    """
    Circuit represents a closed path in space.

    Differently from polygons, paths can cross each other
    """

    __slots__ = ()


class mCircuit(CircuitAny, mPath):
    """
    A mutable circuit.
    """

    __slots__ = ()

    pos = mPath.pos