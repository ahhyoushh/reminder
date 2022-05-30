from smallshapes import Shape, mShape
from smallvectors import Vec, Immutable


class PathAny(Shape):
    """
    Base class for Path and mPath.
    """

    __slots__ = ('_data',)

    @property
    def pos(self):
        pt0 = self[-1]
        M, S = 0, Vec(0, 0)

        for pt in self:
            L = (pt - pt0).norm()
            M += L
            S += (pt + pt0) * (L / 2)
            pt0 = pt
        return S / M

    @property
    def xmin(self):
        return min(self._data[::2])

    @property
    def xmax(self):
        return max(self._data[::2])

    @property
    def ymin(self):
        return min(self._data[1::2])

    @property
    def ymax(self):
        return max(self._data[1::2])

    @property
    def vertices(self):
        vec = self._vec
        return [vec(x, y) for x, y in zip(self._data[::2], self._data[1::2])]

    @property
    def cbb_radius(self):
        pos = self.pos
        return max((v - pos).norm() for v in self.vertices)

    def __init__(self, *data):
        if len(data) == 1:
            data = data[0]
        self._data = [x + 0.0 for vec in data for x in vec]

    def __iter__(self):
        numbers = iter(self._data)
        vec = Vec
        for x in numbers:
            yield vec(x, next(numbers))

    def __len__(self):
        return len(self._data) // 2

    def __getitem__(self, idx):
        N = len(self._data) // 2
        if idx < -N or idx >= N:
            raise IndexError(idx)
        elif idx < 0:
            idx = N + idx
        i = 2 * idx
        return Vec(self._data[i], self._data[i + 1])

    def __flatiter__(self):
        return iter(self._data)

    def __flatlen__(self):
        return len(self._data)

    def __flatgetitem__(self, idx):
        return self._data[idx]

    def move_to_vec(self, value):
        return self.move_vec(value - self.pos)

    def move_vec(self, value):
        new = object.__new__(self.__class__)
        data = new._data = self._data[:]
        dx, dy = value
        for i in range(0, len(self._data), 2):
            data[i] += dx
            data[i + 1] += dy
        return new

    # def iter_closing(self):
    #     """Itera sobre os pontos do objeto repetindo o primeiro ao final"""
    #
    #     for x in self._data:
    #         yield x
    #     yield self._data[0]
    #
    # def get(self, i):
    #     """Semelhante à obj[i], mas ao invés de overflow, assume índices
    #     periódicos"""
    #
    #     return self._data[i % len(self._data)]
    #
    # def directions(self, n):
    #     """Retorna a lista de direções exaustivas para o teste do SAT
    #     associadas ao objeto."""
    #
    #     out = []
    #     p0 = self._data[-1]
    #     for p in self._data:
    #         x, y = p - p0
    #         p0 = p
    #         out.append(Vec(-y, x))
    #     return out
    #
    # def shadow(self, n):
    #     """Retorna as coordenadas da sombra na direção n dada.
    #     Assume n normalizado."""
    #
    #     r = self.radius
    #     center_pos = dot(self.pos, n)
    #     return (center_pos - r, center_pos + r)
    #
    # def is_simple(self):
    #     pass
    #
    # def is_convex(self):
    #     pass
    #
    # def clip(self, other):
    #     return clip(self, other)
    #
    # def convex_hull(self, other):
    #     return convex_hull(self)
    #
    # def ROG_sqr(self, axis=None):
    #     return ROG_sqr(self, axis)


class Path(PathAny, Immutable):
    """
    Open path in 2D space.
    """

    __slots__ = ()


class mPath(PathAny, mShape):
    """
    A mutable path.
    """

    __slots__ = ()

    @PathAny.pos.setter
    def pos(self, value):
        self.imove_to_vec(value)

    def imove_vec(self, vec):
        x, y = vec
        self._data[::2] = [x + xi for xi in self._data[::2]]
        self._data[1::2] = [y + yi for yi in self._data[1::2]]

    def imove_to_vec(self, vec):
        data = self._data
        dx, dy = vec - self.pos
        for i in range(0, len(self._data), 2):
            data[i] += dx
            data[i + 1] += dy
