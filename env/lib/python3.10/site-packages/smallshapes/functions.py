from generic import generic


@generic
def distance(A, B):
    """
    Return the distance of two objects.

    Return 0 if one object is contained into the other of if they intercept
    """

    raise NotImplementedError


@generic
def contain(A, B):
    """
    Return True if A completely contains B.
    """

    raise NotImplementedError


@generic
def intercept_center(A, B):
    """
    Return the center point of the intercept between A and B.
    """

    raise NotImplementedError


@generic
def penetration(A, B):
    """
    Return the penetration between A and B.
    """

    raise NotImplementedError


def simplify_number(x):
    """
    Convert number to the simplest numeric class that correctly represents it.
    """

    try:
        i = int(x)
        if i == x:
            return i
    except ValueError:
        return x