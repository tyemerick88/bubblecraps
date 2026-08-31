"""Translate between Bubble Craps bet values and public engine bets."""

from __future__ import annotations

import math
from dataclasses import dataclass

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
    HardWay,
    Hop,
    Horn,
    Lay,
    Odds,
    PassLine,
    Place,
    Small,
    Tall,
    Three,
    Two,
    Yo,
)

from bubblecraps.session.settings import Ruleset
from bubblecraps.session.state import BetState, BetType

HOP_RESULT_LENGTH = 2
MIN_DIE_FACE = 1
MAX_DIE_FACE = 6


class BetAdapterError(ValueError):
    """Report an invalid adapter request or unsupported projection."""


@dataclass(frozen=True, slots=True)
class BetRequest:
    """Describe a request to construct one supported engine bet."""

    bet_type: BetType
    amount: float
    number: int | None = None
    hop_result: tuple[int, int] | None = None

    def __post_init__(self) -> None:
        """Validate request shape without reproducing engine legality rules."""
        if not isinstance(self.bet_type, BetType):
            raise BetAdapterError("bet_type must be a BetType")
        if not isinstance(self.amount, float):
            raise BetAdapterError("amount must be a float")
        if not math.isfinite(self.amount):
            raise BetAdapterError("amount must be finite")
        if self.amount <= 0:
            raise BetAdapterError("amount must be positive")
        if self.number is not None and (
            not isinstance(self.number, int) or isinstance(self.number, bool)
        ):
            raise BetAdapterError("number must be an int when provided")
        if self.hop_result is not None and not _valid_hop_result(self.hop_result):
            raise BetAdapterError(
                "hop_result must contain two integer dice values from 1 through 6"
            )


_SIMPLE_CONSTRUCTORS: dict[BetType, type[Bet]] = {
    BetType.PASS_LINE: PassLine,
    BetType.DONT_PASS: DontPass,
    BetType.COME: Come,
    BetType.DONT_COME: DontCome,
    BetType.FIELD: Field,
    BetType.C_AND_E: CAndE,
    BetType.ANY_SEVEN: Any7,
    BetType.TWO: Two,
    BetType.THREE: Three,
    BetType.ELEVEN: Yo,
    BetType.TWELVE: Boxcars,
    BetType.ANY_CRAPS: AnyCraps,
    BetType.HORN: Horn,
    BetType.BIG_SIX: Big6,
    BetType.BIG_EIGHT: Big8,
    BetType.LOW_ROLLS: Small,
    BetType.ROLL_EM_ALL: All,
    BetType.HIGH_ROLLS: Tall,
}

_NUMBERED_CONSTRUCTORS: dict[BetType, type[Bet]] = {
    BetType.PLACE: Place,
    BetType.BUY: Buy,
    BetType.LAY: Lay,
    BetType.HARD_WAY: HardWay,
}

_ODDS_BASE_TYPES: dict[BetType, type[Bet]] = {
    BetType.PASS_LINE_ODDS: PassLine,
    BetType.DONT_PASS_ODDS: DontPass,
    BetType.COME_ODDS: Come,
    BetType.DONT_COME_ODDS: DontCome,
}

_CRAPLESS_UNSUPPORTED = {
    BetType.DONT_PASS,
    BetType.DONT_COME,
    BetType.DONT_PASS_ODDS,
    BetType.DONT_COME_ODDS,
    BetType.LAY,
    BetType.BIG_SIX,
    BetType.BIG_EIGHT,
}

_ENGINE_TYPES: dict[type[Bet], BetType] = {
    constructor: bet_type for bet_type, constructor in _SIMPLE_CONSTRUCTORS.items()
} | {constructor: bet_type for bet_type, constructor in _NUMBERED_CONSTRUCTORS.items()}

_NUMBERED_ENGINE_TYPES = (Come, DontCome, Place, Buy, Lay, HardWay, Big6, Big8)
_LUCKY_ROLLER_ENGINE_TYPES = (Small, All, Tall)


