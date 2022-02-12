from typing import Protocol

from attr import attrs
from PySide6.QtCore import QPoint


class PointProtocol(Protocol):
    """
    A two dimensional representation of a point on a plain.

    Attributes
    ----------
    x: int
        The horizontal location of the point.
    y: int
        The vertical location of the point.
    """

    x: int
    y: int


@attrs(slots=True, auto_attribs=True)
class MutablePoint:
    """
    A two dimensional representation of a point on a plain, that uses ``attrs`` to create a basic
    implementation.

    Attributes
    ----------
    x: int
        The horizontal location of the point.
    y: int
        The vertical location of the point.
    """

    x: int
    y: int

    @classmethod
    def from_qpoint(cls, point: QPoint):
        return cls(point.x(), point.y())
