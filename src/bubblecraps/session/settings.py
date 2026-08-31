"""Define per-session configuration values."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import StrEnum
from typing import Final, Literal

from crapssim.rules import ClassicRules, CraplessRules, Rules
from crapssim.strategy.tools import NullStrategy
from crapssim.table import Player, Table

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
        """Validate the session configuration fields."""
        if not isinstance(self.ruleset, Ruleset):
            raise TypeError("ruleset must be a Ruleset")
        if not isinstance(self.starting_bankroll, float):
            raise TypeError("starting_bankroll must be a float")
        if not math.isfinite(self.starting_bankroll):
            raise ValueError("starting_bankroll must be finite")
        if self.starting_bankroll <= 0:
            raise ValueError("starting_bankroll must be positive")
        if not isinstance(self.vig_paid_on_win, bool):
            raise TypeError("vig_paid_on_win must be a bool")


def create_table_and_player(
    configuration: SessionConfiguration,
) -> tuple[Table, Player]:
    """Create the engine objects for one interactive session."""
    rules: Rules
    if configuration.ruleset is Ruleset.CLASSIC:
        rules = ClassicRules()
    elif configuration.ruleset is Ruleset.CRAPLESS:
        rules = CraplessRules()
    else:
        raise ValueError(f"Unsupported ruleset: {configuration.ruleset}")

    table = Table(rules=rules)
    table.settings["vig_rounding"] = VIG_ROUNDING
    table.settings["vig_paid_on_win"] = configuration.vig_paid_on_win
    player = table.add_player(
        bankroll=configuration.starting_bankroll,
        strategy=NullStrategy(),
    )
    return table, player