def create_bet(request: BetRequest, ruleset: Ruleset) -> Bet:
    """Construct a supported engine bet from an approved request."""
    if not isinstance(ruleset, Ruleset):
        raise BetAdapterError("ruleset must be a Ruleset")
    if ruleset is Ruleset.CRAPLESS and request.bet_type in _CRAPLESS_UNSUPPORTED:
        raise BetAdapterError(
            f"{request.bet_type.value} is not available for {ruleset.value}"
        )

    try:
        return _construct_bet(request)
    except BetAdapterError:
        raise
    except (KeyError, TypeError, ValueError) as error:
        raise BetAdapterError(
            f"Could not construct {request.bet_type.value} from request"
        ) from error


def _construct_bet(request: BetRequest) -> Bet:
    if request.bet_type in _SIMPLE_CONSTRUCTORS:
        _require_shape(request, number=False, hop_result=False)
        return _SIMPLE_CONSTRUCTORS[request.bet_type](request.amount)
    if request.bet_type in _NUMBERED_CONSTRUCTORS:
        _require_shape(request, number=True, hop_result=False)
        if request.number is None:
            raise BetAdapterError(f"{request.bet_type.value} requires number")
        return _NUMBERED_CONSTRUCTORS[request.bet_type](request.number, request.amount)
    if request.bet_type in _ODDS_BASE_TYPES:
        _require_shape(request, number=True, hop_result=False)
        if request.number is None:
            raise BetAdapterError(f"{request.bet_type.value} requires number")
        return Odds(
            _ODDS_BASE_TYPES[request.bet_type],
            request.number,
            request.amount,
        )
    if request.bet_type is BetType.HOP:
        _require_shape(request, number=False, hop_result=True)
        if request.hop_result is None:
            raise BetAdapterError("hop requires hop_result")
        return Hop(request.hop_result, request.amount)
    raise BetAdapterError(f"No constructor binding for {request.bet_type.value}")


def project_bet(bet_id: str, bet: Bet) -> BetState:
    """Create detached state from one supported engine bet."""
    if not bet_id:
        raise BetAdapterError("bet_id must not be empty")

    if type(bet) is Odds:
        bet_type = _project_odds_type(bet)
    elif type(bet) is Hop:
        bet_type = BetType.HOP
    else:
        try:
            bet_type = _ENGINE_TYPES[type(bet)]
        except KeyError as error:
            raise BetAdapterError(
                f"No projection binding for engine bet type {type(bet).__name__}"
            ) from error

    number = bet.number if isinstance(bet, (*_NUMBERED_ENGINE_TYPES, Odds)) else None
    hop_result = bet.result if type(bet) is Hop else None
    rolled_numbers = (
        tuple(sorted(bet.rolled_numbers))
        if isinstance(bet, _LUCKY_ROLLER_ENGINE_TYPES)
        else None
    )
    return BetState(
        bet_id=bet_id,
        bet_type=bet_type,
        amount=bet.amount,
        number=number,
        hop_result=hop_result,
        rolled_numbers=rolled_numbers,
    )


def _project_odds_type(bet: Odds) -> BetType:
    for bet_type, base_type in _ODDS_BASE_TYPES.items():
        if bet.base_type is base_type:
            return bet_type
    raise BetAdapterError(f"No Odds projection binding for base type {bet.base_type}")


def _require_shape(
    request: BetRequest,
    *,
    number: bool,
    hop_result: bool,
) -> None:
    if number and request.number is None:
        raise BetAdapterError(f"{request.bet_type.value} requires number")
    if not number and request.number is not None:
        raise BetAdapterError(f"{request.bet_type.value} does not accept number")
    if hop_result and request.hop_result is None:
        raise BetAdapterError(f"{request.bet_type.value} requires hop_result")
    if not hop_result and request.hop_result is not None:
        raise BetAdapterError(f"{request.bet_type.value} does not accept hop_result")


def _valid_hop_result(result: tuple[int, int]) -> bool:
    return (
        isinstance(result, tuple)
        and len(result) == HOP_RESULT_LENGTH
        and all(isinstance(die, int) and not isinstance(die, bool) for die in result)
        and all(MIN_DIE_FACE <= die <= MAX_DIE_FACE for die in result)
    )
