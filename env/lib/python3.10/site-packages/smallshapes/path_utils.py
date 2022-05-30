from smallvectors import Vec


def _w_list(L):
    """
    Return list of weight terms W = 1/2 * (y1*x0 - y0*x1) for all points in the
    input list.

    Each term is the result of the integral $\int <y, x>.d\vec{\ell}$ over a
    straight line segment.
    """

    N = len(L)
    out = []
    for i in range(N):
        x1, y1 = L[(i + 1) % N]
        x0, y0 = L[i]
        out.append(0.5 * (y1 * x0 - y0 * x1))
    return out


def area(L):
    """
    Compute area of polygon defined by list of points.

    List should be in counter-clockwise fashion. Otherwise, area will be negative.

    Example:
        >>> pts = [(0, 0), (1, 0), (1, 2), (0, 1)]
        >>> area(pts)
        1.5
    """

    return sum(_w_list(L))


def center_of_mass(L):
    """
    Return the center of mass vector for a solid polygon defined by the given
    list of points.

    Example:
        >>> pts = [(0, 0), (1, 0), (1, 1), (0, 1)]
        >>> center_of_mass(pts)
        Vec(0.5, 0.5)
    """

    W = _w_list(L)
    A = sum(W)
    N = len(L)
    x_cm = 0
    y_cm = 0
    if A == 0:
        return Vec(*L[0])
    for i in range(N):
        x1, y1 = L[(i + 1) % N]
        x0, y0 = L[i]
        wi = W[i]
        x_cm += (x1 + x0) * wi / 3.0
        y_cm += (y1 + y0) * wi / 3.0
    x_cm /= A
    y_cm /= A
    return Vec(x_cm, y_cm)


def ROG_sqr(L, axis=None):
    """
    Return the square of the gyration radius.

    The gyration radius squared is equal to the moment of inertia of an object
    with mass equal to one.

    >>> pts = [(0, 0), (2, 0), (2, 2), (0, 2)]

    If axis is not determined, assumes a moment of inertia against the center
    of mass.

    >>> ROG_sqr(pts)                             # doctest: +ELLIPSIS
    0.666...

    The value of this quantity, as with the moment of inertia, depends of a
    reference point.

    >>> ROG_sqr(pts, axis=(0, 0))                # doctest: +ELLIPSIS
    2.666...
    """

    W = _w_list(L)
    A = sum(W)
    N = len(L)
    ROG2_orig = 0
    for i in range(N):
        x1, y1 = L[(i + 1) % N]
        x0, y0 = L[i]
        ROG2_orig += ((x1 + x0) ** 2 - x1 * x0 + (y1 + y0)
                      ** 2 - y1 * y0) * W[i] / 6
    ROG2_orig /= A

    # Parallel axis theorem to move the object away from the center of mass.
    cm = center_of_mass(L)
    ROG2_cm = ROG2_orig - (cm.x ** 2 + cm.y ** 2)
    if axis is None:
        return ROG2_cm
    else:
        # Uses the parallel axis theorem again to translate back to the final
        # axis.
        D = (cm - axis)
        return ROG2_cm + (D.x ** 2 + D.y ** 2)


def clip(poly1, poly2):
    """
    Sutherland-Hodgman polygon clipping algorithm.
    """

    def inside(pt):
        """
        Return True if point is inside second polygon.
        """
        pt_rel = pt - r0
        return T.x * pt_rel.y >= T.y * pt_rel.x

    def intercept_point():
        """
        Return intercept between segments formed by ``r1 - r0`` and ``v1 - v0``.
        """

        A = r0.x * r1.y - r0.y * r1.x
        B = v0.x * v1.y - v0.y * v1.x
        C = 1.0 / (T.x * T_.y - T.y * T_.x)
        return Vec((-A * T_.x + B * T.x) * C, (-A * T_.y + B * T.y) * C)

    out = list(poly1)
    r0 = poly2[-1]

    # Iterates over lines in poly2
    for r1 in poly2:
        if not out:
            raise ValueError('no superposition detected')

        T = r1 - r0
        points, out = out, []
        v0 = points[-1]
        v0_inside = inside(v0)

        # In each line, iterate over the points in the output polygon.
        for v1 in points:
            T_ = v1 - v0

            # inside, outside ==> creates intermediate point
            # both inside ==> copy to the out polygon
            # both outside ==> abandon previous point
            v1_inside = inside(v1)
            if (v1_inside + v0_inside) == 1:
                out.append(intercept_point())
            if v1_inside:
                out.append(v1)

            # Update previous point
            v0 = v1
            v0_inside = v1_inside

        # Update initial point
        r0 = r1
    return out


def convex_hull(points):
    """
    Convex hull for the list of points.

    Uses Andrew's monotonic chain algorithm in O(n log n).

    Example:
        >>> hull = convex_hull([(0, 0), (1, 1), (1, 0), (0, 1), (0.5, 0.5)])
        >>> hull == [(0, 0), (1, 0), (1, 1), (0, 1)]
        True
    """

    # Lexicographical sort
    points = sorted(set(map(tuple, points)))
    points = [Vec(*pt) for pt in points]
    if len(points) <= 1:
        return points

    # L: lower vertices
    # Adds points to L if the result preserves an counter-clockwise direction.
    L = []
    for p in points:
        while len(L) >= 2 and (L[-1] - L[-2]).cross(p - L[-2]) <= 0:
            L.pop()
        L.append(p)

    # U: upper vertices
    # Similar as before, but iterates in the opposite order.
    U = []
    for p in reversed(points):
        while len(U) >= 2 and (U[-1] - U[-2]).cross(p - U[-2]) <= 0:
            U.pop()
        U.append(p)

    # Remove last point since it is duplicated
    return L[:-1] + U[:-1]