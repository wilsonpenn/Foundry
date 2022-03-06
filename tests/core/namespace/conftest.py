from pytest import fixture

from foundry.core.namespace.Namespace import MutableNamespace, Namespace


@fixture
def empty_namespace():
    return Namespace(None, {}, {}, {})


@fixture
def namespace_with_parent(empty_namespace):
    return Namespace(empty_namespace, {}, {}, {})


@fixture
def namespace_with_dependency(empty_namespace):
    return Namespace(None, {"a": empty_namespace}, {}, {})


@fixture
def namespace_with_parent_with_dependency(empty_namespace):
    return Namespace(empty_namespace, {"a": empty_namespace}, {}, {})


@fixture
def namespace_with_dependencies(empty_namespace):
    return Namespace(None, {"a": empty_namespace, "b": empty_namespace}, {}, {})


@fixture
def namespace_with_parent_with_dependencies(empty_namespace):
    return Namespace(empty_namespace, {"a": empty_namespace, "b": empty_namespace}, {}, {})


@fixture
def namespace_with_dependency_with_child(empty_namespace):
    return Namespace(None, {"a": empty_namespace}, {}, {"a": empty_namespace})


@fixture
def namespace_with_parent_with_dependency_with_child(empty_namespace):
    return Namespace(empty_namespace, {"a": empty_namespace}, {}, {"a": empty_namespace})


@fixture
def namespace_with_dependencies_with_child(empty_namespace):
    return Namespace(None, {"a": empty_namespace, "b": empty_namespace}, {}, {"a": empty_namespace})


@fixture
def namespace_with_parent_with_dependencies_with_child(empty_namespace):
    return Namespace(empty_namespace, {"a": empty_namespace, "b": empty_namespace}, {}, {"a": empty_namespace})


@fixture
def namespace_with_dependency_with_children(empty_namespace):
    return Namespace(None, {"a": empty_namespace}, {}, {"a": empty_namespace, "b": empty_namespace})


@fixture
def namespace_with_parent_with_dependency_with_children(empty_namespace):
    return Namespace(empty_namespace, {"a": empty_namespace}, {}, {"a": empty_namespace, "b": empty_namespace})


@fixture
def namespace_with_dependencies_with_children(empty_namespace):
    return Namespace(
        None, {"a": empty_namespace, "b": empty_namespace}, {}, {"a": empty_namespace, "b": empty_namespace}
    )


@fixture
def namespace_with_parent_with_dependencies_with_children(empty_namespace):
    return Namespace(
        empty_namespace, {"a": empty_namespace, "b": empty_namespace}, {}, {"a": empty_namespace, "b": empty_namespace}
    )


@fixture
def namespace_with_dependency_with_child_with_element(empty_namespace):
    return Namespace(None, {"a": empty_namespace}, {"c": 1}, {"a": empty_namespace})


@fixture
def namespace_with_parent_with_dependency_with_child_with_element(empty_namespace):
    return Namespace(empty_namespace, {"a": empty_namespace}, {"c": 1}, {"a": empty_namespace})


@fixture
def namespace_with_dependencies_with_child_with_element(empty_namespace):
    return Namespace(None, {"a": empty_namespace, "b": empty_namespace}, {"c": 1}, {"a": empty_namespace})


@fixture
def namespace_with_parent_with_dependencies_with_child_with_element(empty_namespace):
    return Namespace(empty_namespace, {"a": empty_namespace, "b": empty_namespace}, {"c": 1}, {"a": empty_namespace})


@fixture
def namespace_with_dependency_with_children_with_element(empty_namespace):
    return Namespace(None, {"a": empty_namespace}, {"c": 1}, {"a": empty_namespace, "b": empty_namespace})


@fixture
def namespace_with_parent_with_dependency_with_children_with_element(empty_namespace):
    return Namespace(empty_namespace, {"a": empty_namespace}, {"c": 1}, {"a": empty_namespace, "b": empty_namespace})


@fixture
def namespace_with_dependencies_with_children_with_element(empty_namespace):
    return Namespace(
        None, {"a": empty_namespace, "b": empty_namespace}, {"c": 1}, {"a": empty_namespace, "b": empty_namespace}
    )


