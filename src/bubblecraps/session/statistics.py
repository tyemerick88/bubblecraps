"""Define the future owner of session statistics."""

from __future__ import annotations

from dataclasses import dataclass


class SessionStatistics:
    """Own future aggregate statistics for a game session."""


@dataclass(frozen=True, slots=True)
class SessionStatisticsState:
    """Represent detached, immutable aggregate session statistics."""

    total_rolls: int = 0
    total_shooters_started: int = 0
    points_established: int = 0
    points_made: int = 0
    seven_outs: int = 0
    net_total_player_cash_change: float = 0.0
