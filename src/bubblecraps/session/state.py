"""Define immutable state values published by a game session."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from bubblecraps.session.history import RollRecord, SessionHistoryState
from bubblecraps.session.statistics import SessionStatisticsState


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
    can_repeat_last_bet: bool
    can_double_bets: bool
    can_clear_bets: bool
    can_set_bets_on_or_off: bool
    can_undo: bool
    can_save: bool
    can_load: bool


@dataclass(frozen=True, slots=True)
class BetState:
    """Describe an active bet without exposing its engine object."""

    bet_id: str
    bet_type: str
    amount: float
    number: int | None = None


@dataclass(frozen=True, slots=True)
class GameState:
    """Represent the immutable state exposed to the controller."""

    phase: GamePhase
    actions: AvailableActions
    bankroll: float
    point: int | None
    puck_on: bool
    bets: tuple[BetState, ...]
    die1: int | None
    die2: int | None
    last_roll: RollRecord | None
    statistics: SessionStatisticsState
    history: SessionHistoryState
