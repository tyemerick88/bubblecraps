"""Define immutable state values published by a game session."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from crapssim.bet import Bet

from bubblecraps.session.history import RollRecord, SessionHistory
from bubblecraps.session.statistics import SessionStatistics


class GamePhase(Enum):
    """Identify the lifecycle phase of a game session."""

    READY = "ready"
    ROLLING = "rolling"
    RESOLVING = "resolving"
    ANIMATING = "animating"


@dataclass(frozen=True, slots=True)
class AvailableActions:
    """Describe which session commands are currently available."""

    can_roll: bool
    can_place_bets: bool
    can_remove_bets: bool
    can_undo: bool
    can_save: bool
    can_load: bool


@dataclass(frozen=True, slots=True)
class GameState:
    """Represent the immutable state exposed to the controller."""

    phase: GamePhase
    actions: AvailableActions
    bankroll: float
    point: int | None
    puck_on: bool
    bets: list[Bet]
    die1: int | None
    die2: int | None
    last_roll: RollRecord | None
    statistics: SessionStatistics
    history: SessionHistory
