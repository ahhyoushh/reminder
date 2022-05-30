import random
from functools import lru_cache
from math import sqrt, acos

__all__ = ['Color', 'colorproperty', 'rgb', 'rgba', 'COLOR_NAMES']


class Color(object):
    """
    Represents a color.
    """

    __slots__ = ['_red', '_green', '_blue', '_alpha']
    _CACHE = {}
    _RANGE = (0, 1, 2, 3)

    @classmethod
    def from_rgba(cls, red=0, green=0, blue=0, alpha=255):
        """
        Create color from RGBa components.
        """

        new = object.__new__(cls)
        new._fromrgba(red, green, blue, alpha)
        return new

    def __init__(self, *args, **kwargs):
        # RGB parameters (with or without alpha)
        if len(args) in [3, 4]:
            self._fromrgba(*args, **kwargs)

        elif len(args) == 1:
            value, = args

            # Start from another color, tuple or list of values
            if isinstance(value, (list, tuple, Color)):
                self._fromrgba(*value)

            # Start from string (either hex or color name)
            elif isinstance(value, str):
                if value.startswith('#'):
                    self._fromhex(value, **kwargs)
                elif value == 'random':
                    self._fromrgba(*[random.randint(0, 255) for _ in range(3)])
                else:
                    self._fromname(value, **kwargs)

            # Start from integer
            elif isinstance(value, int):
                r = (value & 0xff0000) >> 16
                g = (value & 0xff00) >> 8
                b = (value & 0xff) >> 0
                self._fromrgba(r, g, b, **kwargs)

        elif len(args) == 0:
            raise NotImplemented
        else:
            TypeError('invalid number of arguments: %s' % len(args))

    def _fromrgba(self, r=0, g=0, b=0, a=255):
        self._red = int(r)
        self._green = int(g)
        self._blue = int(b)
        self._alpha = int(a)

    def _fromhex(self, value, alpha=255):
        value = value[1:]
        if len(value) in [3, 4]:
            value = ''.join(c + c for c in value)
        if len(value) == 6:
            a = alpha
            r, g, b = (
                int(value[2 * i:2 * i + 2], 16) for i in range(3))
        elif len(value) == 8:
            r, g, b, a = (
                int(value[2 * i:2 * i + 2], 16) for i in range(4))
        else:
            raise ValueError('invalid hex code: #%s' % value)
        self._fromrgba(r, g, b, a)

    def _fromname(self, value):
        value = value.lower()
        self._fromrgba(*self._CACHE[value].rgba)

    @property
    def red(self):
        """
        Red component (from 0 to 255)
        """
        return self._red

    @property
    def green(self):
        """
        Green component (from 0 to 255)
        """

        return self._green

    @property
    def blue(self):
        """
        Blue component (from 0 to 255)
        """

        return self._blue

    @property
    def alpha(self):
        """
        Alpha component (0: transparent, 255: solid color)
        """

        return self._alpha

    @property
    def hue(self):
        """
        Hue component (from 0 to 255).
        """

        return NotImplemented

    @property
    def saturation(self):
        """
        Saturation component (from 0 to 255).
        """

        return NotImplemented

    @property
    def intensity(self):
        """
        Intensity component (from 0 to 255).
        """

        return NotImplemented

    @property
    def rgba(self):
        """
        Tuple with (red, green, blue, alpha)
        """
        return tuple(self)

    @property
    def rgb(self):
        """
        Tuple with (red, green, blue)
        """
        return self[:3]

    @property
    def rgbf(self):
        """
        Floating-point version of rgb, normalized in the [0, 1] interval.
        """

        return tuple(x / 255. for x in self[:3])

    @property
    def rgbaf(self):
        """
        Floating-point version of rgba, normalized in the [0, 1] interval.
        """

        return tuple(x / 255. for x in self)

    @property
    def rgbau(self):
        """
        RGBA as a single 32 bit unsigned integer.
        """

        c = self
        return (c[0] << 24) + (c[1] << 16) + (c[2] << 8) + c[3]

    @property
    def rgbu(self):
        c = self
        return (c[0] << 16) + (c[1] << 8) + c[2]

    @property
    def hsi(self):
        return self.hsia[:-1]

    @property
    def hsia(self):
        # (H)ue, (S)aturation, (I)ntensity
        # ref: https://en.wikipedia.org/wiki/RGB_color_model#Nonlinearity
        R, G, B, a = self

        I = (R + G + B) / 3
        S = 1 - min(R, G, B) / I

        # Normalized
        r, g, b = R / 255, G / 255, B / 255
        h_numer = acos(((r - g) + (r - b)) / 2)
        h_denom = sqrt((r - b) ** 2 + (r - b) * (g - b))
        return h_numer / h_denom, S, I, a

    @property
    def hsiaf(self):
        return tuple(x / 255 for x in self.hsia)

    @property
    def hsif(self):
        return tuple(x / 255 for x in self.hsi)

    def copy(self, red=None, green=None, blue=None, alpha=None, **kwds):
        """
        Returns a copy, possibly changing the value of a component.

        Example:
            >>> color = Color('white')
            >>> color.copy(red=80, alpha=128)
            Color(80, 255, 255, 128)
        """
        R, G, B, A = self

        if red is not None:
            R = red
        if green is not None:
            G = green
        if blue is not None:
            B = blue
        if alpha is not None:
            A = alpha
        if kwds:
            raise NotImplementedError

        return Color(R, G, B, A)

    # Métodos mágicos
    def __repr__(self):
        return 'Color%s' % (tuple(self),)

    def __len__(self):
        return 4

    def __eq__(self, other):
        try:
            return (
                (self._red == other._red) and
                (self._green == other._green) and
                (self._blue == other._blue) and
                (self._alpha == other._alpha))
        except (AttributeError, TypeError):
            if len(other) == 4:
                return all(x == y for (x, y) in zip(self, other))
            elif len(other) == 3:
                return ((self._alpha == 255) and
                        all(x == y for (x, y) in zip(self, other)))
            return False

    def __iter__(self):
        yield self._red
        yield self._green
        yield self._blue
        yield self._alpha

    def __getitem__(self, key):
        if isinstance(key, int):
            if key < 0:
                key += len(self)
                if key < 0:
                    raise IndexError(key)
            if key == 0:
                return self._red
            elif key == 1:
                return self._green
            elif key == 2:
                return self._blue
            elif key == 3:
                return self._alpha
        else:
            return tuple(self[i] for i in self._RANGE[key])
        raise IndexError(key)

    def __hash__(self):
        return hash(self.u_rgba)


