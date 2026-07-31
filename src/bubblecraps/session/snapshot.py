"""Define future session snapshots for undo support."""

from __future__ import annotations

from dataclasses import dataclass

from crapssim.table import Player, Table

from bubblecraps.session.history import SessionHistory
from bubblecraps.session.settings import SessionConfiguration
from bubblecraps.session.statistics import SessionStatistics


@dataclass(frozen=True, slots=True)
class SessionSnapshot:
    """Represent an immutable pre-mutation session snapshot."""

    player: Player
    table: Table
    history: SessionHistory
    statistics: SessionStatistics
    settings: SessionConfiguration
