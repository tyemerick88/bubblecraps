# Milestone 2: Domain Core Completion

- Status: Implementation in progress; WP2.1 complete
- Roadmap source: [docs/roadmap.md](../roadmap.md)
- Primary architecture reference: [docs/PAG-mini-v0.6.md](../PAG-mini-v0.6.md)
- Supporting design reference: [docs/PAG-v0.6.md](../PAG-v0.6.md)
- Depends on: [Milestone 1](milestone-1-architecture-skeleton.md)
- Engine baseline: exact published `crapssim==0.4.1`

## Milestone Intent

Milestone 2 turns the pure-Python session skeleton from Milestone 1 into a tested domain core while
remaining within the public behavior of the published `crapssim==0.4.1` package. It implements
session construction, detached state, aggregate history, statistics, supported player commands, and
single-roll orchestration. `crapssim` remains the sole authority for rules, bet legality, dice
resolution, point transitions, payouts, and bankroll effects.

The milestone ends with a deterministic, headless game session that can be exercised entirely from
Python. It does not require a `crapssim` source change, an unreleased sibling-checkout API, private
engine members, persistence, undo, Qt controller behavior, or GUI rendering.

## Completed Foundation

Milestone 0 established the dependency direction, engine ownership policy, quality baselines, and
exact published `crapssim==0.4.1` dependency. Milestone 1 established the runtime package skeleton,
session signatures, controller and GUI shells, infrastructure placeholders, and automated boundary
checks. Milestone 2 must preserve those boundaries and keep the architecture tests passing.

## Engine Compatibility Contract

Milestone 2 targets the installed, published `crapssim==0.4.1` API as it exists:

- No Milestone 2 task modifies `crapssim` or depends on an uncommitted sibling checkout.
- Integration uses public classes, constructors, methods, and attributes only.
- Bubble Craps does not inspect private placement keys or other underscore-prefixed engine members.
- Bubble Craps does not use reflection, monkeypatching, engine subclassing, or copied engine rules to
  fill API gaps.
- Tables use engine defaults except for two reviewed Bubble Craps vig policies:
  `vig_rounding="none"` and the session's `vig_paid_on_win` value. Arbitrary `Table.settings`
  overrides and a casino-profile abstraction remain deferred.
- `Player.add_bet` and `Player.remove_bet` silently accept or reject attempts and return `None`.
  Bubble Craps may observe whether public state changed, but it must not invent a specific engine
  rejection reason.
- `TableUpdate.run` mutates the table but does not publish an authoritative per-bet settlement
  journal. Bubble Craps records aggregate roll observations and must not infer that a changed or
  missing bet won, lost, pushed, moved, or was otherwise resolved.
- Expected rejections must leave observed domain state unchanged. Milestone 2 does not promise
  transactional rollback after an unexpected engine exception.
- Missing safe public support produces a stable `NOT_IMPLEMENTED` domain result; it is not a reason
  to reach into private engine behavior or duplicate rules.

## What Will Be Accomplished

- A constructible `GameSession` owning one `crapssim.Table` and one `crapssim.Player`.
- Explicit Classic or Crapless ruleset selection with fixed unrounded vig and configurable
  pay-on-win commission behavior.
- A strategy-neutral interactive player using `crapssim.strategy.tools.NullStrategy`.
- A reviewed adapter for a deliberately limited set of bet requests and detached projections.
- Deterministic and random single-roll orchestration through `crapssim.TableUpdate`.
- Recursively immutable GUI-facing state and conservative available actions.
- Aggregate roll, shooter, event, and player-command history.
- Cumulative session statistics derived from observed engine transitions.
- Best-effort supported bet commands and stable generic command outcomes.
- Domain tests for supported commands, expected rejection, transitions, aggregate history,
  statistics, rulesets, and deterministic roll sequences.

## Architecture Invariants

- `src/bubblecraps/session/` contains no PySide6, controller, GUI, application, or asset imports.
- `GameSession` is the only Bubble Craps runtime class that mutates live `crapssim` objects.
- Bubble Craps does not reproduce winning numbers, losing numbers, payout ratios, point rules, bet
  legality, removability, working behavior, or bankroll calculations.
