from foundry.core.namespace.Namespace import MutableNamespace, Namespace


def test_namespace_initialization_empty():
    Namespace(None, {}, {}, {})


def test_namespace_initialization_with_parent(empty_namespace):
    Namespace(empty_namespace, {}, {}, {})


def test_namespace_initialization_empty_with_dependency(empty_namespace):
    Namespace(None, {"a": empty_namespace}, {}, {})


def test_namespace_initialization_with_parent_with_dependency(empty_namespace):
    Namespace(empty_namespace, {"a": empty_namespace}, {}, {})


def test_namespace_initialization_empty_with_dependencies(empty_namespace):
    Namespace(None, {"a": empty_namespace, "b": empty_namespace}, {}, {})


def test_namespace_initialization_with_parent_with_dependencies(empty_namespace):
    Namespace(empty_namespace, {"a": empty_namespace, "b": empty_namespace}, {}, {})


def test_namespace_initialization_empty_with_dependency_with_child(empty_namespace):
    Namespace(None, {"a": empty_namespace}, {}, {"a": empty_namespace})


def test_namespace_initialization_with_parent_with_dependency_with_child(empty_namespace):
    Namespace(empty_namespace, {"a": empty_namespace}, {}, {"a": empty_namespace})


def test_namespace_initialization_empty_with_dependencies_with_child(empty_namespace):
    Namespace(None, {"a": empty_namespace, "b": empty_namespace}, {}, {"a": empty_namespace})


def test_namespace_initialization_with_parent_with_dependencies_with_child(empty_namespace):
    Namespace(empty_namespace, {"a": empty_namespace, "b": empty_namespace}, {}, {"a": empty_namespace})


def test_namespace_initialization_empty_with_dependency_with_children(empty_namespace):
    Namespace(None, {"a": empty_namespace}, {}, {"a": empty_namespace, "b": empty_namespace})


def test_namespace_initialization_with_parent_with_dependency_with_children(empty_namespace):
    Namespace(empty_namespace, {"a": empty_namespace}, {}, {"a": empty_namespace, "b": empty_namespace})


def test_namespace_initialization_empty_with_dependencies_with_children(empty_namespace):
    Namespace(None, {"a": empty_namespace, "b": empty_namespace}, {}, {"a": empty_namespace, "b": empty_namespace})


def test_namespace_initialization_with_parent_with_dependencies_with_children(empty_namespace):
    Namespace(
        empty_namespace, {"a": empty_namespace, "b": empty_namespace}, {}, {"a": empty_namespace, "b": empty_namespace}
    )


def test_namespace_initialization_empty_with_dependency_with_child_with_element(empty_namespace):
    Namespace(None, {"a": empty_namespace}, {"c": 1}, {"a": empty_namespace})


def test_namespace_initialization_with_parent_with_dependency_with_child_with_element(empty_namespace):
    Namespace(empty_namespace, {"a": empty_namespace}, {"c": 1}, {"a": empty_namespace})


def test_namespace_initialization_empty_with_dependencies_with_child_with_element(empty_namespace):
    Namespace(None, {"a": empty_namespace, "b": empty_namespace}, {"c": 1}, {"a": empty_namespace})


def test_namespace_initialization_with_parent_with_dependencies_with_child_with_element(empty_namespace):
    Namespace(empty_namespace, {"a": empty_namespace, "b": empty_namespace}, {"c": 1}, {"a": empty_namespace})


def test_namespace_initialization_empty_with_dependency_with_children_with_element(empty_namespace):
    Namespace(None, {"a": empty_namespace}, {"c": 1}, {"a": empty_namespace, "b": empty_namespace})


def test_namespace_initialization_with_parent_with_dependency_with_children_with_element(empty_namespace):
    Namespace(empty_namespace, {"a": empty_namespace}, {"c": 1}, {"a": empty_namespace, "b": empty_namespace})


def test_namespace_initialization_empty_with_dependencies_with_children_with_element(empty_namespace):
    Namespace(
        None, {"a": empty_namespace, "b": empty_namespace}, {"c": 1}, {"a": empty_namespace, "b": empty_namespace}
    )


