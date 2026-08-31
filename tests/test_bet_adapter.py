from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest
from crapssim.bet import (
    All,
    Any7,
    AnyCraps,
    Bet,
    Big6,
    Big8,
    Boxcars,
    Buy,
    CAndE,
    Come,
    DontCome,
    DontPass,
    Field,
    Fire,
    HardWay,
    Hop,
    Horn,
    Lay,
    Odds,
    PassLine,
    Place,
    Put,
    Small,
    Tall,
    Three,
    Two,
    World,
    Yo,
)
from crapssim.table import TableUpdate

from bubblecraps.session.bet_adapter import (
    BetAdapterError,
    BetRequest,
    create_bet,
    project_bet,
)
from bubblecraps.session.settings import (
    Ruleset,
    SessionConfiguration,
    create_table_and_player,
)
from bubblecraps.session.state import BetState, BetType

BET_AMOUNT = 5.0
COME_POINT = 9
DONT_COME_POINT = 5

SIMPLE_BINDINGS = [
    (BetType.PASS_LINE, PassLine, None),
    (BetType.DONT_PASS, DontPass, None),
    (BetType.COME, Come, None),
    (BetType.DONT_COME, DontCome, None),
    (BetType.FIELD, Field, None),
    (BetType.C_AND_E, CAndE, None),
    (BetType.ANY_SEVEN, Any7, None),
    (BetType.TWO, Two, None),
    (BetType.THREE, Three, None),
    (BetType.ELEVEN, Yo, None),
    (BetType.TWELVE, Boxcars, None),
    (BetType.ANY_CRAPS, AnyCraps, None),
    (BetType.HORN, Horn, None),
    (BetType.BIG_SIX, Big6, 6),
    (BetType.BIG_EIGHT, Big8, 8),
]

NUMBERED_BINDINGS = [
    (BetType.PLACE, Place, 6),
    (BetType.BUY, Buy, 4),
    (BetType.LAY, Lay, 10),
    (BetType.HARD_WAY, HardWay, 8),
]

ODDS_BINDINGS = [
    (BetType.PASS_LINE_ODDS, PassLine),
    (BetType.DONT_PASS_ODDS, DontPass),
    (BetType.COME_ODDS, Come),
    (BetType.DONT_COME_ODDS, DontCome),
]

LUCKY_ROLLER_BINDINGS = [
    (BetType.LOW_ROLLS, Small),
    (BetType.ROLL_EM_ALL, All),
    (BetType.HIGH_ROLLS, Tall),
]

LUCKY_ROLLER_SEQUENCES = [
    (
        BetType.LOW_ROLLS,
        ((3, 3), (1, 1), (2, 2), (1, 2), (2, 3)),
        (2, 3, 4, 5, 6),
        130.0,
    ),
    (
        BetType.HIGH_ROLLS,
        ((6, 6), (4, 4), (5, 5), (4, 5), (5, 6)),
        (8, 9, 10, 11, 12),
        130.0,
    ),
    (
        BetType.ROLL_EM_ALL,
        (
            (6, 6),
            (1, 1),
            (5, 6),
            (1, 2),
            (5, 5),
            (2, 2),
            (4, 5),
            (2, 3),
            (4, 4),
            (3, 3),
        ),
        (2, 3, 4, 5, 6, 8, 9, 10, 11, 12),
        250.0,
    ),
]


def _create_classic_bet(request: BetRequest) -> Bet:
    return create_bet(request, Ruleset.CLASSIC)


@pytest.mark.parametrize(
    ("bet_type", "engine_type", "projected_number"), SIMPLE_BINDINGS
)
def test_simple_bindings_construct_and_project(
    bet_type: BetType,
    engine_type: type[Bet],
    projected_number: int | None,
) -> None:
    bet = _create_classic_bet(BetRequest(bet_type=bet_type, amount=BET_AMOUNT))

    assert type(bet) is engine_type
    assert project_bet("bet-1", bet) == BetState(
        bet_id="bet-1",
        bet_type=bet_type,
        amount=BET_AMOUNT,
        number=projected_number,
    )


@pytest.mark.parametrize(("bet_type", "engine_type", "number"), NUMBERED_BINDINGS)
def test_numbered_bindings_construct_and_project(
    bet_type: BetType,
    engine_type: type[Bet],
    number: int,
) -> None:
    bet = _create_classic_bet(
        BetRequest(
            bet_type=bet_type,
            amount=BET_AMOUNT,
            number=number,
        )
    )

    assert type(bet) is engine_type
    assert project_bet("bet-1", bet) == BetState(
        bet_id="bet-1",
        bet_type=bet_type,
        amount=BET_AMOUNT,
        number=number,
    )


