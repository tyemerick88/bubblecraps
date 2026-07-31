"""Define the Qt-facing session controller contract."""

from __future__ import annotations

from PySide6.QtCore import QObject, Signal

from bubblecraps.session.state import GameState


class SessionController(QObject):
    """Bridge GUI commands and future session state notifications."""

    state_changed = Signal(GameState)
    session_loaded = Signal()
    session_saved = Signal()
    session_reset = Signal()

    @property
    def state(self) -> GameState:
        """Return the current GUI-facing game state."""
        raise NotImplementedError

    def roll(self) -> None:
        """Placeholder for forwarding a roll command to the session."""

    def undo(self) -> None:
        """Placeholder for forwarding an undo command to the session."""

    def place_bet(self) -> None:
        """Placeholder for forwarding a bet-placement command to the session."""

    def new_session(self) -> None:
        """Placeholder for forwarding a new-session command to the session."""

    def save(self, filename: str) -> None:
        """Placeholder for forwarding a session-save command."""

    def load(self, filename: str) -> None:
        """Placeholder for forwarding a session-load command."""