Color._CACHE.update(
    # HTML 4.01 colors.
    # See https://en.wikipedia.org/wiki/Web_colors
    white=Color('#ffffff'),
    silver=Color('#c0c0c0'),
    gray=Color('#808080'),
    black=Color('#000000'),
    red=Color('#ff0000'),
    maroon=Color('#800000'),
    yellow=Color('#ffff00'),
    olive=Color('#808000'),
    lime=Color('#00ff00'),
    green=Color('#008000'),
    aqua=Color('#00ffff'),
    teal=Color('#008080'),
    blue=Color('#0000ff'),
    navy=Color('#000080'),
    fuschia=Color('#ff00ff'),
    purple=Color('#800080'),
    transparent=Color('#ffffff00'),
    null=Color('#00000000'),
)

# SVG extended Colors
# http://www.w3.org/TR/css3-color/#svg-color
COLOR_NAMES = [
    ['aliceblue', '#F0F8FF'],
    ['antiquewhite', '#FAEBD7'],
    ['aqua', '#00FFFF'],
    ['aquamarine', '#7FFFD4'],
    ['azure', '#F0FFFF'],
    ['beige', '#F5F5DC'],
    ['bisque', '#FFE4C4'],
    ['black', '#000000'],
    ['blanchedalmond', '#FFEBCD'],
    ['blue', '#0000FF'],
    ['blueviolet', '#8A2BE2'],
    ['brown', '#A52A2A'],
    ['burlywood', '#DEB887'],
    ['cadetblue', '#5F9EA0'],
    ['chartreuse', '#7FFF00'],
    ['chocolate', '#D2691E'],
    ['coral', '#FF7F50'],
    ['cornflowerblue', '#6495ED'],
    ['cornsilk', '#FFF8DC'],
    ['crimson', '#DC143C'],
    ['cyan', '#00FFFF'],
    ['darkblue', '#00008B'],
    ['darkcyan', '#008B8B'],
    ['darkgoldenrod', '#B8860B'],
    ['darkgray', '#A9A9A9'],
    ['darkgreen', '#006400'],
    ['darkgrey', '#A9A9A9'],
    ['darkkhaki', '#BDB76B'],
    ['darkmagenta', '#8B008B'],
    ['darkolivegreen', '#556B2F'],
    ['darkorange', '#FF8C00'],
    ['darkorchid', '#9932CC'],
    ['darkred', '#8B0000'],
    ['darksalmon', '#E9967A'],
    ['darkseagreen', '#8FBC8F'],
    ['darkslateblue', '#483D8B'],
    ['darkslategray', '#2F4F4F'],
    ['darkslategrey', '#2F4F4F'],
    ['darkturquoise', '#00CED1'],
    ['darkviolet', '#9400D3'],
    ['deeppink', '#FF1493'],
    ['deepskyblue', '#00BFFF'],
    ['dimgray', '#696969'],
    ['dimgrey', '#696969'],
    ['dodgerblue', '#1E90FF'],
    ['firebrick', '#B22222'],
    ['floralwhite', '#FFFAF0'],
    ['forestgreen', '#228B22'],
    ['fuchsia', '#FF00FF'],
    ['gainsboro', '#DCDCDC'],
    ['ghostwhite', '#F8F8FF'],
    ['gold', '#FFD700'],
    ['goldenrod', '#DAA520'],
    ['gray', '#808080'],
    ['green', '#008000'],
    ['greenyellow', '#ADFF2F'],
    ['grey', '#808080'],
    ['honeydew', '#F0FFF0'],
    ['hotpink', '#FF69B4'],
    ['indianred', '#CD5C5C'],
    ['indigo', '#4B0082'],
    ['ivory', '#FFFFF0'],
    ['khaki', '#F0E68C'],
    ['lavender', '#E6E6FA'],
    ['lavenderblush', '#FFF0F5'],
    ['lawngreen', '#7CFC00'],
    ['lemonchiffon', '#FFFACD'],
    ['lightblue', '#ADD8E6'],
    ['lightcoral', '#F08080'],
    ['lightcyan', '#E0FFFF'],
    ['lightgoldenrodyellow', '#FAFAD2'],
    ['lightgray', '#D3D3D3'],
    ['lightgreen', '#90EE90'],
    ['lightgrey', '#D3D3D3'],
    ['lightpink', '#FFB6C1'],
    ['lightsalmon', '#FFA07A'],
    ['lightseagreen', '#20B2AA'],
    ['lightskyblue', '#87CEFA'],
    ['lightslategray', '#778899'],
    ['lightslategrey', '#778899'],
    ['lightsteelblue', '#B0C4DE'],
    ['lightyellow', '#FFFFE0'],
    ['lime', '#00FF00'],
    ['limegreen', '#32CD32'],
    ['linen', '#FAF0E6'],
    ['magenta', '#FF00FF'],
    ['maroon', '#800000'],
    ['mediumaquamarine', '#66CDAA'],
    ['mediumblue', '#0000CD'],
    ['mediumorchid', '#BA55D3'],
    ['mediumpurple', '#9370DB'],
    ['mediumseagreen', '#3CB371'],
    ['mediumslateblue', '#7B68EE'],
    ['mediumspringgreen', '#00FA9A'],
    ['mediumturquoise', '#48D1CC'],
    ['mediumvioletred', '#C71585'],
    ['midnightblue', '#191970'],
    ['mintcream', '#F5FFFA'],
    ['mistyrose', '#FFE4E1'],
    ['moccasin', '#FFE4B5'],
    ['navajowhite', '#FFDEAD'],
    ['navy', '#000080'],
    ['oldlace', '#FDF5E6'],
    ['olive', '#808000'],
    ['olivedrab', '#6B8E23'],
    ['orange', '#FFA500'],
    ['orangered', '#FF4500'],
    ['orchid', '#DA70D6'],
    ['palegoldenrod', '#EEE8AA'],
    ['palegreen', '#98FB98'],
    ['paleturquoise', '#AFEEEE'],
    ['palevioletred', '#DB7093'],
    ['papayawhip', '#FFEFD5'],
    ['peachpuff', '#FFDAB9'],
    ['peru', '#CD853F'],
    ['pink', '#FFC0CB'],
    ['plum', '#DDA0DD'],
    ['powderblue', '#B0E0E6'],
    ['purple', '#800080'],
    ['red', '#FF0000'],
    ['rosybrown', '#BC8F8F'],
    ['royalblue', '#4169E1'],
    ['saddlebrown', '#8B4513'],
    ['salmon', '#FA8072'],
    ['sandybrown', '#F4A460'],
    ['seagreen', '#2E8B57'],
    ['seashell', '#FFF5EE'],
    ['sienna', '#A0522D'],
    ['silver', '#C0C0C0'],
    ['skyblue', '#87CEEB'],
    ['slateblue', '#6A5ACD'],
    ['slategray', '#708090'],
    ['slategrey', '#708090'],
    ['snow', '#FFFAFA'],
    ['springgreen', '#00FF7F'],
    ['steelblue', '#4682B4'],
    ['tan', '#D2B48C'],
    ['teal', '#008080'],
    ['thistle', '#D8BFD8'],
    ['tomato', '#FF6347'],
    ['turquoise', '#40E0D0'],
    ['violet', '#EE82EE'],
    ['wheat', '#F5DEB3'],
    ['white', '#FFFFFF'],
    ['whitesmoke', '#F5F5F5'],
    ['yellow', '#FFFF00'],
    ['yellowgreen', '#9ACD32']
]
for _name, _code in COLOR_NAMES:
    Color._CACHE.setdefault(_name, Color(_code))


