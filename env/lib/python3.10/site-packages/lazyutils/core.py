class delegate_to(object):
    """
    Delegate access to an inner variable.

    A delegate is an alias for an attribute of the same name that lives in an
    inner object of a class.

    Example:
        Consider the very simple example::

            class Foo(object):
                data = "foo-bar"
                upper = delegate_to('data')

            x = Foo()

        ``x.upper()`` is now an alias for ``x.data.upper()``.

    Args:
        attribute:
            Name of the inner variable that receives delegation.
        readonly:
            If true, makes the the delegate readonly.
        inner_name:
            The name of the inner variable. Can be ommited if the name is the
            same of the attribute.
    """

    def __init__(self, attribute, readonly=False, inner_name=None):
        self.attribute = attribute
        self.readonly = readonly
        self.inner_name = inner_name

    def __get__(self, obj, cls=None):
        if obj is None:
            return self
        owner = getattr(obj, self.attribute)
        try:
            attr = self._name
        except AttributeError:
            attr = self._name = self._get_name(cls)
        return getattr(owner, attr)

    def __set__(self, obj, value):
        if self.readonly:
            raise AttributeError
        owner = getattr(obj, self.attribute)
        try:
            attr = self._name
        except AttributeError:
            attr = self._name = self._get_name(type(obj))
        setattr(owner, attr, value)

    def _get_name(self, cls):
        for attr in dir(cls):
            value = getattr(cls, attr, None)
            if value is self:
                return attr
        raise RuntimeError('not a member of class')


class delegate_ro(delegate_to):
    """
    A read-only version of delegate_to()
    """

    def __init__(self, attribute):
        super().__init__(attribute, readonly=True)


class alias(object):
    """
    An alias to an attribute.

    Args:
        attribute (str):
            Name of aliased attribute.
        readonly (bool):
            If True, makes the alias read only.
    """

    def __init__(self, attribute, readonly=False):
        self.attribute = attribute
        self.readonly = readonly

    def __get__(self, obj, cls=None):
        if obj is not None:
            return getattr(obj, self.attribute)
        return self

    def __set__(self, obj, value):
        if self.readonly:
            raise AttributeError(self.attribute)

        setattr(obj, self.attribute, value)


class readonly(alias):
    """
    A read-only alias to an attribute.
    """

    def __init__(self, attribute):
        super(readonly, self).__init__(attribute, readonly=True)


class lazy:
    """
    Decorator that defines an attribute that is initialized as first usage
    rather than at instance creation.

    Usage is similar to the ``@property`` decorator, although lazy attributes do
    not override the *setter* and *deleter* methods.
    """

    def __init__(self, function):
        self.function = function
        self.__name__ = getattr(function, '__name__', None)

    def __get__(self, obj, cls=None):
        if obj is None:
            return self

        result = self.function(obj)
        try:
            attr_name = self._attr
        except AttributeError:
            attr_name = self._get_attribute_name(cls)

        setattr(obj, attr_name, result)
        return result

    def _get_attribute_name(self, cls):
        """Inspect live object for some attributes."""

        try:
            if getattr(cls, self.__name__) is self:
                return self.__name__
        except AttributeError:
            pass

        for attr in dir(cls):
            value = getattr(cls, attr, None)
            if value is self:
                self._attr = attr
                return attr

        raise TypeError('lazy accessor not found in %s' % cls.__name__)


class lazy_shared(lazy):
    """
    A lazy accessor whose state is computed at first access and is shared
    between all instances.
    """

    def __get__(self, obj, cls=None):
        if obj is None:
            return self

        try:
            return self.state
        except AttributeError:
            self.state = self.function(obj)
            return self.state


class lazy_classattribute(lazy):
    """
    A lazy accessor tied to a class instead of specific instances.
    """

    def __get__(self, obj, cls=None):
        result = self.function(obj)
        setattr(cls, self.__name__, result)
        return result
