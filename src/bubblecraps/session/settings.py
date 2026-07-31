"""Define per-session configuration values."""

from __future__ import annotations

from dataclasses import dataclass

from crapssim.table import TableSettings


@dataclass(frozen=True, slots=True)
class SessionConfiguration:
    """Represent the configuration for one game session."""

    ruleset: str
    table_settings: TableSettings
    casino_profile: str | None
    starting_bankroll: int