@fixture
def namespace_with_parent_with_dependencies_with_children_with_element(empty_namespace):
    return Namespace(
        empty_namespace,
        {"a": empty_namespace, "b": empty_namespace},
        {"c": 1},
        {"a": empty_namespace, "b": empty_namespace},
    )


@fixture
def namespace_with_dependency_with_child_with_elements(empty_namespace):
    return Namespace(None, {"a": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace})


@fixture
def namespace_with_parent_with_dependency_with_child_with_elements(empty_namespace):
    return Namespace(empty_namespace, {"a": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace})


@fixture
def namespace_empty_with_dependencies_with_child_with_elements(empty_namespace):
    return Namespace(None, {"a": empty_namespace, "b": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace})


@fixture
def namespace_with_parent_with_dependencies_with_child_with_elements(empty_namespace):
    return Namespace(
        empty_namespace, {"a": empty_namespace, "b": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace}
    )


@fixture
def namespace_empty_with_dependency_with_children_with_elements(empty_namespace):
    return Namespace(None, {"a": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace, "b": empty_namespace})


@fixture
def namespace_with_parent_with_dependency_with_children_with_elements(empty_namespace):
    return Namespace(
        empty_namespace, {"a": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace, "b": empty_namespace}
    )


@fixture
def namespace_empty_with_dependencies_with_children_with_elements(empty_namespace):
    return Namespace(
        None,
        {"a": empty_namespace, "b": empty_namespace},
        {"c": 1, "d": 2},
        {"a": empty_namespace, "b": empty_namespace},
    )


@fixture
def namespace_with_parent_with_dependencies_with_children_with_elements(empty_namespace):
    return Namespace(
        empty_namespace,
        {"a": empty_namespace, "b": empty_namespace},
        {"c": 1, "d": 2},
        {"a": empty_namespace, "b": empty_namespace},
    )


@fixture
def empty_mutable_namespace():
    return MutableNamespace(None, {}, {}, {})


@fixture
def mutable_namespace_with_parent(empty_mutable_namespace):
    return MutableNamespace(empty_mutable_namespace, {}, {}, {})


@fixture
def mutable_namespace_with_dependency(empty_mutable_namespace):
    return MutableNamespace(None, {"a": empty_mutable_namespace}, {}, {})


@fixture
def mutable_namespace_with_parent_with_dependency(empty_mutable_namespace):
    return MutableNamespace(empty_mutable_namespace, {"a": empty_mutable_namespace}, {}, {})


@fixture
def mutable_namespace_with_dependencies(empty_mutable_namespace):
    return MutableNamespace(None, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}, {}, {})


@fixture
def mutable_namespace_with_parent_with_dependencies(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}, {}, {}
    )


@fixture
def mutable_namespace_with_dependency_with_child(empty_mutable_namespace):
    return MutableNamespace(None, {"a": empty_mutable_namespace}, {}, {"a": empty_mutable_namespace})


@fixture
def mutable_namespace_with_parent_with_dependency_with_child(empty_mutable_namespace):
    return MutableNamespace(empty_mutable_namespace, {"a": empty_mutable_namespace}, {}, {"a": empty_mutable_namespace})


@fixture
def mutable_namespace_with_dependencies_with_child(empty_mutable_namespace):
    return MutableNamespace(
        None, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}, {}, {"a": empty_mutable_namespace}
    )