- `GameState` and `AvailableActions` are produced by `GameSession`; callers do not infer legality.
- Published domain values contain no live engine objects or mutable session containers.
- Domain tests use explicit dice outcomes or seeds and do not depend on uncontrolled randomness.
- No controller signal or GUI behavior is evidence of a domain transition.
- Persistence, logging, and application configuration remain separate from gameplay history.

## Resolved Domain Decisions

### Money

- Use finite `float` values for bankroll, wagers, cash deltas, shooter profit, and session profit.
- Reject non-finite values and require a positive starting bankroll and positive wager amount.
- Do not truncate engine values with `int(...)`.
- Use exact assertions where practical and `pytest.approx` at floating-point integration boundaries.

### Immutable Published State

- `GameState` is a recursively immutable, detached projection rather than a view of live session or
  engine containers.
- Published collections use tuples and published mappings use an immutable representation.
- Bet projections contain only reviewed public descriptive fields; they do not expose `Bet`
  instances or claim rule authority.
- History and statistics in state are immutable snapshots, not mutable owners.

### Generic Command Outcomes

- Domain commands return a stable result with `ACCEPTED`, `REJECTED`, or `NOT_IMPLEMENTED` status.
- `REJECTED` means the attempted public engine operation produced no accepted observable change. It
  does not claim an engine-defined cause.
- `NOT_IMPLEMENTED` means Bubble Craps cannot perform the request safely through the approved public
  v0.4.1 integration surface.
- Detailed error catalogs are deferred until the engine exposes authoritative rejection information
  or the product defines reasons independent of engine rules.

### Aggregate History

- A successful roll records dice, point before and after, shooter identity, total-player-cash delta,
  and detached layout observations.
- Bet changes caused directly by accepted player commands may be recorded as player-command changes.
- Before/after layout differences around a roll are observations only. They are never labeled as a
  per-bet win, loss, push, move, removal reason, payout, or attributable cash delta.
- Session statistics derive from aggregate observed transitions and do not recalculate outcomes.

### Snapshots And Undo

- The Milestone 1 `GameSession` shell retains its `undo_stack: list[SessionSnapshot]` type declaration
  to preserve the target architecture without remove-and-reintroduce churn.
- Milestone 2 does not initialize, populate, read, or restore from that stack and does not create or
  capture `SessionSnapshot` values.
- `undo`, `save`, and `load` return `NOT_IMPLEMENTED`.
- Snapshot design, restoration, serialization, and deterministic undo belong to Milestone 3.

## Decisions Required Before Behavioral Implementation

### Supported Bet Adapter Subset

Document the exact Bubble Craps request keys, engine constructors, accepted parameters, and detached
projection fields proposed for Milestone 2. Each binding must be demonstrably implementable with
public constructors and public attributes. Reject a proposed binding if it requires:

- A private engine member or reflection-based discovery.
- A copied point, winning-number, losing-number, payout, or legality table.
- Calling `Bet.get_result` outside the engine roll lifecycle.
- A Bubble Craps bankroll or wager calculation.

Bubble Craps request keys are application-owned integration keys, not engine-defined identifiers.

### Supported Convenience Commands

Evaluate clear, repeat, and double independently against the approved adapter and public v0.4.1
methods. Implement only a command with a bounded best-effort algorithm and no private or copied-rule
dependency. Otherwise return `NOT_IMPLEMENTED` and keep its available action false.

### Deferred Set Bets On/Off Command

The Interblock game description, Section 3.2, requires Set Bets On/Off to suppress resolution of
Place, Lay, Buy, Odds, and Hard Ways bets for the next roll regardless of point state. It also defines
command exclusions and automatic transitions for Lay, Odds, Place, and Buy bets after point and
seven-out events.

`crapssim==0.4.1` cannot represent this complete behavior. Its public `always_working` override
controls come-out behavior for only some bet classes; it does not disable eligible bets during
point-on rolls and Hard Ways has no corresponding public working-state capability.

Therefore, `set_bets_on_or_off` is deferred to Milestone 6. That milestone owns the required
`crapssim` change and published release, the exact-version dependency update, and complete domain,
persistence, controller, and GUI integration for Section 3.2. Until then, Milestone 2 must return
`NOT_IMPLEMENTED`, keep the corresponding available action false, and must not emulate the command
by removing bets from engine collections, skipping engine update steps, or reproducing lifecycle
rules in Bubble Craps.

