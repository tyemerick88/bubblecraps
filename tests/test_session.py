from __future__ import annotations

from bubblecraps.session import persistence
from bubblecraps.session.settings import SessionConfiguration


def test_session_configuration_and_persistence_placeholders_are_importable() -> None:
    assert persistence.__doc__ is not None
    assert SessionConfiguration.__doc__ is not None