class colorproperty(property):
    """
    Automatically converts attribute assignments to color objects.
    """

    def __init__(self, name, default=None):
        default = (None if default is None else Color(default))
        attr = '_' + name

        def fget(self):
            return getattr(self, attr, default)

        def fset(self, value):
            if value is None:
                setattr(self, attr, default)
            elif isinstance(value, Color):
                setattr(self, attr, value)
            else:
                setattr(self, attr, Color(value))

        def fdel(self):
            if hasattr(self, attr):
                delattr(self, attr)
            else:
                raise AttributeError(name)

        super(colorproperty, self).__init__(fget, fset, fdel)


def color(*args):
    """
    Faster constructor of Color() objects.

    Accept all positional arguments as Color(), but rejects any keyword
    arguments.

    It avoids a few expansive checks in the Color() constructor and also caches
    the results.
    """

    if len(args) == 1:
        value = args[0]
        if isinstance(value, Color):
            return value
        elif isinstance(value, str):
            if not value.startswith('#'):
                return _cached_hex(value)

    return _cached_color(args)


@lru_cache(maxsize=512)
def _cached_hex(value):
    return Color(value)


@lru_cache(maxsize=512)
def _cached_color(args):
    return Color(*args)


def rgb(color):
    """
    Convert input in a tuple of (red, green, blue) colors.

    Null values are converted to solid black.
    """

    try:
        return color.rgb
    except AttributeError:
        return Color(color or 'black').rgb


def rgba(color):
    """
    Convert input in a tuple of (red, green, blue, alpha) components

    Null values are converted to solid black.
    """

    try:
        return color.rgba
    except AttributeError:
        return Color(color or 'black').rgba
