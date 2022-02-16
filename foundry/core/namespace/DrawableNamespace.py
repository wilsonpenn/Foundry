from foundry.core.drawable.Drawable import DrawableProtocol
from foundry.core.drawable.DrawableGenerator import DrawableGeneratator
from foundry.core.namespace.Namespace import (
    Namespace,
    NamespaceProtocol,
    PydanticNamespace,
)


class PydanticDrawableNamespace(PydanticNamespace):
    elements: dict[str, DrawableGeneratator]

    @property
    def namespace(self) -> NamespaceProtocol[DrawableProtocol]:
        return Namespace(self.namespaces, {k: v.drawable for k, v in self.elements.items()})  # type: ignore
