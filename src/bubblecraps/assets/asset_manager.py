"""Define the semantic interface for presentation asset access."""

from __future__ import annotations


class AssetManager:
    """Isolate GUI widgets from physical asset paths and resource storage."""

    def chip(self, denomination: int) -> object:
        """Return the future chip resource for ``denomination``."""
        raise NotImplementedError

    def die_face(self, value: int) -> object:
        """Return the future die-face resource for ``value``."""
        raise NotImplementedError

    def puck(self) -> object:
        """Return the future puck resource."""
        raise NotImplementedError

    def table_background(self) -> object:
        """Return the future table-background resource."""
        raise NotImplementedError

    def icon(self, name: str) -> object:
        """Return the future icon resource named ``name``."""
        raise NotImplementedError

    def sound(self, name: str) -> object:
        """Return the future sound resource named ``name``."""
        raise NotImplementedError

    def font(self, name: str) -> object:
        """Return the future font resource named ``name``."""
        raise NotImplementedError