## In Scope

- Pure-Python domain implementation under `src/bubblecraps/session/`.
- Integration with the exact published `crapssim==0.4.1` API.
- Classic and Crapless table construction with committed engine defaults, fixed
  `vig_rounding="none"`, and configured `vig_paid_on_win`.
- Interactive player creation with `NullStrategy`.
- A reviewed constructor/projection adapter for a limited supported bet subset.
- Detached state projection and conservative available-action computation.
- Best-effort place and remove commands plus separately approved clear, repeat, and double commands.
- One-roll orchestration, including explicit deterministic test outcomes.
- Aggregate roll, shooter, event, and player-command history.
- Cumulative session statistics and clean new-session behavior.
- Focused domain and installed-engine contract tests.

## Out Of Scope

- Any source change, local patch, or unreleased API in the `crapssim` repository.
- Arbitrary table-setting overrides or casino profiles beyond the approved vig policies.
- Per-bet roll outcomes, settlement reasons, payout attribution, or an engine event journal.
- Specific engine rejection reasons or transactional command guarantees.
- The Interblock Section 3.2 Set Bets On/Off command, which is assigned to Milestone 6 with its
  published engine prerequisite and cross-layer integration.
- Serialization, deserialization, metadata, migrations, or file-version checks.
- Snapshot values, undo-stack runtime behavior, restoration, or undo determinism. The existing
  future type declaration remains in the shell.
- Functional `GameSession.save`, `GameSession.load`, or `GameSession.undo` behavior.
- Controller forwarding, Qt signals, GUI behavior, asset loading, logging, and bootstrap wiring.
- Replay, strategy playback, auto-play, developer tools, or Easy Craps support.
- New game rules, payout logic, bet-resolution logic, or engine workarounds.

## Detailed Work Packages

## WP2.1: Domain Contract Reconciliation

Goal: finalize a domain API that states only what v0.4.1 can support safely.

Tasks:

- Apply the resolved money, immutability, generic-outcome, aggregate-history, and snapshot decisions.
- Remove unresolved `object` placeholders from Milestone 2 values.
- Define immutable command result values and generic statuses.
- Replace broad `TableSettings` and `casino_profile` configuration with the explicit
  `vig_paid_on_win` session option, defaulting to true.
- Reconcile existing `GameSession` stubs with supported, rejected, and deferred behavior.
- Ensure documentation makes no per-bet settlement or transactional rollback promise.

Deliverable: an agreed domain API with unsupported behavior represented explicitly.

## WP2.2: Immutable State And Action Model

Goal: produce a stable, recursively immutable representation for future controller use.

Tasks:

- Keep `GamePhase` values aligned with the PAG.
- Implement immutable `AvailableActions` and detached `GameState` values.
- Define the rule-neutral `BetState` fields as application ID, type identifier, amount, and optional
  number; WP2.4 owns the supported identifiers and engine mappings.
- Define immutable history and statistics projections with tuple collections and scalar counters.
- Define initial state: point off, no dice result, no last roll, and empty roll history.
- Publish detached bet-layout, history, and statistics values only.
- Centralize action computation inside `GameSession`.
- Keep `AvailableActions` as data only; dynamic action computation begins when WP2.7 constructs the
  live session and is never delegated to the controller or GUI.
- Treat action flags as conservative permission to attempt a command, not acceptance guarantees.
- Keep unsupported and Milestone 3 actions false.
- Test that published state cannot mutate the live session or expose a live engine object.

Deliverable: immutable state and action values with focused mutation-resistance tests.

## WP2.3: Minimal Configuration And Ruleset Factory

Goal: construct a valid engine table from minimal immutable session settings.

Tasks:

- Validate a finite positive starting bankroll.
- Represent supported rulesets with a string-valued enum containing only `classic` and `crapless`.
- Parse external identifiers through that enum and reject unknown values without silent fallback.
- Construct the corresponding public `crapssim.rules` object.
- Validate `vig_paid_on_win` as a boolean session option defaulting to true.
- Create a `Table` from engine defaults, then set `vig_rounding` to `"none"` and
  `vig_paid_on_win` to the configured value.
- Create exactly one player with `NullStrategy`.
- Do not add arbitrary table settings, casino profiles, or silent ruleset fallback.

