from __future__ import annotations

from PySide6.QtCore import QObject, SignalInstance

from bubblecraps.controller.session_controller import SessionController

CONTROLLER_METHODS = (
    "roll",
    "undo",
    "place_bet",
    "new_session",
    "save",
    "load",
)
CONTROLLER_SIGNALS = (
    "state_changed",
    "session_loaded",
    "session_saved",
    "session_reset",
)


def test_session_controller_exposes_the_qt_bridge_contract() -> None:
    assert issubclass(SessionController, QObject)
    assert isinstance(vars(SessionController)["state"], property)
    assert all(
        callable(getattr(SessionController, method)) for method in CONTROLLER_METHODS
    )

    controller = SessionController()
    assert all(
        isinstance(getattr(controller, signal), SignalInstance)
        for signal in CONTROLLER_SIGNALS
    )