def test_namespace_initialization_with_parent_with_dependencies_with_children_with_element(empty_namespace):
    Namespace(
        empty_namespace,
        {"a": empty_namespace, "b": empty_namespace},
        {"c": 1},
        {"a": empty_namespace, "b": empty_namespace},
    )


def test_namespace_initialization_empty_with_dependency_with_child_with_elements(empty_namespace):
    Namespace(None, {"a": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace})


def test_namespace_initialization_with_parent_with_dependency_with_child_with_elements(empty_namespace):
    Namespace(empty_namespace, {"a": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace})


def test_namespace_initialization_empty_with_dependencies_with_child_with_elements(empty_namespace):
    Namespace(None, {"a": empty_namespace, "b": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace})


def test_namespace_initialization_with_parent_with_dependencies_with_child_with_elements(empty_namespace):
    Namespace(empty_namespace, {"a": empty_namespace, "b": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace})


def test_namespace_initialization_empty_with_dependency_with_children_with_elements(empty_namespace):
    Namespace(None, {"a": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace, "b": empty_namespace})


def test_namespace_initialization_with_parent_with_dependency_with_children_with_elements(empty_namespace):
    Namespace(empty_namespace, {"a": empty_namespace}, {"c": 1, "d": 2}, {"a": empty_namespace, "b": empty_namespace})


def test_namespace_initialization_empty_with_dependencies_with_children_with_elements(empty_namespace):
    Namespace(
        None,
        {"a": empty_namespace, "b": empty_namespace},
        {"c": 1, "d": 2},
        {"a": empty_namespace, "b": empty_namespace},
    )


def test_namespace_initialization_with_parent_with_dependencies_with_children_with_elements(empty_namespace):
    Namespace(
        empty_namespace,
        {"a": empty_namespace, "b": empty_namespace},
        {"c": 1, "d": 2},
        {"a": empty_namespace, "b": empty_namespace},
    )


def test_mutable_namespace_initialization_empty():
    MutableNamespace(None, {}, {}, {})


def test_mutable_namespace_initialization_with_parent(empty_mutable_namespace):
    MutableNamespace(empty_mutable_namespace, {}, {}, {})


def test_mutable_namespace_initialization_empty_with_dependency(empty_mutable_namespace):
    MutableNamespace(None, {"a": empty_mutable_namespace}, {}, {})


def test_mutable_namespace_initialization_with_parent_with_dependency(empty_mutable_namespace):
    MutableNamespace(empty_mutable_namespace, {"a": empty_mutable_namespace}, {}, {})


def test_mutable_namespace_initialization_empty_with_dependencies(empty_mutable_namespace):
    MutableNamespace(None, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}, {}, {})


def test_mutable_namespace_initialization_with_parent_with_dependencies(empty_mutable_namespace):
    MutableNamespace(empty_mutable_namespace, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}, {}, {})


def test_mutable_namespace_initialization_empty_with_dependency_with_child(empty_mutable_namespace):
    MutableNamespace(None, {"a": empty_mutable_namespace}, {}, {"a": empty_mutable_namespace})


def test_mutable_namespace_initialization_with_parent_with_dependency_with_child(empty_mutable_namespace):
    MutableNamespace(empty_mutable_namespace, {"a": empty_mutable_namespace}, {}, {"a": empty_mutable_namespace})


def test_mutable_namespace_initialization_empty_with_dependencies_with_child(empty_mutable_namespace):
    MutableNamespace(
        None, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}, {}, {"a": empty_mutable_namespace}
    )


def test_mutable_namespace_initialization_with_parent_with_dependencies_with_child(empty_mutable_namespace):
    MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {},
        {"a": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_empty_with_dependency_with_children(empty_mutable_namespace):
    MutableNamespace(
        None, {"a": empty_mutable_namespace}, {}, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}
    )


def test_mutable_namespace_initialization_with_parent_with_dependency_with_children(empty_mutable_namespace):
    MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace},
        {},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_empty_with_dependencies_with_children(empty_mutable_namespace):
    MutableNamespace(
        None,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_with_parent_with_dependencies_with_children(empty_mutable_namespace):
    MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_empty_with_dependency_with_child_with_element(empty_mutable_namespace):
    MutableNamespace(None, {"a": empty_mutable_namespace}, {"c": 1}, {"a": empty_mutable_namespace})


def test_mutable_namespace_initialization_with_parent_with_dependency_with_child_with_element(empty_mutable_namespace):
    MutableNamespace(empty_mutable_namespace, {"a": empty_mutable_namespace}, {"c": 1}, {"a": empty_mutable_namespace})


def test_mutable_namespace_initialization_empty_with_dependencies_with_child_with_element(empty_mutable_namespace):
    MutableNamespace(
        None, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}, {"c": 1}, {"a": empty_mutable_namespace}
    )


