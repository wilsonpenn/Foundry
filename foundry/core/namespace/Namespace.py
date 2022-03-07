from __future__ import annotations

from abc import ABC, abstractmethod
from collections import ChainMap, deque
from typing import (
    Any,
    Generic,
    Iterator,
    Optional,
    Protocol,
    Sequence,
    Type,
    TypeVar,
    Union,
)

from attr import attrs, field
from pydantic import BaseModel

from foundry.core.namespace import NamespaceType

_T = TypeVar("_T")


class NamespaceProtocol(Protocol, Generic[_T]):
    """
    A representation of a namespace to hold a series of elements and dependencies inside.  Each element will be
    of the same type whereas, dependencies each can contain their own type respectively.  Each dependency must be
    related to this instance in some way, relative to this instance's parent.  Likewise, this element can contain
    multiple children, who can reference anything that this instance can and this instance or any of this instance's
    other children, assuming that child doesn't also reference it.

    Attributes
    ----------
    parent: Optional[NamespaceProtocol]
        The parent of this namespace, which can be used to find dependencies for itself or its children.  If parent
        is None, then this instance is the root and cannot have any dependencies.
    dependencies: dict[str, NamespaceProtocol]
        A series of dependencies that are included without priority to the scope, or dictionary interface, of this
        instance.  Likewise, other elements of this instance can refer to dependencies' elements.
    elements: dict[str, _T]
        A series of items that can be referred to inside this namespace's scope and can utilize the dependencies.
    children: dict[str, NamespaceProtocol]
        A series of other namespaces that use this instance as its parent.  If any child does not have this instance
        set as its parent, it will automatically be updated to reflect this, provided that this operation is
        possible.
    """

    parent: Optional[NamespaceProtocol]
    dependencies: dict[str, NamespaceProtocol]
    elements: dict[str, _T]
    children: dict[str, NamespaceProtocol]

    @property
    def root(self) -> NamespaceProtocol:
        """
        Finds the namespace without a parent.  From the root node all other namespaces of the same vein should
        be accessible.

        Returns
        -------
        NamespaceProtocol
            The namespace whose parent is None.
        """
        ...

    def __dict__(self) -> dict:
        """
        Converts the namespace to a dict that can be reconstructed back into itself.

        Returns
        -------
        dict
            A dict that represents a namespace.
        """
        ...

    def __getitem__(self, key: str) -> Any:
        ...


_PT = TypeVar("_PT")


class PydanticNamespaceProtocol(Protocol, Generic[_PT]):
    """
    A converted from JSON to a namespace.

    Attributes
    ----------
    parent: Optional[NamespaceProtocol]
        The parent of this namespace, which can be used to find dependencies for itself or its children.  If parent
        is None, then this instance is the root and cannot have any dependencies.
    dependencies: dict[str, NamespaceProtocol]
        A series of dependencies that are included without priority to the scope, or dictionary interface, of this
        instance.  Likewise, other elements of this instance can refer to dependencies' elements.
    elements: dict[str, _PT]
        A series of items that can be referred to inside this namespace's scope and can utilize the dependencies.
    children: dict[str, NamespaceProtocol]
        A series of other namespaces that use this instance as its parent.  If any child does not have this instance
        set as its parent, it will automatically be updated to reflect this, provided that this operation is
        possible.
    """

    parent: Optional[NamespaceProtocol]
    dependencies: dict[str, NamespaceProtocol]
    elements: dict[str, _PT]
    children: dict[str, NamespaceProtocol]

    @property
    def namespace(self) -> NamespaceProtocol[_PT]:
        """
        A converted namespace that encapsulates the full functionality of a namespace.

        Returns
        -------
        NamespaceProtocol[_PT]
            A namespace which represents the JSON parsed inside this namespace.
        """
        ...

    @classmethod
    def validate(cls, v: dict) -> PydanticNamespaceProtocol[_PT]:
        """
        Validates and parses the dict into an instance if applicable.

        Parameters
        ----------
        v : dict
            The JSON data represented as a dict.

        Returns
        -------
        PydanticNamespaceProtocol[_PT]
            The corresponding namespace who represents the data inside the dict.
        """
        ...


