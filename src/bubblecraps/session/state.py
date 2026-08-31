"""Define immutable state values published by a game session."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum, StrEnum

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


class BetType(StrEnum):
    """Identify a bet supported by the Bubble Craps adapter."""

    PASS_LINE = "pass_line"
    DONT_PASS = "dont_pass"
    COME = "come"
    DONT_COME = "dont_come"
    PASS_LINE_ODDS = "pass_line_odds"
    DONT_PASS_ODDS = "dont_pass_odds"
    COME_ODDS = "come_odds"
    DONT_COME_ODDS = "dont_come_odds"
    PLACE = "place"
    BUY = "buy"
    LAY = "lay"
    FIELD = "field"
    C_AND_E = "c_and_e"
    ANY_SEVEN = "any_seven"
    TWO = "two"
    THREE = "three"
    ELEVEN = "eleven"
    TWELVE = "twelve"
    ANY_CRAPS = "any_craps"
    HORN = "horn"
    BIG_SIX = "big_six"
    BIG_EIGHT = "big_eight"
    HARD_WAY = "hard_way"
    HOP = "hop"
    LOW_ROLLS = "low_rolls"
    ROLL_EM_ALL = "roll_em_all"
    HIGH_ROLLS = "high_rolls"


@dataclass(frozen=True, slots=True)
class BetState:
    """Describe an active bet without exposing its engine object."""

    bet_id: str
    bet_type: BetType
    amount: float
    number: int | None = None
    hop_result: tuple[int, int] | None = None
    rolled_numbers: tuple[int, ...] | None = None

    def __post_init__(self) -> None:
        """Require an approved bet type identifier."""
        if not isinstance(self.bet_type, BetType):
            raise TypeError("bet_type must be a BetType")


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
