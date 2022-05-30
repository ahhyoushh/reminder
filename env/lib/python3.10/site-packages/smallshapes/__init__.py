from .__meta__ import __author__, __version__
from .core import *
from .aabb import AABBAny, AABB, mAABB
from .aabb import aabb_coords, aabb_center, aabb_pshape, aabb_rect, aabb_shape
from .circle import CircleAny, Circle, mCircle
from .segment import SegmentAny, Segment, mSegment
from .path_utils import area, center_of_mass, ROG_sqr, clip, convex_hull
from .path import PathAny, Path, mPath
from .circuit import CircuitAny, Circuit, mCircuit
from .poly import PolyAny, Poly, mPoly
from .poly_convex import ConvexPolyAny, ConvexPoly, mConvexPoly
from .poly_regular import RegularPolyAny, RegularPoly, mRegularPoly
from .poly_rectangle import RectangleAny, Rectangle, mRectangle
from .poly_triangle import TriangleAny, Triangle, mTriangle

# Late binding
MathFunctionsMixin._circle = Circle
MathFunctionsMixin._mcircle = mCircle
MathFunctionsMixin._aabb = AABB
MathFunctionsMixin._maabb = mAABB
MathFunctionsMixin._segment = Segment
MathFunctionsMixin._msegment = mSegment
MathFunctionsMixin._path = Path
MathFunctionsMixin._mpath = mPath
MathFunctionsMixin._circuit = Circuit
MathFunctionsMixin._mcircuit = mCircuit
MathFunctionsMixin._poly = Poly
MathFunctionsMixin._mpoly = mPoly
MathFunctionsMixin._convexpoly = ConvexPoly
MathFunctionsMixin._mconvexpoly = mConvexPoly
MathFunctionsMixin._regularpoly = RegularPoly
MathFunctionsMixin._mregularpoly = mRegularPoly
MathFunctionsMixin._rectangle = Rectangle
MathFunctionsMixin._mrectangle = mRectangle
MathFunctionsMixin._triangle = Triangle
MathFunctionsMixin._mtriangle = mTriangle