Deliverable: validated minimal configuration and tested engine-default table construction.

## WP2.4: Reviewed Bet Adapter

Goal: translate a limited set of application requests into public engine bet constructors and active
bets into detached descriptive projections.

Tasks:

- Propose and approve the supported request and projection matrix before implementation.
- Replace the provisional `BetState.bet_type: str` field with a `BetType(StrEnum)` containing only
  approved Bubble Craps integration identifiers; do not treat every engine class or Interblock bet
  name as supported automatically.
- Use explicit reviewed bindings rather than reflection-based discovery.
- Validate only domain shape such as known keys and finite positive amounts; leave legality to the
  engine.
- Use public constructor parameters and public attributes only.
- Return generic rejection for unknown or unsupported requests.
- Add installed-v0.4.1 contract tests for every approved binding.

Deliverable: a narrow adapter and public-API tests with no copied rule behavior.

## WP2.5: Aggregate History Model

Goal: record session transitions without claiming unavailable per-bet roll authority.

Tasks:

- Implement per-instance immutable snapshots backed by internal append-only history ownership.
- Record UTC-aware timestamps through an injectable clock.
- Record initial `NEW_SESSION` followed by `NEW_SHOOTER` events.
- Record one aggregate record for every successful roll.
- Record dice, point before/after, shooter, total-player-cash delta, and detached layouts.
- Record accepted player-command changes with aggregate command cash delta.
- Record `POINT_ESTABLISHED`, `POINT_MADE`, `SEVEN_OUT`, and subsequent `NEW_SHOOTER` events from
  public before/after state.
- Do not classify roll-time bet differences or publish per-bet settlement amounts.

Deliverable: deterministic aggregate history grounded in public engine observations.

## WP2.6: Session Statistics

Goal: maintain cumulative statistics from aggregate authoritative transitions.

Minimum fields:

- Total rolls and total shooters started.
- Points established and points made.
- Seven-outs.
- Net total-player-cash change from the configured starting bankroll.

Tasks:

- Initialize all values for a new session and publish immutable snapshots.
- Update statistics exactly once after each successful roll.
- Count transitions from observed public engine state and recorded events.
- Calculate net change from public total-player-cash; do not calculate payouts.
- Ensure expected command rejection does not change statistics.

Deliverable: deterministic aggregate statistics with representative sequence tests.

## WP2.7: GameSession Construction And State Production

Goal: make `GameSession` the single constructible owner of a live session.

Tasks:

- Add an initializer accepting minimal configuration, an optional deterministic dice seam, and an
  injectable clock.
- Own one `Table`, one `Player`, one history owner, one statistics owner, and immutable settings.
- Retain the future `undo_stack` type declaration, but do not initialize or use it and do not
  construct a snapshot.
- Record initial `NEW_SESSION` and `NEW_SHOOTER` events in that order.
- Produce initial and post-command detached `GameState` values.
- Keep production dice random and timestamps UTC-based.
- Expose no alternative Bubble Craps runtime mutation path.

Deliverable: a constructible session with deterministic Classic and Crapless initial-state tests.

## WP2.8: Supported Best-Effort Bet Commands

Goal: implement supported player commands while preserving engine ownership.

Tasks:

- Place approved adapter requests through public bet constructors and `Player.add_bet`.
- Remove an identified projected bet through `Player.remove_bet` without private placement keys.
- Determine acceptance from detached public before/after observations and total-player-cash change.
- Return generic `REJECTED` when an expected refusal produces no observable change.
- Record accepted player-command changes with aggregate cash delta.
- Evaluate clear, repeat, and double independently.
- Return `NOT_IMPLEMENTED` when a convenience command cannot be bounded safely.
- Return `NOT_IMPLEMENTED` for `set_bets_on_or_off`; do not attempt a Bubble Craps workaround.
- Do not promise rollback after an unexpected exception.

Deliverable: tested supported commands and an explicit convenience-command limitation list.

## WP2.9: Roll Orchestration And Aggregate Transitions

Goal: advance one complete engine-owned roll and record aggregate effects.

Tasks:

