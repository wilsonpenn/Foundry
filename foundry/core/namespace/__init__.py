from enum import Enum


class NamespaceType(str, Enum):
    """
    The type of elements allowed inside the namespace.
    """

    DRAWABLE = "DRAWABLE"

    @classmethod
    def has_value(cls, value: str) -> bool:
        """
        A convenience method to quickly determine if a value is a valid enumeration.

        Parameters
        ----------
        value : str
            The value to check against the enumeration.

        Returns
        -------
        bool
            If the value is inside the enumeration.
        """
        return value in cls._value2member_map_
