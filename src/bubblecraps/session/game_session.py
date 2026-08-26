"""Define the future session orchestration boundary."""

from __future__ import annotations

from crapssim.table import Player, Table

from bubblecraps.session.commands import CommandResult, CommandStatus
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
    # Milestone 3 initializes and owns snapshot capture and restoration.
    undo_stack: list[SessionSnapshot]

    @property
    def state(self) -> GameState:
        """Return the immutable GUI-facing representation of the session."""
        raise NotImplementedError

    def roll(self) -> CommandResult:
        """Placeholder for advancing the session by one roll."""
        raise NotImplementedError

    def undo(self) -> CommandResult:
        """Report that undo is deferred until Milestone 3."""
        return CommandResult(CommandStatus.NOT_IMPLEMENTED)

    def place_bet(self) -> CommandResult:
        """Placeholder for placing a bet through the session."""
        raise NotImplementedError

    def remove_bet(self) -> CommandResult:
        """Placeholder for removing a bet through the session."""
        raise NotImplementedError

    def repeat_last_bet(self) -> CommandResult:
        """Placeholder for repeating the most recently placed bet."""
        raise NotImplementedError

    def double_bet(self) -> CommandResult:
        """Placeholder for doubling the applicable active bets."""
        raise NotImplementedError

    def set_bets_on_or_off(self, working: bool) -> CommandResult:
        """Report that Interblock working-state control is deferred."""
        del working
        return CommandResult(CommandStatus.NOT_IMPLEMENTED)

    def clear_all_bets(self) -> CommandResult:
        """Placeholder for clearing the active bets from the table."""
        raise NotImplementedError

    def new_session(self) -> CommandResult:
        """Placeholder for resetting this game session."""
        raise NotImplementedError

    def save(self, filename: str) -> CommandResult:
        """Report that session persistence is deferred until Milestone 3."""
        del filename
        return CommandResult(CommandStatus.NOT_IMPLEMENTED)

    @classmethod
    def load(cls, filename: str) -> CommandResult:
        """Report that session loading is deferred until Milestone 3."""
        del cls, filename
        return CommandResult(CommandStatus.NOT_IMPLEMENTED)