@fixture
def mutable_namespace_with_parent_with_dependencies_with_child(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {},
        {"a": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_with_dependency_with_children(empty_mutable_namespace):
    return MutableNamespace(
        None, {"a": empty_mutable_namespace}, {}, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}
    )


@fixture
def mutable_namespace_with_parent_with_dependency_with_children(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace},
        {},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_with_dependencies_with_children(empty_mutable_namespace):
    return MutableNamespace(
        None,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_with_parent_with_dependencies_with_children(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_with_dependency_with_child_with_element(empty_mutable_namespace):
    return MutableNamespace(None, {"a": empty_mutable_namespace}, {"c": 1}, {"a": empty_mutable_namespace})


@fixture
def mutable_namespace_with_parent_with_dependency_with_child_with_element(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace, {"a": empty_mutable_namespace}, {"c": 1}, {"a": empty_mutable_namespace}
    )


@fixture
def mutable_namespace_with_dependencies_with_child_with_element(empty_mutable_namespace):
    return MutableNamespace(
        None, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}, {"c": 1}, {"a": empty_mutable_namespace}
    )


@fixture
def mutable_namespace_with_parent_with_dependencies_with_child_with_element(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1},
        {"a": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_with_dependency_with_children_with_element(empty_mutable_namespace):
    return MutableNamespace(
        None, {"a": empty_mutable_namespace}, {"c": 1}, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}
    )


@fixture
def mutable_namespace_with_parent_with_dependency_with_children_with_element(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace},
        {"c": 1},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_with_dependencies_with_children_with_element(empty_mutable_namespace):
    return MutableNamespace(
        None,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_with_parent_with_dependencies_with_children_with_element(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_with_dependency_with_child_with_elements(empty_mutable_namespace):
    return MutableNamespace(None, {"a": empty_mutable_namespace}, {"c": 1, "d": 2}, {"a": empty_mutable_namespace})


@fixture
def mutable_namespace_with_parent_with_dependency_with_child_with_elements(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace, {"a": empty_mutable_namespace}, {"c": 1, "d": 2}, {"a": empty_mutable_namespace}
    )


@fixture
def mutable_namespace_empty_with_dependencies_with_child_with_elements(empty_mutable_namespace):
    return MutableNamespace(
        None,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_with_parent_with_dependencies_with_child_with_elements(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_empty_with_dependency_with_children_with_elements(empty_mutable_namespace):
    return MutableNamespace(
        None,
        {"a": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_with_parent_with_dependency_with_children_with_elements(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_empty_with_dependencies_with_children_with_elements(empty_mutable_namespace):
    return MutableNamespace(
        None,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


@fixture
def mutable_namespace_with_parent_with_dependencies_with_children_with_elements(empty_mutable_namespace):
    return MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


@fixture
def all_namespaces(
    empty_namespace,
    empty_mutable_namespace,
    namespace_with_parent,
    mutable_namespace_with_parent,
    namespace_with_parent_with_dependencies,
    mutable_namespace_with_parent_with_dependencies,
    namespace_with_dependency,
    mutable_namespace_with_dependency,
    namespace_with_dependency_with_child,
    mutable_namespace_with_dependency_with_child,
    namespace_with_parent_with_dependency,
    mutable_namespace_with_parent_with_dependency,
    namespace_with_parent_with_dependency_with_child,
    mutable_namespace_with_parent_with_dependency_with_child,
    namespace_with_dependencies,
    mutable_namespace_with_dependencies,
    namespace_with_dependencies_with_child,
    mutable_namespace_with_dependencies_with_child,
    namespace_with_parent_with_dependencies_with_child,
    mutable_namespace_with_parent_with_dependencies_with_child,
    namespace_with_dependency_with_children,
    mutable_namespace_with_dependency_with_children,
    namespace_with_parent_with_dependencies_with_children,
    mutable_namespace_with_parent_with_dependencies_with_children,
    namespace_with_dependencies_with_child_with_element,
    mutable_namespace_with_dependencies_with_child_with_element,
    namespace_with_parent_with_dependency_with_children,
    mutable_namespace_with_parent_with_dependency_with_children,
    namespace_with_parent_with_dependency_with_child_with_element,
    mutable_namespace_with_parent_with_dependency_with_child_with_element,
    namespace_with_dependencies_with_children,
    mutable_namespace_with_dependencies_with_children,
    namespace_with_dependency_with_children_with_element,
    mutable_namespace_with_dependency_with_children_with_element,
    namespace_with_dependency_with_child_with_element,
    mutable_namespace_with_dependency_with_child_with_element,
    namespace_with_dependencies_with_children_with_element,
    mutable_namespace_with_dependencies_with_children_with_element,
    namespace_with_dependency_with_child_with_elements,
    mutable_namespace_with_dependency_with_child_with_elements,
    namespace_with_parent_with_dependencies_with_child_with_element,
    mutable_namespace_with_parent_with_dependencies_with_child_with_element,
    namespace_with_parent_with_dependency_with_child_with_elements,
    mutable_namespace_with_parent_with_dependency_with_child_with_elements,
    namespace_empty_with_dependency_with_children_with_elements,
    mutable_namespace_empty_with_dependency_with_children_with_elements,
    namespace_with_parent_with_dependency_with_children_with_element,
    mutable_namespace_with_parent_with_dependency_with_children_with_element,
    namespace_with_parent_with_dependencies_with_child_with_elements,
    mutable_namespace_with_parent_with_dependencies_with_child_with_elements,
    namespace_with_parent_with_dependencies_with_children_with_elements,
    mutable_namespace_with_parent_with_dependencies_with_children_with_elements,
    namespace_with_parent_with_dependencies_with_children_with_element,
    mutable_namespace_with_parent_with_dependencies_with_children_with_element,
    namespace_empty_with_dependencies_with_children_with_elements,
    mutable_namespace_empty_with_dependencies_with_children_with_elements,
    namespace_empty_with_dependencies_with_child_with_elements,
    mutable_namespace_empty_with_dependencies_with_child_with_elements,
    namespace_with_parent_with_dependency_with_children_with_elements,
    mutable_namespace_with_parent_with_dependency_with_children_with_elements,
):

    return [
        empty_namespace,
        empty_mutable_namespace,
        namespace_with_parent,
        mutable_namespace_with_parent,
        namespace_with_parent_with_dependencies,
        mutable_namespace_with_parent_with_dependencies,
        namespace_with_dependency,
        mutable_namespace_with_dependency,
        namespace_with_dependency_with_child,
        mutable_namespace_with_dependency_with_child,
        namespace_with_parent_with_dependency,
        mutable_namespace_with_parent_with_dependency,
        namespace_with_parent_with_dependency_with_child,
        mutable_namespace_with_parent_with_dependency_with_child,
        namespace_with_dependencies,
        mutable_namespace_with_dependencies,
        namespace_with_dependencies_with_child,
        mutable_namespace_with_dependencies_with_child,
        namespace_with_parent_with_dependencies_with_child,
        mutable_namespace_with_parent_with_dependencies_with_child,
        namespace_with_dependency_with_children,
        mutable_namespace_with_dependency_with_children,
        namespace_with_parent_with_dependencies_with_children,
        mutable_namespace_with_parent_with_dependencies_with_children,
        namespace_with_dependencies_with_child_with_element,
        mutable_namespace_with_dependencies_with_child_with_element,
        namespace_with_parent_with_dependency_with_children,
        mutable_namespace_with_parent_with_dependency_with_children,
        namespace_with_parent_with_dependency_with_child_with_element,
        mutable_namespace_with_parent_with_dependency_with_child_with_element,
        namespace_with_dependencies_with_children,
        mutable_namespace_with_dependencies_with_children,
        namespace_with_dependency_with_children_with_element,
        mutable_namespace_with_dependency_with_children_with_element,
        namespace_with_dependency_with_child_with_element,
        mutable_namespace_with_dependency_with_child_with_element,
        namespace_with_dependencies_with_children_with_element,
        mutable_namespace_with_dependencies_with_children_with_element,
        namespace_with_dependency_with_child_with_elements,
        mutable_namespace_with_dependency_with_child_with_elements,
        namespace_with_parent_with_dependencies_with_child_with_element,
        mutable_namespace_with_parent_with_dependencies_with_child_with_element,
        namespace_with_parent_with_dependency_with_child_with_elements,
        mutable_namespace_with_parent_with_dependency_with_child_with_elements,
        namespace_empty_with_dependency_with_children_with_elements,
        mutable_namespace_empty_with_dependency_with_children_with_elements,
        namespace_with_parent_with_dependency_with_children_with_element,
        mutable_namespace_with_parent_with_dependency_with_children_with_element,
        namespace_with_parent_with_dependencies_with_child_with_elements,
        mutable_namespace_with_parent_with_dependencies_with_child_with_elements,
        namespace_with_parent_with_dependencies_with_children_with_elements,
        mutable_namespace_with_parent_with_dependencies_with_children_with_elements,
        namespace_with_parent_with_dependencies_with_children_with_element,
        mutable_namespace_with_parent_with_dependencies_with_children_with_element,
        namespace_empty_with_dependencies_with_children_with_elements,
        mutable_namespace_empty_with_dependencies_with_children_with_elements,
        namespace_empty_with_dependencies_with_child_with_elements,
        mutable_namespace_empty_with_dependencies_with_child_with_elements,
        namespace_with_parent_with_dependency_with_children_with_elements,
        mutable_namespace_with_parent_with_dependency_with_children_with_elements,
    ]
