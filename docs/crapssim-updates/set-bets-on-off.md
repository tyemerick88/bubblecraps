# Crapssim Update: Set Bets On/Off

- Status: Required for Bubble Craps Milestone 6
- Target project: `crapssim`
- Current unsupported baseline: published `crapssim==0.4.1`
- Consumer: Bubble Craps
- Product requirement: Interblock game description, Section 3.2
- Bubble Craps roadmap owner: Milestone 6

## Purpose

Bubble Craps must reproduce the Interblock Set Bets On/Off behavior without implementing bet
settlement or working-state rules in the application. This requires a published `crapssim` release
that owns the complete behavior and exposes a public integration contract.

Bubble Craps Milestone 2 returns `NOT_IMPLEMENTED` for `set_bets_on_or_off`. Milestone 5 may render
the control as unavailable. Milestone 6 may enable it only after consuming and testing the published
engine capability described here.

## Authoritative Behavior

Section 3.2 of the Interblock game description requires Set Bets Off to disable these active bets for
the next roll:

- Place.
- Lay.
- Buy.
- Odds.
- Hard Ways: 2-2, 3-3, 4-4, and 5-5.

An off bet remains wagered but the next dice outcome does not resolve it. The documented lifecycle
also requires:

- Off bets are excluded from Clear Last Bet, Double Bet, and Repeat Last Bet.
- An off bet may still be increased, reduced, or removed directly.
- A player may set active or newly placed eligible bets off before the next roll.
- Lay bets become on after a point is reestablished or a 7 is rolled.
- Odds bets are removed when a point is reestablished.
- Other eligible bets remain off until explicitly turned on or another documented transition applies.
- Place and Buy bets are automatically off after a seven-out and require Set Bets On to reactivate.
- Off wagers continue to reduce playable credit and count as money committed to the table.
- Starting a roll may still require enough active wagers under the configured game conditions.
- A manual marker-puck transition to off sets eligible bets off when the corresponding game setting
  is enabled.

The source document is
[`docs/.intrablock/Craps_Crapless_Craps_Easy_Craps_game_description_Washington-specific_v2.5.1_0.pdf`](../.intrablock/Craps_Crapless_Craps_Easy_Craps_game_description_Washington-specific_v2.5.1_0.pdf).

## Current Engine Gap

Published `crapssim==0.4.1` cannot represent the complete requirement.

- `Place`, `Buy`, `Lay`, `Put`, and `Odds` expose `always_working`.
- `always_working` controls come-out behavior; it does not suppress settlement during point-on rolls.
- `HardWay` has no public working-state capability.
- `Put` exposes the override but is not part of the Section 3.2 affected-bet list.
- `TableUpdate.run` settles every active bet through `Player.update_bet` and offers no public way to
  skip settlement for an off bet.
- No public operation owns the automatic Lay, Odds, Place, Buy, point, or seven-out transitions.
- No public capability reports whether the complete Interblock behavior is available.

Bubble Craps must not approximate the feature by setting `always_working`, temporarily removing bets
from `Player.bets`, monkeypatching settlement, subclassing engine bets, or reproducing the engine
update sequence.

## Required Engine Changes

### Per-Bet Working State

Add engine-owned working state for every Section 3.2 eligible bet:

- `Place`.
- `Lay`.
- `Buy`.
- `Odds`.
- `HardWay`.

The state must distinguish whether an active wager participates in the next roll. It must not be
limited to point-off or come-out behavior.

The engine should preserve backward compatibility for existing simulation callers. Existing
`always_working` behavior may be retained, migrated, or deprecated, but its interaction with the new
state must be explicit and tested.

### Public Player Or Table Operation

Expose a public operation that applies the requested on/off state to all eligible active bets for one
player. Bubble Craps must not discover eligibility with reflection or maintain its own affected-bet
list.

The operation should:

- Accept the player and requested state, or be an instance method on an appropriate engine owner.
- Update all currently eligible active bets.
- Leave ineligible bets unchanged.
- Return a structured result or another observable public outcome identifying whether the command
  changed state.
- Behave idempotently when every eligible bet already has the requested state.
- Define behavior when no eligible bets are present.
- Support newly placed eligible bets being set off by a repeated Set Bets Off command.

The final API shape belongs to `crapssim`; Bubble Craps requires stable public behavior rather than a
specific method name.

### Settlement Suppression

The normal engine roll lifecycle must skip resolution for off bets. This includes both winning and
losing outcomes while the point is on or off.

Settlement suppression must occur inside the engine-owned update path so that:

- Wagers remain attached to the player.
- Bankroll and total committed cash remain correct.
- No payout, loss, push, movement, or removal occurs because of the skipped roll.
- Other active bets resolve normally.
- Dice, point, shooter, and table statistics continue to advance normally.

