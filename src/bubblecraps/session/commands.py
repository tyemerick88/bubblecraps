"""Define generic outcomes for session commands."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class CommandStatus(Enum):
    """Identify the generic outcome of a session command."""

    ACCEPTED = "accepted"
    REJECTED = "rejected"
    NOT_IMPLEMENTED = "not_implemented"


@dataclass(frozen=True, slots=True)
class CommandResult:
    """Represent a stable session-command outcome."""

    status: CommandStatus
