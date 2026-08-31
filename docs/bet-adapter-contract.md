# Bet Adapter Contract

- Status: Accepted for Milestone 2 WP2.4
- Engine baseline: exact published `crapssim==0.4.1`
- Product source: Interblock game description version 2.5.1

## Purpose

The session bet adapter translates stable Bubble Craps requests into public `crapssim` bet
constructors and translates supported live bets into detached `BetState` values. It does not settle
bets, calculate payouts or bankroll effects, inspect private engine placement keys, or call
`Bet.get_result`.

## Request Contract

`BetRequest` is immutable and contains:

- `bet_type: BetType`.
- `amount: float`.
- `number: int | None` for numbered and Odds bets.
- `hop_result: tuple[int, int] | None` for Hop bets.

The adapter validates request shape, finite positive amounts, and physical dice faces. Engine
constructors and `Player.add_bet` remain responsible for number, amount, timing, parent-bet,
bankroll, and other game legality.

## Projection Contract

`BetState` is immutable and contains:

- `bet_id`: application-owned identity supplied by the session.
- `bet_type`: an approved Bubble Craps `BetType` identifier.
- `amount`: the public engine wager amount.
- `number`: the public target or moved number when applicable.
- `hop_result`: the public Hop dice result when applicable.
- `rolled_numbers`: the sorted immutable Lucky Roller progress when applicable.

The projection contains no live engine object and does not expose payout, winning-number,
losing-number, removability, settlement, or private placement-key behavior.

## Approved Bindings

| `BetType` value | Engine constructor | Required request fields | Classic | Crapless |
| --- | --- | --- | --- | --- |
| `pass_line` | `PassLine(amount)` | amount | yes | yes |
| `dont_pass` | `DontPass(amount)` | amount | yes | no |
| `come` | `Come(amount)` | amount | yes | yes |
| `dont_come` | `DontCome(amount)` | amount | yes | no |
| `pass_line_odds` | `Odds(PassLine, number, amount)` | amount, number | yes | yes |
| `dont_pass_odds` | `Odds(DontPass, number, amount)` | amount, number | yes | no |
| `come_odds` | `Odds(Come, number, amount)` | amount, number | yes | yes |
| `dont_come_odds` | `Odds(DontCome, number, amount)` | amount, number | yes | no |
| `place` | `Place(number, amount)` | amount, number | yes | yes |
| `buy` | `Buy(number, amount)` | amount, number | yes | yes |
| `lay` | `Lay(number, amount)` | amount, number | yes | no |
| `field` | `Field(amount)` | amount | yes | yes |
| `c_and_e` | `CAndE(amount)` | amount | yes | yes |
| `any_seven` | `Any7(amount)` | amount | yes | yes |
| `two` | `Two(amount)` | amount | yes | yes |
| `three` | `Three(amount)` | amount | yes | yes |
| `eleven` | `Yo(amount)` | amount | yes | yes |
| `twelve` | `Boxcars(amount)` | amount | yes | yes |
| `any_craps` | `AnyCraps(amount)` | amount | yes | yes |
| `horn` | `Horn(amount)` | amount | yes | yes |
| `big_six` | `Big6(amount)` | amount | yes | no |
| `big_eight` | `Big8(amount)` | amount | yes | no |
| `hard_way` | `HardWay(number, amount)` | amount, number | yes | yes |
| `hop` | `Hop(hop_result, amount)` | amount, hop result | yes | yes |
| `low_rolls` | `Small(amount)` | amount | yes | yes |
| `roll_em_all` | `All(amount)` | amount | yes | yes |
| `high_rolls` | `Tall(amount)` | amount | yes | yes |

The engine ATS names map directly to Interblock Lucky Roller: `Small` tracks Low Rolls, `Tall`
tracks High Rolls, and `All` tracks Roll 'Em All. Their public `rolled_numbers` set is projected as a
sorted tuple. Payout values remain engine-owned table settings.

## Variant Availability Exception

The adapter owns only the fixed product-surface availability shown above. This is a deliberate,
reviewed exception because `crapssim==0.4.1` incorrectly permits Lay, Big 6, and Big 8 in Crapless
Craps. The same filter consistently covers the documented Don't-side bets.

This exception does not authorize Bubble Craps to reproduce other legality. Once a request passes
the product-surface filter, the engine remains authoritative for whether `Player.add_bet` accepts it.

## Excluded Engine Bets

The following public engine classes are not approved Milestone 2 bindings:

- `Put`: not part of the Interblock product surface used by Bubble Craps.
- `World`: not named by the Interblock document.
- `Fire`: not equivalent to the documented Lucky Shooter behavior.

Application-known request-shape, product-availability, and projection failures raise
`BetAdapterError` with a specific explanatory message. Engine command rejection remains generic:
the adapter does not invent amount, timing, bankroll, parent-bet, removability, or settlement reasons
when `Player.add_bet` makes no observable change.