- Reject a roll attempt when the interactive player has no active wager.
- Capture only public pre-roll values needed for aggregate history and statistics.
- Invoke `crapssim.TableUpdate.run` exactly once for each accepted roll.
- Use `NullStrategy` so strategy updates do not add bets.
- Pass explicit test dice through the public `dice_outcome` parameter.
- Observe public dice, point, shooter, detached layout, and total-player-cash values afterward.
- Append one roll record and update statistics once after successful completion.
- Derive only aggregate point and shooter events; do not infer per-bet outcomes.
- Return the synchronous session to `READY`; Qt-timed phases remain deferred.
- Do not claim strict failure atomicity after an unexpected engine exception.

Deliverable: deterministic aggregate transitions for representative Classic and Crapless sequences.

## WP2.10: New Session And Deferred Commands

Goal: complete the domain lifecycle without crossing into persistence or undo.

Tasks:

- Rebuild engine and domain internals from validated configuration for a new session.
- Verify no history, statistics, bets, dice, point, shooter, or identifier leaks from the old session.
- Record fresh `NEW_SESSION` and `NEW_SHOOTER` events.
- Return `NOT_IMPLEMENTED` for `set_bets_on_or_off`, undo, save, load, and unsupported convenience
  commands.

Deliverable: tested reset behavior and explicit deferred-command results.

## WP2.11: Domain Test Suite And Verification

Goal: prove the revised domain behavior and architecture boundaries.

Tasks:

- Add focused tests for values, configuration, adapter, state, history, statistics, commands, rolls,
  and lifecycle.
- Verify both rulesets, engine defaults plus the approved vig policies, `NullStrategy`, and
  deterministic outcomes.
- Verify every adapter binding uses public v0.4.1 constructors and attributes.
- Verify generic rejection and no history/statistics mutation after expected rejection.
- Verify aggregate event order, shooter lifecycle, statistics, and session reset.
- Assert that no per-bet roll outcome or attributable payout is published or inferred.
- Assert that runtime and tests do not import a sibling checkout or prospective contract module.
- Keep architecture tests passing and Qt out of session modules and tests.
- Run all project quality gates.

Deliverable: deterministic tests for every revised acceptance criterion.

## Required Test Scenarios

- New Classic and Crapless sessions using fixed unrounded vig and both supported
  `vig_paid_on_win` values.
- Unknown ruleset, non-finite money, non-positive bankroll, and malformed request rejection.
- One `NullStrategy` player and no automatic strategy bets during a roll.
- Approved adapter construction and detached projection for every supported binding.
- Unknown adapter key produces generic rejection without mutation.
- Successful and expected-rejected supported bet placement and removal.
- Explicit `NOT_IMPLEMENTED` results for `set_bets_on_or_off` and unsupported convenience commands.
- Roll without an active wager is rejected without mutation.
- Deterministic Classic come-out, point establishment, point made, and seven-out sequences.
- Deterministic Crapless extreme-point establishment through engine behavior.
- Dice, point before/after, shooter, total-player-cash delta, and layouts in aggregate roll records.
- Significant aggregate event order across multi-roll and shooter transitions.
- Statistics after point-made and seven-out sequences.
- Recursive state immutability and absence of live engine objects.
- No history or statistics change after an expected rejected command.
- New-session reset with no prior state or identifier leakage.
- Explicit `NOT_IMPLEMENTED` behavior for undo, save, and load.
- No test expects or reconstructs a per-bet roll outcome.

## Acceptance Criteria

- `GameSession` constructs one-player Classic or Crapless sessions from minimal explicit settings.
- Tables retain published engine defaults except for `vig_rounding="none"` and the configured
  `vig_paid_on_win` policy.
- The interactive player uses `NullStrategy` and receives no automatic strategy bets.
- The adapter's approved subset uses public v0.4.1 bindings only.
- Published state, history, statistics, and bet projections are immutable and detached.
- Available actions are conservative attempt permissions and unsupported actions remain false.
- Supported bet commands delegate mutation to public methods and report only generic outcomes.
- Expected rejected commands do not change published state, history, or statistics.
- Every accepted roll has an active wager, calls `TableUpdate.run` once, creates one aggregate roll
  record, and updates statistics once.
- Aggregate observations match the installed engine for deterministic sequences.
- No Bubble Craps value claims a per-bet roll outcome, payout attribution, or specific engine
  rejection reason.
