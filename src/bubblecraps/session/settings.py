"""Define per-session configuration values."""

from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Final, Literal

VIG_ROUNDING: Final[Literal["none"]] = "none"
"""Fixed engine vig-rounding policy for Bubble Craps sessions."""


class Ruleset(StrEnum):
    """Identify a ruleset supported by Bubble Craps."""

    CLASSIC = "classic"
    CRAPLESS = "crapless"


@dataclass(frozen=True, slots=True)
class SessionConfiguration:
    """Represent the configuration for one game session."""

    ruleset: Ruleset
    starting_bankroll: float
    vig_paid_on_win: bool = True

    def __post_init__(self) -> None:
        """Reject unparsed ruleset values at the domain boundary."""
        if not isinstance(self.ruleset, Ruleset):
            raise TypeError("ruleset must be a Ruleset")
