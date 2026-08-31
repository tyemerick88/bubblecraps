from __future__ import annotations

from copy import deepcopy

import pytest
from crapssim.rules import ClassicRules, CraplessRules
from crapssim.strategy.tools import NullStrategy
from crapssim.table import Table

from bubblecraps.session.settings import (
    VIG_ROUNDING,
    Ruleset,
    SessionConfiguration,
    create_table_and_player,
)

STARTING_BANKROLL = 250.0


@pytest.mark.parametrize("starting_bankroll", [0.0, -1.0])
def test_session_configuration_rejects_non_positive_bankroll(
    starting_bankroll: float,
) -> None:
    with pytest.raises(ValueError, match="starting_bankroll must be positive"):
        SessionConfiguration(
            ruleset=Ruleset.CLASSIC,
            starting_bankroll=starting_bankroll,
        )


@pytest.mark.parametrize(
    "starting_bankroll", [float("inf"), float("-inf"), float("nan")]
)
def test_session_configuration_rejects_non_finite_bankroll(
    starting_bankroll: float,
) -> None:
    with pytest.raises(ValueError, match="starting_bankroll must be finite"):
        SessionConfiguration(
            ruleset=Ruleset.CLASSIC,
            starting_bankroll=starting_bankroll,
        )


@pytest.mark.parametrize("starting_bankroll", [100, True, "100"])
def test_session_configuration_requires_float_bankroll(
    starting_bankroll: object,
) -> None:
    with pytest.raises(TypeError, match="starting_bankroll must be a float"):
        SessionConfiguration(
            ruleset=Ruleset.CLASSIC,
            starting_bankroll=starting_bankroll,  # type: ignore[arg-type]
        )


def test_session_configuration_requires_boolean_vig_policy() -> None:
    with pytest.raises(TypeError, match="vig_paid_on_win must be a bool"):
        SessionConfiguration(
            ruleset=Ruleset.CLASSIC,
            starting_bankroll=100.0,
            vig_paid_on_win=1,  # type: ignore[arg-type]
        )


@pytest.mark.parametrize(
    ("ruleset", "rules_type"),
    [
        (Ruleset.CLASSIC, ClassicRules),
        (Ruleset.CRAPLESS, CraplessRules),
    ],
)
@pytest.mark.parametrize("vig_paid_on_win", [True, False])
def test_create_table_and_player_uses_supported_rules_and_vig_policy(
    ruleset: Ruleset,
    rules_type: type[ClassicRules] | type[CraplessRules],
    vig_paid_on_win: bool,
) -> None:
    engine_defaults = deepcopy(Table().settings)
    configuration = SessionConfiguration(
        ruleset=ruleset,
        starting_bankroll=STARTING_BANKROLL,
        vig_paid_on_win=vig_paid_on_win,
    )

    table, player = create_table_and_player(configuration)

    expected_settings = engine_defaults | {
        "vig_rounding": VIG_ROUNDING,
        "vig_paid_on_win": vig_paid_on_win,
    }
    assert isinstance(table.rules, rules_type)
    assert table.settings == expected_settings
    assert table.players == [player]
    assert player.table is table
    assert player.bankroll == STARTING_BANKROLL
    assert isinstance(player.strategy, NullStrategy)
    assert player.bets == []


def test_interactive_player_strategy_does_not_add_bets() -> None:
    table, player = create_table_and_player(
        SessionConfiguration(
            ruleset=Ruleset.CLASSIC,
            starting_bankroll=100.0,
        )
    )

    player.strategy.update_bets(player)

    assert player.bets == []
    assert len(table.players) == 1