@pytest.mark.parametrize(("bet_type", "base_type"), ODDS_BINDINGS)
def test_odds_bindings_preserve_parent_type(
    bet_type: BetType,
    base_type: type[Bet],
) -> None:
    bet = _create_classic_bet(
        BetRequest(
            bet_type=bet_type,
            amount=BET_AMOUNT,
            number=6,
        )
    )

    assert type(bet) is Odds
    assert bet.base_type is base_type
    assert project_bet("bet-1", bet) == BetState(
        bet_id="bet-1",
        bet_type=bet_type,
        amount=BET_AMOUNT,
        number=6,
    )


def test_hop_binding_normalizes_and_projects_dice_result() -> None:
    bet = _create_classic_bet(
        BetRequest(
            bet_type=BetType.HOP,
            amount=BET_AMOUNT,
            hop_result=(3, 2),
        )
    )

    assert type(bet) is Hop
    assert project_bet("bet-1", bet) == BetState(
        bet_id="bet-1",
        bet_type=BetType.HOP,
        amount=BET_AMOUNT,
        hop_result=(2, 3),
    )


@pytest.mark.parametrize(("bet_type", "engine_type"), LUCKY_ROLLER_BINDINGS)
@pytest.mark.parametrize("ruleset", [Ruleset.CLASSIC, Ruleset.CRAPLESS])
def test_lucky_roller_bindings_construct_and_project_progress(
    bet_type: BetType,
    engine_type: type[Bet],
    ruleset: Ruleset,
) -> None:
    bet = create_bet(BetRequest(bet_type=bet_type, amount=BET_AMOUNT), ruleset)

    assert type(bet) is engine_type
    assert project_bet("bet-1", bet) == BetState(
        bet_id="bet-1",
        bet_type=bet_type,
        amount=BET_AMOUNT,
        rolled_numbers=(),
    )

    assert isinstance(bet, (Small, All, Tall))
    bet.rolled_numbers.update({8, 2, 5})

    assert project_bet("bet-1", bet).rolled_numbers == (2, 5, 8)


@pytest.mark.parametrize(
    ("bet_type", "dice_outcomes", "expected_numbers", "expected_bankroll"),
    LUCKY_ROLLER_SEQUENCES,
)
def test_lucky_roller_bindings_follow_full_engine_lifecycle(
    bet_type: BetType,
    dice_outcomes: tuple[tuple[int, int], ...],
    expected_numbers: tuple[int, ...],
    expected_bankroll: float,
) -> None:
    table, player = create_table_and_player(
        SessionConfiguration(
            ruleset=Ruleset.CLASSIC,
            starting_bankroll=100.0,
        )
    )
    bet = create_bet(BetRequest(bet_type=bet_type, amount=1.0), Ruleset.CLASSIC)
    player.add_bet(bet)

    for dice_outcome in dice_outcomes:
        TableUpdate().run(table, dice_outcome=dice_outcome)

    assert bet not in player.bets
    assert player.bankroll == expected_bankroll
    assert project_bet("bet-1", bet).rolled_numbers == expected_numbers


def test_moving_bets_project_their_public_number() -> None:
    assert (
        project_bet("come-1", Come(BET_AMOUNT, number=COME_POINT)).number == COME_POINT
    )
    assert (
        project_bet("dont-come-1", DontCome(BET_AMOUNT, number=DONT_COME_POINT)).number
        == DONT_COME_POINT
    )


@pytest.mark.parametrize(
    ("amount", "message"),
    [
        (0.0, "amount must be positive"),
        (-1.0, "amount must be positive"),
        (float("inf"), "amount must be finite"),
        (float("nan"), "amount must be finite"),
    ],
)
def test_bet_request_rejects_invalid_amount(amount: float, message: str) -> None:
    with pytest.raises(BetAdapterError, match=message):
        BetRequest(bet_type=BetType.FIELD, amount=amount)


def test_bet_request_rejects_unparsed_type() -> None:
    with pytest.raises(BetAdapterError, match="bet_type must be a BetType"):
        BetRequest(
            bet_type="field",  # type: ignore[arg-type]
            amount=BET_AMOUNT,
        )


def test_bet_request_requires_float_amount() -> None:
    with pytest.raises(BetAdapterError, match="amount must be a float"):
        BetRequest(
            bet_type=BetType.FIELD,
            amount=5,
        )


def test_bet_request_requires_integer_number() -> None:
    with pytest.raises(BetAdapterError, match="number must be an int when provided"):
        BetRequest(
            bet_type=BetType.PLACE,
            amount=BET_AMOUNT,
            number=True,
        )


