'''
Implementa o separating axis theorem (sat) para detecção de colisão entre as
formas de colisão básicas.
'''
from generic import generic
from smallvectors import Vec
from smallshapes import Circle, AABB

e1 = Vec(1, 0)
e2 = Vec(0, 1)


@generic
def shadow(A, normal):
    return A.shadow(normal)


@shadow.register(AABB, object)
def shadow_aabb(A, normal):
    if normal is e1:
        return A.xmin, A.xmax
    elif normal is e2:
        return A.ymin, A.ymax
    else:
        return A.shadow(normal)


###############################################################################
#                       Cálculo de direções sat
###############################################################################
GENERIC_DIRECTIONS = []


@generic
def normals(A, B):
    try:
        return A.normals() + B.normals()
    except AttributeError:
        return GENERIC_DIRECTIONS


@normals.register(Circle, Circle)
def normals_circle(A, B):
    return [(B.pos - A.pos).normalize()]


@normals.register(AABB, AABB)
def normals_aabb(A, B):
    return [e1, e2]


@normals.register(AABB, Circle)
def normals_aabb_circle(A, B):
    # Encontra o vértice mais próximo do centro
    D = float('inf')
    pt = Vec(0, 0)
    for v in A.vertices:
        delta = B.pos - v
        dnew = delta.norm()
        if dnew < D:
            D = dnew
            pt = delta

    return [pt.normalize(), e1, e2]


# ...
###############################################################################
#                       Implementações do ŜAT
###############################################################################


def sat(A, B):
    '''Retorna o vetor de mínima penetração (ou None, caso não haja
    superposição) usando o teorema dos eixos separadores nos dois objetos
    dados.

    O vetor de mínima penetração é definido como um vetor que sai do primeiro
    para o segundo objeto e cujo módulo é igual ao tamanho da menor
    superposição entre ambos

    Exemples
    --------

    O SAT é um algoritmo genérico que permite calcular o vetor de menor
    separação entre dois objetos em superposição. Também detecta a ausência
    de superposição. Funciona para objetos convexos arbitrários.

    Testamos dois círculos em superposição

    >>> c1 = Circle(3, (0, 0))
    >>> c2 = Circle(3, (3, 4))
    >>> sat(c1, c2)
    Vec(0.6000000000000001, 0.8)

    Caso não haja superposição, a função retorna None

    >>> sat(c1, Circle(3, (10, 10))) is None
    True

    A função sat funciona para figuras arbitrárias que suportam os métodos
    normals() e shadow()

    >>> box1 = AABB(4, 9, 1, 6)
    >>> box2 = AABB(0, 5, 0, 5)
    >>> sat(box1, box2)
    Vec(-1.0, 0.0)
    '''

    nlist = normals(A, B)

    D = float('inf')
    for n in nlist:
        a1, a2 = shadow(A, n)
        b1, b2 = shadow(B, n)
        S = min(a2, b2) - max(a1, b1)
        if S < 0:
            return None
        elif S < D:
            D = S
            if (a1 + a2) > (b1 + b2):
                n *= -1
            d = n.normalize()
    return d * D


if __name__ == '__main__':
    import doctest
    doctest.testmod()