- Unexpected exceptions are not described as transactionally rolled back.
- New-session reconstruction leaks no prior state or identifiers.
- `set_bets_on_or_off`, unsupported convenience commands, undo, save, and load return
  `NOT_IMPLEMENTED`.
- No snapshot or runtime undo stack is created or used in Milestone 2; only the future type
  declaration is retained.
- No Milestone 2 change is required in the `crapssim` repository.
- Session modules and tests contain zero Qt imports and duplicate no engine rules.
- Ruff formatting, Ruff lint, strict mypy, pytest, and `pip check` all pass.

## Verification Checklist

- Confirm the supported adapter matrix and clear, repeat, and double subset were approved first.
- Verify the sibling `crapssim` checkout is not a runtime or test dependency.
- Inspect every `crapssim` binding for public-only use.
- Verify no winning-number, losing-number, payout, point, removability, or working-state rule was
  copied into Bubble Craps.
- Verify tables retain engine defaults except for the approved vig policies and players use
  `NullStrategy`.
- Verify deterministic tests drive rolls through one `TableUpdate.run` call.
- Verify roll records remain aggregate and never classify per-bet layout differences.
- Verify state cannot mutate live session containers or engine instances.
- Verify history and statistics update once per successful roll and not after expected rejection.
- Verify unsupported commands return `NOT_IMPLEMENTED` and have false action flags.
- Verify no session code attempts to emulate Interblock Set Bets On/Off by mutating engine bet
  collections around a roll or reproducing its lifecycle transitions.
- Run `python -m compileall -q main.py src/bubblecraps`.
- Run `python tools/check.py`.
- Run `python -m pytest -v` and inspect all domain tests discovered.
- Verify `tests/test_architecture.py` still passes.
- Verify the installed engine is the exact published `crapssim==0.4.1` distribution.

## Risks And Mitigations

Risk: Bubble Craps becomes a second rules engine through adapter or command preflight.

- Mitigation: Approve explicit public bindings, validate request shape only, and reject mappings that
  need copied rule data or private behavior.

Risk: Silent engine command rejection is presented as a specific failure.

- Mitigation: Observe detached public state and return only generic `REJECTED`.

Risk: Before/after layouts are mistaken for authoritative settlement events.

- Mitigation: Record aggregate observations and prohibit per-bet roll classifications and payout
  attribution.

Risk: Best-effort multi-step commands imply transactional safety.

- Mitigation: Review convenience commands independently, document limitations, and return
  `NOT_IMPLEMENTED` when they cannot be bounded through public APIs.

Risk: Bubble Craps partially emulates Set Bets On/Off with `always_working` or temporary bet removal.

- Mitigation: Defer the command to Milestone 6, where a published engine release must implement the
  complete Interblock Section 3.2 behavior; return `NOT_IMPLEMENTED` throughout Milestone 2.

Risk: Frozen state leaks mutable engine or session ownership.

- Mitigation: Publish recursively immutable detached values and test mutation resistance.

Risk: Milestone 2 absorbs engine, undo, or persistence work.

- Mitigation: Require no engine changes, create no snapshots, leave the declared undo stack
  uninitialized and unused, and keep deferred commands explicit.

## Milestone 2 Exit Decision

- Pass: Every acceptance criterion is met through the exact published v0.4.1 API and all quality
  gates pass.
- Pass with follow-ups: Only non-behavioral documentation issues remain with owners and target
  milestones.
- Hold: The implementation depends on private or unreleased engine behavior, duplicates a rule,
  infers per-bet roll outcomes, leaks mutable ownership, or overstates command atomicity.

## Review Record

- Supported adapter request keys and constructors:
- Supported detached bet projection fields:
- Implemented convenience commands and limitations:
- Commands returning `NOT_IMPLEMENTED` (must include `set_bets_on_or_off`):
- Additional approved changes:

## Deliverables Summary

- Finalized domain values and generic command outcomes.
- Minimal validated configuration and engine-default ruleset factory.
- Approved public-only bet constructor/projection adapter.
- Immutable detached state, aggregate history, and statistics.
- Constructible `GameSession` with strategy-neutral engine ownership.
- Supported best-effort commands and explicit unsupported results.
- Deterministic aggregate roll orchestration and clean new-session lifecycle.
- Focused domain and installed-engine contract tests.
- Passing architecture and project quality gates.