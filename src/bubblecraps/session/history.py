"""Define records for future session history tracking."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum


@dataclass(slots=True)
class RollRecord:
    """Represent one resolved dice roll."""

    die1: int
    die2: int
    total: int
    timestamp: datetime
    shooter_number: int
    point_before: int | None
    point_after: int | None
    bankroll_delta: int
    bet_changes: list[object]


@dataclass(slots=True)
class ShooterRecord:
    """Represent one shooter's session record."""

    shooter_number: int
    rolls: int
    point_numbers_made: list[int]
    profit: int


class SessionEventType(Enum):
    """Identify a significant game-session event."""

    NEW_SESSION = "new_session"
    NEW_SHOOTER = "new_shooter"
    POINT_ESTABLISHED = "point_established"
    POINT_MADE = "point_made"
    SEVEN_OUT = "seven_out"
    UNDO = "undo"
    SESSION_SAVED = "session_saved"
    SESSION_LOADED = "session_loaded"


@dataclass(frozen=True, slots=True)
class SessionEvent:
    """Represent an event retained in session history."""

    timestamp: datetime
    event_type: SessionEventType
    description: str


class SessionHistory:
    """Own the future collection of session history records."""

    rolls: list[RollRecord]
    shooters: list[ShooterRecord]
    events: list[SessionEvent]