class PartialNamespace(Generic[_T], ABC):
    """
    A partial implementation of the NamespaceProtocol.  This provides the core interface for creating a namespace,
    while enabling extension of such elements.

    Attributes
    ----------
    parent: Optional[NamespaceProtocol]
        The parent of this namespace, which can be used to find dependencies for itself or its children.  If parent
        is None, then this instance is the root and cannot have any dependencies.
    dependencies: dict[str, NamespaceProtocol]
        A series of dependencies that are included without priority to the scope, or dictionary interface, of this
        instance.  Likewise, other elements of this instance can refer to dependencies' elements.
    elements: dict[str, _T]
        A series of items that can be referred to inside this namespace's scope and can utilize the dependencies.
    children: dict[str, NamespaceProtocol]
        A series of other namespaces that use this instance as its parent.  If any child does not have this instance
        set as its parent, it will automatically be updated to reflect this, provided that this operation is
        possible.
    """

    parent: Optional[NamespaceProtocol]
    dependencies: dict[str, NamespaceProtocol]
    elements: dict[str, _T]
    children: dict[str, NamespaceProtocol]

    def __eq__(self, other) -> bool:
        """
        Tests for equality between two elements.

        Parameters
        ----------
        other : Any
            The other element to be compared.

        Returns
        -------
        bool
            If these self and other are equivalent.

        Notes
        -----
        The only specification for something to be equal is that is a subclass of PartialNamespace.  Thus any
        children of PartialNamespace can be equal to one another.

        Parent is not checked for equality, as this creates a recursive loop.  Instead, it is advised to check the
        root for equality if such a check is desired.
        """
        if not isinstance(other, PartialNamespace):
            return False

        return (
            self.dependencies == other.dependencies
            and self.elements == other.elements
            and self.children == other.children
        )

    def __iter__(self) -> Iterator:
        return iter(self.public_elements)

    def __getitem__(self, key: str) -> Any:
        return self.public_elements[key]

    def __dict__(self) -> dict:
        """
        Converts the namespace to a dict that can be reconstructed back into itself.

        Returns
        -------
        dict
            A dict that represents a namespace.
        """
        return {
            "dependencies": {k: v.__dict__() for k, v in self.dependencies.items()},
            "elements": self.elements,
            "children": {k: v.__dict__() for k, v in self.children.items()},
        }

    @property
    def public_elements(self) -> ChainMap:
        """
        The entire dict of elements that can be accessed via the dictionary interface.

        Returns
        -------
        ChainMap
            A dict containing the elements of this instance and any public facing elements from its dependencies.
        """
        return ChainMap(self.elements, *[d.elements for d in self.dependencies.values()])

    @property
    def root(self) -> NamespaceProtocol:
        """
        Finds the namespace without a parent.  From the root node all other namespaces of the same vein should
        be accessible.

        Returns
        -------
        NamespaceProtocol
            The namespace whose parent is None.
        """
        parent = self
        while parent.parent is not None:
            assert parent is not parent.parent
            parent = parent.parent
            assert self is not parent

        return parent

    @classmethod
    @abstractmethod
    def from_values(
        cls,
        parent: Optional[NamespaceProtocol],
        dependencies: dict[str, NamespaceProtocol],
        elements: dict[str, _PT],
        children: dict[str, NamespaceProtocol],
    ) -> PartialNamespace[_PT]:
        """
        Creates a namespace with full accordance to the NamespaceProtocol, converting any fields if required.

        Parameters
        ----------
        parent: Optional[NamespaceProtocol]
            The parent of this namespace, which can be used to find dependencies for itself or its children.  If parent
            is None, then this instance is the root and cannot have any dependencies.
        dependencies: dict[str, NamespaceProtocol]
            A series of dependencies that are included without priority to the scope, or dictionary interface, of this
            instance.  Likewise, other elements of this instance can refer to dependencies' elements.
        elements: dict[str, _T]
            A series of items that can be referred to inside this namespace's scope and can utilize the dependencies.
        children: dict[str, NamespaceProtocol]
            A series of other namespaces that use this instance as its parent.  If any child does not have this instance
            set as its parent, it will automatically be updated to reflect this, provided that this operation is
            possible.

        Returns
        -------
        PartialNamespace[_PT]
            The created namespace that represent each of the respective fields from the NamespaceProtocol.
        """
        ...

    @classmethod
    def from_dict(
        cls,
        parent: Optional[dict],
        dependencies: dict[str, dict],
        elements: dict[str, _PT],
        children: dict[str, dict],
    ) -> PartialNamespace[_PT]:
        """
        Creates a namespace back from the __dict__ method, converting any required fields back to a NamespaceProtocol.

        Parameters
        ----------
        parent : Optional[dict]
            The parent of this namespace, which can be used to find dependencies for itself or its children.  If parent
            is None, then this instance is the root and cannot have any dependencies.
        dependencies : dict[str, dict]
            A series of dependencies that are included without priority to the scope, or dictionary interface, of this
            instance.  Likewise, other elements of this instance can refer to dependencies' elements.
        elements : dict[str, _PT]
            A series of items that can be referred to inside this namespace's scope and can utilize the dependencies.
        children : dict[str, dict]
            A series of other namespaces that use this instance as its parent.  If any child does not have this instance
            set as its parent, it will automatically be updated to reflect this, provided that this operation is
            possible.

        Returns
        -------
        PartialNamespace[_PT]
            The created namespace that represent each of the respective fields from the NamespaceProtocol.
        """
        return cls.from_values(
            parent=cls.from_dict(**parent) if parent is not None else None,
            dependencies={k: cls.from_values(parent=None, **v) for k, v in dependencies.items()},
            elements=elements,
            children={k: cls.from_values(parent=None, **v) for k, v in children.items()},
        )

    @classmethod
    def from_namespace(cls, namespace: NamespaceProtocol[_PT]) -> PartialNamespace[_PT]:
        """
        Creates a namespace of this type from any other NamespaceProtocol.

        Parameters
        ----------
        namespace : NamespaceProtocol[_PT]
            The namespace to convert to this type.

        Returns
        -------
        PartialNamespace[_PT]
            The converted namespace.
        """
        return cls.from_values(namespace.parent, namespace.dependencies, namespace.elements, namespace.children)


