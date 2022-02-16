from pydantic import BaseModel

from foundry.core.namespace import NamespaceType
from foundry.core.namespace.DrawableNamespace import PydanticDrawableNamespace
from foundry.core.namespace.Namespace import PydanticNamespace


class NamespaceGeneratator(BaseModel):
    def __init_subclass__(cls, **kwargs) -> None:
        return super().__init_subclass__(**kwargs)

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def generate_namespace(cls, v: dict) -> PydanticNamespace:
        """
        The constructor for each specific namespace.

        Parameters
        ----------
        v : dict
            The dictionary to create the namespace.

        Returns
        -------
        NamespaceProtocol
            The created namespace as defined by `v["type"]`.

        Raises
        ------
        NotImplementedError
            If the constructor does not have a valid constructor for `v["type"]`.
        """
        type_ = NamespaceType(v["type"])
        if type_ == NamespaceType.DRAWABLE:
            return PydanticDrawableNamespace(**v)
        raise NotImplementedError(f"There is no namespace of type {type_}")

    @classmethod
    def validate(cls, v: dict) -> PydanticNamespace:
        """
        Validates that the provided object is a valid NamespaceProtocol.

        Parameters
        ----------
        v : dict
            The dictionary to create the namespace.

        Returns
        -------
        NamespaceProtocol
            If validated, a namespace will be created in accordance to `generate_drawable`.

        Raises
        ------
        TypeError
            If a dictionary is not provided.
        TypeError
            If the dictionary does not contain the key `"type"`.
        TypeError
            If the type provided is not inside :class:`~foundry.core.namespace.NamespaceProtocol.DrawableType`.
        """
        if not isinstance(v, dict):
            raise TypeError("Dictionary required")
        if "type" not in v:
            raise TypeError("Must have a type")
        if not NamespaceType.has_value(type_ := v["type"]):
            raise TypeError(f"{type_} is not a valid widget type")
        return cls.generate_namespace(v)