### Automatic Transitions

Implement the Section 3.2 transitions in the engine lifecycle:

- Turn Lay bets on after a point is reestablished or a 7 is rolled.
- Remove Odds bets when a point is reestablished as required by the Interblock behavior.
- Keep other eligible off bets off unless explicitly reactivated or covered by another documented
  transition.
- Set Place and Buy bets off after a seven-out.
- Apply marker-puck-driven deactivation when the relevant engine setting is enabled.

Transition timing must be defined relative to bet settlement, point updates, and shooter changes so
consumers do not have to infer or reproduce it.

### Command Interaction

Expose enough public behavior for consumers to enforce these command rules without duplicating bet
eligibility:

- Clear Last Bet ignores off bets.
- Double Bet ignores off bets.
- Repeat Last Bet ignores off bets.
- Direct increase, reduction, and removal remain available for off bets when otherwise legal.

If these convenience commands become engine operations, they should implement the exclusions
directly. If they remain consumer-orchestrated, the engine must expose a stable public way to query
whether a bet is eligible and currently on or off.

### Projection And Capability Contract

Expose public read-only information sufficient for Bubble Craps to create detached state:

- Whether an active bet participates in the next roll.
- Whether the bet supports Set Bets On/Off.
- A capability or version signal indicating that complete Section 3.2 behavior is available.

The capability must represent the complete contract, not only the presence of an `always_working`
attribute.

## Engine Test Requirements

Add focused tests covering at least:

- Each eligible bet can be turned off and on.
- Ineligible bets are unchanged.
- A point-on winning roll does not resolve an off Place, Buy, Lay, Odds, or Hard Way bet.
- A point-on losing roll does not resolve each off eligible bet.
- Point-off behavior remains correct for on and off bets.
- Mixed on and off bets settle independently on the same roll.
- Off wagers remain included in committed cash without changing bankroll during a skipped result.
- Newly placed eligible bets can be included by a repeated Set Bets Off command.
- Lay reactivation after point establishment and 7.
- Odds removal after point establishment.
- Place and Buy automatic deactivation after seven-out.
- Other eligible bets remain off across rolls as documented.
- Clear Last, Double, and Repeat ignore off bets.
- Direct increase, reduction, and removal of off bets follow normal engine legality.
- Idempotent on/off requests have defined results.
- No-eligible-bet requests have defined results.
- Classic and Crapless rulesets produce the documented transitions.
- Existing simulation behavior remains backward compatible unless a release note explicitly records
  an approved breaking change.

Use deterministic dice outcomes and drive settlement through the normal public table-update path.

## Published Release Requirements

Before Bubble Craps integration begins:

- The engine change is reviewed and merged in the `crapssim` project.
- The complete behavior has public documentation and engine tests.
- A new `crapssim` version is published through the normal release channel.
- Bubble Craps installs the release as an exact version, not from a local path, branch, commit, or VCS
  URL.
- Bubble Craps runtime contract tests prove the installed distribution exposes the required public
  operation, projection fields, capability signal, and deterministic behavior.

The exact target version remains unset until the engine project publishes the capability.

## Bubble Craps Milestone 6 Integration

After the published release is available, Milestone 6 will:

- Update the exact `crapssim` dependency pin.
- Implement `GameSession.set_bets_on_or_off` through the public engine operation.
- Add detached per-bet working state to the session projection.
- Compute the corresponding available action from engine-owned capability and state.
- Record accepted on/off commands in session history without recalculating eligibility.
- Include working state in snapshots, undo, save/load, and roundtrip validation.
- Add SessionController forwarding and successful-mutation signals.
- Enable the GUI control only when the installed engine exposes the complete capability.
- Verify Clear Last, Double, Repeat, direct adjustment, and roll behavior end to end.
- Add compliance evidence for all Section 3.2 scenarios.

## Acceptance Gate

This update is ready for Bubble Craps only when all of the following are true:

- A published engine release implements the complete Section 3.2 affected-bet set and lifecycle.
- Off bets are demonstrably skipped by the normal settlement path during point-on and point-off rolls.
- Hard Ways participates in the same public working-state contract.
- Automatic Lay, Odds, Place, Buy, point, and seven-out transitions are engine-owned and tested.
- Consumers can project state and invoke the command without private members, reflection, copied
  eligibility lists, or settlement workarounds.
- Existing engine tests and Bubble Craps runtime contract tests pass against the published package.

Until this gate passes, Bubble Craps must keep `set_bets_on_or_off` unavailable and return
`NOT_IMPLEMENTED`.