def test_mutable_namespace_initialization_with_parent_with_dependencies_with_child_with_element(
    empty_mutable_namespace,
):
    MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1},
        {"a": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_empty_with_dependency_with_children_with_element(empty_mutable_namespace):
    MutableNamespace(
        None, {"a": empty_mutable_namespace}, {"c": 1}, {"a": empty_mutable_namespace, "b": empty_mutable_namespace}
    )


def test_mutable_namespace_initialization_with_parent_with_dependency_with_children_with_element(
    empty_mutable_namespace,
):
    MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace},
        {"c": 1},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_empty_with_dependencies_with_children_with_element(empty_mutable_namespace):
    MutableNamespace(
        None,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_with_parent_with_dependencies_with_children_with_element(
    empty_mutable_namespace,
):
    MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_empty_with_dependency_with_child_with_elements(empty_mutable_namespace):
    MutableNamespace(None, {"a": empty_mutable_namespace}, {"c": 1, "d": 2}, {"a": empty_mutable_namespace})


def test_mutable_namespace_initialization_with_parent_with_dependency_with_child_with_elements(empty_mutable_namespace):
    MutableNamespace(
        empty_mutable_namespace, {"a": empty_mutable_namespace}, {"c": 1, "d": 2}, {"a": empty_mutable_namespace}
    )


def test_mutable_namespace_initialization_empty_with_dependencies_with_child_with_elements(empty_mutable_namespace):
    MutableNamespace(
        None,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_with_parent_with_dependencies_with_child_with_elements(
    empty_mutable_namespace,
):
    MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_empty_with_dependency_with_children_with_elements(empty_mutable_namespace):
    MutableNamespace(
        None,
        {"a": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_with_parent_with_dependency_with_children_with_elements(
    empty_mutable_namespace,
):
    MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_empty_with_dependencies_with_children_with_elements(empty_mutable_namespace):
    MutableNamespace(
        None,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


def test_mutable_namespace_initialization_with_parent_with_dependencies_with_children_with_elements(
    empty_mutable_namespace,
):
    MutableNamespace(
        empty_mutable_namespace,
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
        {"c": 1, "d": 2},
        {"a": empty_mutable_namespace, "b": empty_mutable_namespace},
    )


def test_namespace_from_dict_is_equal(all_namespaces):
    for namespace in all_namespaces:
        namespace_from_dict = Namespace.from_dict(parent=None, **namespace.__dict__())
        assert namespace == namespace_from_dict
        assert isinstance(namespace_from_dict, Namespace)
        for child in namespace_from_dict.children.values():
            assert namespace_from_dict is child.parent


def test_mutable_namespace_from_dict_is_equal(all_namespaces):
    for namespace in all_namespaces:
        namespace_from_dict = MutableNamespace.from_dict(parent=None, **namespace.__dict__())
        assert namespace == namespace_from_dict
        assert isinstance(namespace_from_dict, MutableNamespace)
        for child in namespace_from_dict.children.values():
            assert namespace_from_dict is child.parent


def test_namespace_from_namespace_is_equal(all_namespaces):
    for namespace in all_namespaces:
        namespace_from_namespace = Namespace.from_namespace(namespace)
        assert namespace == namespace_from_namespace
        assert isinstance(namespace_from_namespace, Namespace)
        for child in namespace_from_namespace.children.values():
            assert namespace_from_namespace is child.parent


def test_mutable_namespace_from_namespace_is_equal(all_namespaces):
    for namespace in all_namespaces:
        namespace_from_namespace = MutableNamespace.from_namespace(namespace)
        assert namespace == namespace_from_namespace
        assert isinstance(namespace_from_namespace, MutableNamespace)
        for child in namespace_from_namespace.children.values():
            assert namespace_from_namespace is child.parent
