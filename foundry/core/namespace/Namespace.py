from __future__ import annotations

from collections import ChainMap, deque
from typing import Any, Generic, Optional, Protocol, Sequence, Type, TypeVar, Union

from attr import attrs
from pydantic import BaseModel

from foundry.core.namespace import NamespaceType

_T = TypeVar("_T")


class NamespaceProtocol(Protocol, Generic[_T]):
    parent: Optional[NamespaceProtocol]
    dependencies: dict[str, NamespaceProtocol]
    elements: dict[str, _T]
    children: dict[str, NamespaceProtocol]

    @property
    def root(self) -> NamespaceProtocol:
        ...

    def __getitem__(self, key: str) -> Any:
        ...


_PT = TypeVar("_PT")


class PydanticNamespaceProtocol(Protocol, Generic[_PT]):
    parent: Optional[NamespaceProtocol]
    dependencies: dict[str, NamespaceProtocol]
    elements: dict[str, _PT]
    children: dict[str, NamespaceProtocol]

    @property
    def namespace(self) -> NamespaceProtocol[_PT]:
        ...

    @classmethod
    def validate(cls, v: dict) -> PydanticNamespaceProtocol[_PT]:
        ...


class PartialNamespace(Generic[_T]):
    parent: Optional[NamespaceProtocol]
    dependencies: dict[str, NamespaceProtocol]
    elements: dict[str, _T]
    children: dict[str, NamespaceProtocol]

    @property
    def root(self) -> NamespaceProtocol:
        if self.parent is None:
            return self
        else:
            return self.parent.root

    def __getitem__(self, key: str) -> Any:
        return ChainMap(self.elements, *[d.elements for d in self.dependencies.values()])[key]


@attrs(slots=True, auto_attribs=True, eq=True)
class MutableNamespace(PartialNamespace[_T]):
    parent: Optional[NamespaceProtocol]
    dependencies: dict[str, NamespaceProtocol]
    elements: dict[str, _T]
    children: dict[str, NamespaceProtocol]

    @staticmethod
    def from_namespace(namespace: NamespaceProtocol[_PT]) -> MutableNamespace[_PT]:
        return MutableNamespace(namespace.parent, namespace.dependencies, namespace.elements, namespace.children)


@attrs(slots=True, auto_attribs=True, eq=True, frozen=True, hash=True)
class Namespace(PartialNamespace[_T]):
    parent: Optional[Namespace]
    dependencies: dict[str, Namespace]
    elements: dict[str, _T]
    children: dict[str, Namespace]

    @staticmethod
    def from_namespace(namespace: NamespaceProtocol[_PT]) -> Namespace[_PT]:
        parent = (
            namespace.parent
            if namespace.parent is None or isinstance(namespace.parent, Namespace)
            else Namespace.from_namespace(namespace.parent)
        )
        dependencies = {
            s: d if isinstance(d, Namespace) else Namespace.from_namespace(d) for s, d in namespace.dependencies.items()
        }
        children = {
            s: c if isinstance(c, Namespace) else Namespace.from_namespace(c) for s, c in namespace.children.items()
        }
        return Namespace(parent, dependencies, namespace.elements, children)


class NamespaceNotInitializedException(Exception):
    def __init__(self, parent: NamespaceProtocol, uninitialized_child: str):
        self.parent = parent
        self.uninitialized_child = uninitialized_child
        super().__init__(f"{self.parent} does not have the child {self.uninitialized_child} initialized.")


_DEPENDENCY_INFORMATION = tuple[Union[NamespaceProtocol, PydanticNamespaceProtocol], str, dict]


class NamespaceChildrenNotInitializedException(Exception):
    def __init__(
        self,
        partial_initialized_child: NamespaceProtocol,
        parent: Union[NamespaceProtocol, PydanticNamespaceProtocol],
        uninitialized_child: str,
        uninitialized_dependencies: Sequence[_DEPENDENCY_INFORMATION],
    ):
        self.partial_initialized_child = partial_initialized_child
        self.parent = parent
        self.uninitialized_child = uninitialized_child
        self.uninitialized_dependencies = uninitialized_dependencies
        super().__init__(
            f"{self.parent} does not have the child {self.uninitialized_child} initialized and one or "
            + "more dependencies inside {self.uninitialized_dependencies} require this dependency."
        )


