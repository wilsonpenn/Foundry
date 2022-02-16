from __future__ import annotations

from typing import Generic, Protocol, TypeVar

from attr import attrs
from pydantic import BaseModel

from foundry.core.namespace import NamespaceType

_T = TypeVar("_T")


class NamespaceProtocol(Protocol, Generic[_T]):
    namespaces: dict[str, NamespaceProtocol]
    elements: dict[str, _T]


@attrs(slots=True, auto_attribs=True, eq=True, frozen=True, hash=True)
class Namespace(Generic[_T]):
    namespaces: dict[str, Namespace]
    elements: dict[str, _T]


class PydanticNamespace(BaseModel):
    type: NamespaceType
    namespaces: dict[str, PydanticNamespace]

    class Config:
        use_enum_values = True
