"""Write a docstring."""
import numbers
from functools import singledispatch


class Expressions:
    """Write a docstring."""

    def __init__(self, *operands):
        """Write a docstring."""
        self.operands = operands

    def __add__(self, other):
        """Write a docstring."""
        if isinstance(other, numbers.Number):
            return Add(self, Number(other))
        else:
            return Add(self, other)

    def __radd__(self, other):
        """Write a docstring."""
        if isinstance(other, numbers.Number):
            return Number(other) + self
        else:
            return NotImplemented

    def __sub__(self, other):
        """Write a docstring."""
        if isinstance(other, numbers.Number):
            return Sub(self, Number(other))
        else:
            return Sub(self, other)

    def __rsub__(self, other):
        """Write a docstring."""
        if isinstance(other, numbers.Number):
            return Number(other) - self
        else:
            return NotImplemented

    def __mul__(self, other):
        """Write a docstring."""
        if isinstance(other, numbers.Number):
            return Mul(self, Number(other))
        else:
            return Mul(self, other)

    def __rmul__(self, other):
        """Write a docstring."""
        if isinstance(other, numbers.Number):
            return Number(other) * self
        else:
            return NotImplemented

    def __truediv__(self, other):
        """Write a docstring."""
        if isinstance(other, numbers.Number):
            return Div(self, Number(other))
        else:
            return Div(self, other)

    def __rtruediv__(self, other):
        """Write a docstring."""
        if isinstance(other, numbers.Number):
            return Number(other) / self
        else:
            return NotImplemented

    def __pow__(self, other):
        """Write a docstring."""
        if isinstance(other, numbers.Number):
            return Pow(self, Number(other))
        else:
            return Pow(self, other)

    def __rpow__(self, other):
        """Write a docstring."""
        if isinstance(other, numbers.Number):
            return Number(other) ** self
        else:
            return NotImplemented


class Operator(Expressions):
    """Write a docstring."""

    def __repr__(self):
        """Write a docstring."""
        return type(self).__name__ + repr(self.operands)

    def __str__(self):
        """Write a docstring."""
        if (isinstance(self.operands[0],
                       Operator) and isinstance(self.operands[1], Operator)):
            o0 = self.operands[0].__str__()
            o1 = self.operands[1].__str__()
            if self.operands[0].precedence < self.precedence:
                o0 = '(' + o0 + ')'
            if self.operands[1].precedence < self.precedence:
                o1 = '(' + o1 + ')'
            return o0 + self.symbol + o1
        elif isinstance(self.operands[0], Operator):
            o0 = self.operands[0].__str__()
            if self.operands[0].precedence < self.precedence:
                o0 = '(' + o0 + ')'
            return o0 + self.symbol + self.operands[1].__str__()
        elif isinstance(self.operands[1], Operator):
            o1 = self.operands[1].__str__()
            if self.operands[1].precedence < self.precedence:
                o1 = '(' + o1 + ')'
            return self.operands[0].__str__() + self.symbol + o1
        else:
            return (self.operands[0].__str__() + self.symbol
                    + self.operands[1].__str__())


class Add(Operator):
    """Write a docstring."""

    symbol = " + "
    precedence = 1


class Sub(Operator):
    """Write a docstring."""

    symbol = " - "
    precedence = 1


class Mul(Operator):
    """Write a docstring."""

    symbol = " * "
    precedence = 2


class Div(Operator):
    """Write a docstring."""

    symbol = " / "
    precedence = 2


class Pow(Operator):
    """Write a docstring."""

    symbol = " ^ "
    precedence = 3


class Terminal(Expressions):
    """Write a docstring."""

    def __init__(self, value):
        """Write a docstring."""
        self.value = value
        super().__init__()

    def __repr__(self):
        """Write a docstring."""
        return repr(self.value)

    def __str__(self):
        """Write a docstring."""
        return str(self.value)


class Number(Terminal):
    """Write a docstring."""

    def __init__(self, value):
        """Write a docstring."""
        if not isinstance(value, numbers.Number):
            raise ValueError("Number should be a number.")
        else:
            super().__init__(value)


class Symbol(Terminal):
    """Write a docstring."""

    def __init__(self, value):
        """Write a docstring."""
        if not isinstance(value, str):
            raise ValueError("Symbol should be a string.")
        else:
            super().__init__(value)


def postvisitor(expr, fn, **kwargs):
    """Write a docstring."""
    stack = [expr]
    visited = {}
    while stack:
        e = stack.pop()
        unvisited_children = []
        for o in e.operands:
            if o not in visited:
                unvisited_children.append(o)
        if unvisited_children:
            stack.append(e)
            for o in unvisited_children:
                stack.append(o)
        else:
            visited[e] = fn(e, *(visited[o] for o in e.operands), **kwargs)
    return visited[expr]


@singledispatch
def differentiate(expr, *o, **kwargs):
    """Write a docstring."""
    raise NotImplementedError(F"Cannot differentiate a {type(expr).__name__}")


@differentiate.register(Number)
def _(expr, *o, **kwargs):
    return Number(0.0)


@differentiate.register(Symbol)
def _(expr, *o, var, **kwargs):
    if str(expr) == var:
        return Number(1.0)
    else:
        return Number(0.0)


@differentiate.register(Add)
def _(expr, *o, **kwargs):
    return (differentiate(expr.operands[0], *o, **kwargs)
            + differentiate(expr.operands[1], *o, **kwargs))


@differentiate.register(Sub)
def _(expr, *o, **kwargs):
    return (differentiate(expr.operands[0], *o, **kwargs)
            - differentiate(expr.operands[1], *o, **kwargs))


@differentiate.register(Mul)
def _(expr, *o, **kwargs):
    return (differentiate(expr.operands[0], *o, **kwargs) * expr.operands[1]
            + differentiate(expr.operands[1], *o, **kwargs)
            * expr.operands[0])


@differentiate.register(Div)
def _(expr, *o, **kwargs):
    return ((differentiate(expr.operands[0], *o, **kwargs) * expr.operands[1]
             - differentiate(expr.operands[1], *o,
                             **kwargs) * expr.operands[0])
            / expr.operands[1]**2)


@differentiate.register(Pow)
def _(expr, *o, **kwargs):
    return (expr.operands[1] * differentiate(expr.operands[0], *o, **kwargs)
            * expr.operands[0]**(expr.operands[1] - 1))