@attrs(slots=True, auto_attribs=True, cmp=False)
class MutableNamespace(PartialNamespace[_T]):
    parent: Optional[NamespaceProtocol] = field(eq=False, default=None)
    dependencies: dict[str, NamespaceProtocol] = field(default={})
    elements: dict[str, _T] = field(default={})
    children: dict[str, MutableNamespace] = field(default={})

    def __attrs_post_init__(self):
        for child in self.children.values():
            child.parent = self

    @classmethod
    def from_namespace(cls, namespace: NamespaceProtocol[_PT]) -> MutableNamespace[_PT]:
        """
        Creates a namespace of this type from any other NamespaceProtocol.

        Parameters
        ----------
        namespace : NamespaceProtocol[_PT]
            The namespace to convert to this type.

        Returns
        -------
        MutableNamespace[_PT]
            The converted namespace.
        """
        return super().from_namespace(namespace)  # type: ignore

    @classmethod
    def from_values(
        cls,
        parent: Optional[NamespaceProtocol],
        dependencies: dict[str, NamespaceProtocol],
        elements: dict[str, _PT],
        children: dict[str, NamespaceProtocol],
    ) -> MutableNamespace[_PT]:
        """
        Creates a namespace with full accordance to the NamespaceProtocol, converting any fields if required.

        Parameters
        ----------
        parent: Optional[NamespaceProtocol]
            The parent of this namespace, which can be used to find dependencies for itself or its children.  If parent
            is None, then this instance is the root and cannot have any dependencies.
        dependencies: dict[str, NamespaceProtocol]
            A series of dependencies that are included without priority to the scope, or dictionary interface, of this
            instance.  Likewise, other elements of this instance can refer to dependencies' elements.
        elements: dict[str, _T]
            A series of items that can be referred to inside this namespace's scope and can utilize the dependencies.
        children: dict[str, NamespaceProtocol]
            A series of other namespaces that use this instance as its parent.  If any child does not have this instance
            set as its parent, it will automatically be updated to reflect this, provided that this operation is
            possible.

        Returns
        -------
        MutableNamespace[_PT]
            The created namespace that represent each of the respective fields from the NamespaceProtocol.
        """
        return MutableNamespace(parent, dependencies, elements, {k: cls.from_namespace(v) for k, v in children.items()})

    @classmethod
    def from_dict(
        cls,
        parent: Optional[dict],
        dependencies: dict[str, dict],
        elements: dict[str, _PT],
        children: dict[str, dict],
    ) -> MutableNamespace[_PT]:
        return cls.from_values(
            parent=cls.from_dict(**parent) if parent is not None else None,
            dependencies={k: cls.from_values(parent=None, **v) for k, v in dependencies.items()},
            elements=elements,
            children={k: cls.from_values(parent=None, **v) for k, v in children.items()},
        )


@attrs(slots=True, auto_attribs=True, frozen=True, hash=True, cache_hash=True, cmp=False)
class Namespace(PartialNamespace[_T]):
    parent: Optional[NamespaceProtocol] = field(eq=False, default=None)
    dependencies: dict[str, Namespace] = field(default={})
    elements: dict[str, _T] = field(default={})
    children: dict[str, Namespace] = field(default={})

    def __attrs_post_init__(self):
        # Get around frozen object to magically make children connect to parent.
        object.__setattr__(
            self,
            "children",
            {k: Namespace.from_values(self, v.dependencies, v.elements, v.children) for k, v in self.children.items()},
        )

    @classmethod
    def from_namespace(cls, namespace: NamespaceProtocol[_PT]) -> Namespace[_PT]:
        return super().from_namespace(namespace)  # type: ignore

    @classmethod
    def from_dict(
        cls,
        parent: Optional[dict],
        dependencies: dict[str, dict],
        elements: dict[str, _PT],
        children: dict[str, dict],
    ) -> Namespace[_PT]:
        return Namespace.from_namespace(MutableNamespace.from_dict(parent, dependencies, elements, children))

    @classmethod
    def from_values(
        cls,
        parent: Optional[NamespaceProtocol],
        dependencies: dict[str, NamespaceProtocol],
        elements: dict[str, _PT],
        children: dict[str, NamespaceProtocol],
    ) -> Namespace[_PT]:
        dependencies_ = {
            s: d if isinstance(d, Namespace) else Namespace.from_namespace(d) for s, d in dependencies.items()
        }
        children_ = {s: c if isinstance(c, Namespace) else Namespace.from_namespace(c) for s, c in children.items()}

        return Namespace(parent, dependencies_, elements, children_)


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