def pydantic_namespace(element_type: Type[_T]) -> PydanticNamespaceProtocol[_T]:
    def get_number_of_dots(s: str) -> int:
        """
        Provides the amount of starting dots for a given element.

        Parameters
        ----------
        s : str
            The string to find the starting dots for.

        Returns
        -------
        int
            The number of starting dots.
        """
        for index, char in enumerate(s):
            if char != ".":
                return index
        return len(s)

    class PydanticNamespace(BaseModel):
        parent: Optional[NamespaceProtocol]
        dependencies: dict[str, NamespaceProtocol]
        elements: dict[str, _T]
        children: dict[str, NamespaceProtocol]

        @classmethod
        def __get_validators__(cls):
            yield cls.validate

        @property
        def namespace(self) -> Namespace[_T]:
            return Namespace.from_namespace(
                MutableNamespace(self.parent, self.dependencies, self.elements, self.children)
            )

        @staticmethod
        def generate_namespace_from_type(**kwargs) -> NamespaceProtocol:
            if not isinstance(kwargs, dict):
                raise TypeError("Dictionary required")
            if "type" not in kwargs:
                raise KeyError(f"type of namespace is not found inside {kwargs}.")
            _type = kwargs["type"]
            if NamespaceType.INTEGER == _type:
                return pydantic_namespace(int).validate(kwargs).namespace
            raise NotImplementedError

        @classmethod
        def generate_namespace(
            cls,
            parent: Optional[NamespaceProtocol],
            dependencies: dict[str, NamespaceProtocol],
            elements: dict[str, dict],
            children: dict[str, dict],
        ) -> PydanticNamespace:
            """
            Generates a namespace dynamically from its parent and dependencies.

            Parameters
            ----------
            dependencies : dict[str, NamespaceProtocol]
                The dependencies required for this namespace.
            elements : dict[str, dict]
                The elements, as a list of dictionaries to be validated.
            children : dict[str, dict]
                The children namespaces to be referenced.

            Returns
            -------
            PydanticNamespace
                The created namespace.
            """

            self = cls()
            self.parent = parent
            self.dependencies = dependencies
            self.elements = {}
            self.children = {}

            for key, value in elements.items():
                self.elements.update({key: element_type(**value, parent=self)})

            uninitialized_children: deque[_DEPENDENCY_INFORMATION] = deque()
            uninitialized_children.extend([(self, key, value) for key, value in children.items()])

            while len(uninitialized_children) > 0:
                child_parent, key, value = uninitialized_children.pop()

                try:
                    child_parent.children.update({key: self.generate_namespace_from_type(**value)})
                except NamespaceNotInitializedException:
                    uninitialized_children.append((child_parent, key, value))
                except NamespaceChildrenNotInitializedException as e:
                    if e.parent is not self:
                        uninitialized_children.append((child_parent, key, value))
                        raise NamespaceChildrenNotInitializedException(
                            self.namespace, child_parent, key, uninitialized_children
                        )
                    else:
                        self.children.update({key: e.partial_initialized_child})
                        uninitialized_children.extend(e.uninitialized_dependencies)

            return self

        @staticmethod
        def initialize_depedencies(
            parent: Optional[NamespaceProtocol], dependencies: list[str]
        ) -> dict[str, NamespaceProtocol]:
            """
            Initializes a finds the dependencies required for a given namespace to be validated.

            Parameters
            ----------
            parent : Optional[NamespaceProtocol]
                The parent to derive the dependencies from.
            dependencies : list[str]
                The dependencies to initialize.

            Returns
            -------
            dict[str, NamespaceProtocol]
                The dependencies initialized.

            Raises
            ------
            NamespaceNotInitializedException
                If one or more dependencies are initialized, this error will be raised, so the dependency can
                be initialized before continuation.

            Notes
            -----
            The dependencies follow dot format.  This enables a dependency to reference a child of a child.
            """

            initialized_dependencies = {}

            if parent is not None:
                for dependency in dependencies:
                    starting_parent_index = get_number_of_dots(dependency)
                    if starting_parent_index > 1:
                        initialized_dependency = parent
                        for _ in range(starting_parent_index - 1):
                            if initialized_dependency is None:
                                raise AttributeError(f"{dependency} could not be found.")
                            initialized_dependency = initialized_dependency.parent
                    else:
                        initialized_dependency = parent.root

                    child_tree = dependency[starting_parent_index:]
                    depedency_lineage = child_tree.split(".")
                    current_child = depedency_lineage[0]
                    try:
                        for child_name in depedency_lineage:
                            current_child = child_name
                            initialized_dependency = parent.children[current_child]
                    except KeyError:
                        if initialized_dependency is None:
                            raise AttributeError(f"{dependency} does not exist.")
                        raise NamespaceNotInitializedException(initialized_dependency, current_child)
                    initialized_dependencies.update({dependency: parent.children[dependency]})

            return initialized_dependencies

        @classmethod
        def validate(cls, v: dict) -> PydanticNamespace:
            """
            Validates that the provided object is a valid PydanticNamespace.

            Parameters
            ----------
            v : dict
                The dictionary to create the namespace from.

            Returns
            -------
            PydanticNamespace
                If validated, a namespace will be created in accordance to `generate_namespace`.

            Raises
            ------
            NamespaceNotInitializedException
                If one or more dependencies are initialized, this error will be raised, so the dependency can
                be initialized before continuation.
            """
            if not isinstance(v, dict):
                raise TypeError("Dictionary required")
            parent = None if "parent" not in v else v["parent"]
            dependencies = [] if "dependencies" not in v else v["dependencies"]
            initialized_dependencies = cls.initialize_depedencies(parent, dependencies)

            elements = {} if "elements" not in v else v["elements"]
            children = {} if "children" not in v else v["children"]

            return cls.generate_namespace(parent, initialized_dependencies, elements, children)

        class Config:
            use_enum_values = True

    return PydanticNamespace  # type:ignore
