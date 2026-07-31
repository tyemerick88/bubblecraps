"""Define the future session orchestration boundary."""

from __future__ import annotations

from typing import Self

from crapssim.table import Player, Table

from bubblecraps.session.history import SessionHistory
from bubblecraps.session.settings import SessionConfiguration
from bubblecraps.session.snapshot import SessionSnapshot
from bubblecraps.session.state import GameState
from bubblecraps.session.statistics import SessionStatistics


class GameSession:
    """Own future session mutations and crapssim orchestration."""

    table: Table
    player: Player
    history: SessionHistory
    statistics: SessionStatistics
    settings: SessionConfiguration
    undo_stack: list[SessionSnapshot]

    @property
    def state(self) -> GameState:
        """Return the immutable GUI-facing representation of the session."""
        raise NotImplementedError

    def roll(self) -> None:
        """Placeholder for advancing the session by one roll."""

    def undo(self) -> None:
        """Placeholder for restoring the previous session snapshot."""

    def place_bet(self) -> None:
        """Placeholder for placing a bet through the session."""

    def repeat_last_bet(self) -> None:
        """Placeholder for repeating the most recently placed bet."""

    def double_bet(self) -> None:
        """Placeholder for doubling the applicable active bets."""

    def set_bets_on_or_off(self) -> None:
        """Placeholder for toggling the working state of active bets."""

    def clear_all_bets(self) -> None:
        """Placeholder for clearing the active bets from the table."""

    def new_session(self) -> None:
        """Placeholder for resetting this game session."""

    def save(self, filename: str) -> None:
        """Placeholder for saving this session to ``filename``."""

    @classmethod
    def load(cls, filename: str) -> Self:
        """Placeholder for loading a session from ``filename``."""
        raise NotImplementedError