@pytest.mark.parametrize(
    ("bet_request", "message"),
    [
        (
            BetRequest(bet_type=BetType.FIELD, amount=BET_AMOUNT, number=6),
            "field does not accept number",
        ),
        (
            BetRequest(bet_type=BetType.PLACE, amount=BET_AMOUNT),
            "place requires number",
        ),
        (
            BetRequest(bet_type=BetType.HOP, amount=BET_AMOUNT),
            "hop requires hop_result",
        ),
    ],
)
def test_create_bet_rejects_malformed_constructor_shape(
    bet_request: BetRequest,
    message: str,
) -> None:
    with pytest.raises(BetAdapterError, match=message):
        _create_classic_bet(bet_request)


def test_create_bet_rejects_unexpected_hop_result() -> None:
    request = BetRequest(
        bet_type=BetType.FIELD,
        amount=BET_AMOUNT,
        hop_result=(2, 3),
    )

    with pytest.raises(BetAdapterError, match="field does not accept hop_result"):
        _create_classic_bet(request)


def test_create_bet_explains_engine_constructor_failure() -> None:
    request = BetRequest(
        bet_type=BetType.HARD_WAY,
        amount=BET_AMOUNT,
        number=5,
    )

    with pytest.raises(
        BetAdapterError,
        match="Could not construct hard_way from request",
    ):
        _create_classic_bet(request)


@pytest.mark.parametrize("hop_result", [(0, 1), (1, 7), (True, 2)])
def test_bet_request_rejects_invalid_hop_dice(
    hop_result: tuple[int, int],
) -> None:
    with pytest.raises(
        BetAdapterError,
        match="hop_result must contain two integer dice values from 1 through 6",
    ):
        BetRequest(
            bet_type=BetType.HOP,
            amount=BET_AMOUNT,
            hop_result=hop_result,
        )


@pytest.mark.parametrize(
    "bet",
    [
        Put(6, BET_AMOUNT),
        World(BET_AMOUNT),
        Fire(BET_AMOUNT),
    ],
)
def test_project_bet_rejects_engine_bets_outside_approved_subset(bet: Bet) -> None:
    with pytest.raises(
        BetAdapterError,
        match=f"No projection binding for engine bet type {type(bet).__name__}",
    ):
        project_bet("bet-1", bet)


def test_project_bet_rejects_unapproved_put_odds() -> None:
    with pytest.raises(
        BetAdapterError,
        match="No Odds projection binding for base type Put",
    ):
        project_bet("bet-1", Odds(Put, 6, BET_AMOUNT))


def test_project_bet_requires_application_identity() -> None:
    with pytest.raises(BetAdapterError, match="bet_id must not be empty"):
        project_bet("", Field(BET_AMOUNT))


def test_bet_values_are_immutable() -> None:
    request = BetRequest(bet_type=BetType.FIELD, amount=BET_AMOUNT)
    state = project_bet("bet-1", _create_classic_bet(request))

    with pytest.raises(FrozenInstanceError):
        request.amount = 10.0  # type: ignore[misc]
    with pytest.raises(FrozenInstanceError):
        state.amount = 10.0  # type: ignore[misc]


def test_bet_state_rejects_unparsed_type() -> None:
    with pytest.raises(TypeError, match="bet_type must be a BetType"):
        BetState(
            bet_id="bet-1",
            bet_type="field",  # type: ignore[arg-type]
            amount=BET_AMOUNT,
        )


@pytest.mark.parametrize(
    "bet_type",
    [
        BetType.DONT_PASS,
        BetType.DONT_COME,
        BetType.DONT_PASS_ODDS,
        BetType.DONT_COME_ODDS,
        BetType.LAY,
        BetType.BIG_SIX,
        BetType.BIG_EIGHT,
    ],
)
def test_adapter_rejects_bets_unavailable_in_crapless(bet_type: BetType) -> None:
    number = (
        4
        if bet_type
        in {
            BetType.DONT_PASS_ODDS,
            BetType.DONT_COME_ODDS,
            BetType.LAY,
        }
        else None
    )

    with pytest.raises(
        BetAdapterError,
        match=f"{bet_type.value} is not available for crapless",
    ):
        create_bet(
            BetRequest(bet_type=bet_type, amount=BET_AMOUNT, number=number),
            Ruleset.CRAPLESS,
        )


def test_adapter_constructs_supported_crapless_bet() -> None:
    bet = create_bet(
        BetRequest(bet_type=BetType.PLACE, amount=BET_AMOUNT, number=6),
        Ruleset.CRAPLESS,
    )

    assert type(bet) is Place


def test_adapter_requires_parsed_ruleset() -> None:
    with pytest.raises(BetAdapterError, match="ruleset must be a Ruleset"):
        create_bet(
            BetRequest(bet_type=BetType.FIELD, amount=BET_AMOUNT),
            "classic",  # type: ignore[arg-type]
        )


def test_classic_adapter_constructs_dont_pass() -> None:
    bet = _create_classic_bet(BetRequest(bet_type=BetType.DONT_PASS, amount=BET_AMOUNT))

    assert type(bet) is DontPass
