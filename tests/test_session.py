from __future__ import annotations

from dataclasses import FrozenInstanceError, fields
from datetime import UTC, datetime
from typing import get_args, get_origin, get_type_hints

import pytest

from bubblecraps.session import persistence
from bubblecraps.session.commands import CommandResult, CommandStatus
from bubblecraps.session.game_session import GameSession
from bubblecraps.session.history import RollRecord, SessionHistoryState, ShooterRecord
from bubblecraps.session.settings import VIG_ROUNDING, Ruleset, SessionConfiguration
from bubblecraps.session.snapshot import SessionSnapshot
from bubblecraps.session.state import AvailableActions, BetState, GamePhase, GameState
from bubblecraps.session.statistics import SessionStatisticsState


def test_session_configuration_is_minimal_and_immutable() -> None:
    configuration = SessionConfiguration(
        ruleset=Ruleset.CLASSIC,
        starting_bankroll=100.0,
    )

    assert [field.name for field in fields(configuration)] == [
        "ruleset",
        "starting_bankroll",
        "vig_paid_on_win",
    ]
    assert get_type_hints(SessionConfiguration)["starting_bankroll"] is float
    assert get_type_hints(SessionConfiguration)["ruleset"] is Ruleset
    assert configuration.ruleset is Ruleset.CLASSIC
    assert configuration.vig_paid_on_win is True
    assert VIG_ROUNDING == "none"

    pay_upfront = SessionConfiguration(
        ruleset=Ruleset.CRAPLESS,
        starting_bankroll=200.0,
        vig_paid_on_win=False,
    )
    assert pay_upfront.vig_paid_on_win is False

    with pytest.raises(FrozenInstanceError):
        configuration.ruleset = Ruleset.CRAPLESS  # type: ignore[misc]


def test_ruleset_parses_supported_identifiers_and_rejects_unknown_values() -> None:
    assert Ruleset("classic") is Ruleset.CLASSIC
    assert Ruleset("crapless") is Ruleset.CRAPLESS

    with pytest.raises(ValueError):
        Ruleset("easy")

    with pytest.raises(TypeError, match="ruleset must be a Ruleset"):
        SessionConfiguration(
            ruleset="classic",  # type: ignore[arg-type]
            starting_bankroll=100.0,
        )


def test_command_result_is_generic_and_immutable() -> None:
    result = CommandResult(CommandStatus.ACCEPTED)

    assert [status.value for status in CommandStatus] == [
        "accepted",
        "rejected",
        "not_implemented",
    ]
    assert result.status is CommandStatus.ACCEPTED

    with pytest.raises(FrozenInstanceError):
        result.status = CommandStatus.REJECTED  # type: ignore[misc]


def test_history_money_contract_uses_immutable_float_values() -> None:
    roll = RollRecord(
        die1=3,
        die2=4,
        total=7,
        timestamp=datetime(2026, 8, 26, tzinfo=UTC),
        shooter_number=1,
        point_before=6,
        point_after=None,
        total_player_cash_delta=-10.0,
    )
    shooter = ShooterRecord(
        shooter_number=1,
        rolls=3,
        point_numbers_made=(6,),
        profit=-10.0,
    )

    assert "bet_changes" not in {field.name for field in fields(roll)}
    assert get_type_hints(RollRecord)["total_player_cash_delta"] is float
    assert get_type_hints(ShooterRecord)["profit"] is float
    assert shooter.point_numbers_made == (6,)


def test_game_state_bankroll_contract_uses_float() -> None:
    assert get_type_hints(GameState)["bankroll"] is float


def test_available_actions_exposes_complete_command_set() -> None:
    assert [field.name for field in fields(AvailableActions)] == [
        "can_roll",
        "can_place_bets",
        "can_remove_bets",
        "can_repeat_last_bet",
        "can_double_bets",
        "can_clear_bets",
        "can_set_bets_on_or_off",
        "can_undo",
        "can_save",
        "can_load",
    ]


def test_initial_game_state_is_detached_and_immutable() -> None:
    actions = AvailableActions(
        can_roll=False,
        can_place_bets=True,
        can_remove_bets=False,
        can_repeat_last_bet=False,
        can_double_bets=False,
        can_clear_bets=False,
        can_set_bets_on_or_off=False,
        can_undo=False,
        can_save=False,
        can_load=False,
    )
    state = GameState(
        phase=GamePhase.READY,
        actions=actions,
        bankroll=100.0,
        point=None,
        puck_on=False,
        bets=(),
        die1=None,
        die2=None,
        last_roll=None,
        statistics=SessionStatisticsState(),
        history=SessionHistoryState(),
    )

    assert state == GameState(
        phase=GamePhase.READY,
        actions=actions,
        bankroll=100.0,
        point=None,
        puck_on=False,
        bets=(),
        die1=None,
        die2=None,
        last_roll=None,
        statistics=SessionStatisticsState(),
        history=SessionHistoryState(),
    )
    assert state.bets == ()
    assert state.history.rolls == ()
    assert state.history.shooters == ()
    assert state.history.events == ()
    assert state.statistics == SessionStatisticsState()

    with pytest.raises(FrozenInstanceError):
        state.bankroll = 200.0  # type: ignore[misc]


def test_published_state_uses_only_detached_immutable_types() -> None:
    bet = BetState(
        bet_id="bet-1",
        bet_type="place",
        amount=12.0,
        number=6,
    )
    history = SessionHistoryState()
    statistics = SessionStatisticsState()

    assert bet == BetState("bet-1", "place", 12.0, 6)
    assert get_type_hints(GameState)["bets"] == tuple[BetState, ...]
    assert get_type_hints(GameState)["history"] is SessionHistoryState
    assert get_type_hints(GameState)["statistics"] is SessionStatisticsState

    for value in (bet, history, statistics):
        with pytest.raises(FrozenInstanceError):
            value.__setattr__(fields(value)[0].name, None)

    for annotation in get_type_hints(GameState).values():
        assert get_origin(annotation) not in {list, dict, set}
        assert all(
            get_origin(argument) not in {list, dict, set}
            for argument in get_args(annotation)
        )
        assert "crapssim" not in repr(annotation)


def test_deferred_commands_return_not_implemented() -> None:
    session = object.__new__(GameSession)

    assert get_type_hints(GameSession)["undo_stack"] == list[SessionSnapshot]
    assert not hasattr(session, "undo_stack")
    assert session.undo().status is CommandStatus.NOT_IMPLEMENTED
    assert (
        session.set_bets_on_or_off(working=False).status
        is CommandStatus.NOT_IMPLEMENTED
    )
    assert session.save("session.bcs").status is CommandStatus.NOT_IMPLEMENTED
    assert GameSession.load("session.bcs").status is CommandStatus.NOT_IMPLEMENTED


def test_supported_command_shells_remain_deferred_to_later_work_packages() -> None:
    session = object.__new__(GameSession)

    for command in (
        session.roll,
        session.place_bet,
        session.remove_bet,
        session.repeat_last_bet,
        session.double_bet,
        session.clear_all_bets,
        session.new_session,
    ):
        with pytest.raises(NotImplementedError):
            command()


def test_persistence_placeholder_remains_importable() -> None:
    assert persistence.__doc__ is not None
