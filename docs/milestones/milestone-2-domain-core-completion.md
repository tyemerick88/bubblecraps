# Milestone 2: Domain Core Completion

- Status: Draft for review
- Roadmap source: [docs/roadmap.md](../roadmap.md)
- Primary architecture reference: [docs/PAG-mini-v0.6.md](../PAG-mini-v0.6.md)
- Supporting design reference: [docs/PAG-v0.6.md](../PAG-v0.6.md)
- Depends on: [Milestone 1](milestone-1-architecture-skeleton.md)

## Milestone Intent

Milestone 2 turns the pure-Python session skeleton from Milestone 1 into a tested domain core. It
implements session state, history, statistics, configuration, and `GameSession` orchestration while
continuing to use `crapssim` as the sole authority for rules, bet legality, dice resolution, point
transitions, payouts, and bankroll effects.

The milestone ends with a deterministic, headless game session that can be exercised entirely from
Python. It does not implement persistence, reliable undo, Qt controller behavior, or GUI rendering.

## Completed Foundation

Milestone 0 established:

- The authoritative dependency direction and runtime ownership contract.
- The rule that game behavior belongs in `crapssim`, not Bubble Craps.
- Python, dependency, formatting, linting, typing, and test baselines.
- The exact published `crapssim==0.4.1` dependency and engine ownership policy.

Milestone 1 established:

- Importable `application`, `assets`, `controller`, `gui`, and `session` packages.
- Session model and orchestration signatures under `src/bubblecraps/session/`.
- A Qt-aware controller shell and GUI shell without behavioral wiring.
- Application configuration, logging, session persistence, and asset ownership placeholders.
- Automated dependency-boundary, import-cycle, public-contract, and engine-source checks.
- A tracked physical asset hierarchy and updated repository documentation.

Milestone 2 builds on those boundaries. It must not move behavior into another layer or weaken the
Milestone 0 architecture tests.

## What Will Be Accomplished

By the end of Milestone 2, the project will have:

- A constructible `GameSession` that owns one `crapssim.Table` and one `crapssim.Player`.
- Explicit ruleset selection and validated immutable session configuration.
- A strategy-neutral interactive player that does not place automatic simulation bets.
- Deterministic and random single-roll orchestration through `crapssim.TableUpdate`.
- Immutable GUI-facing state values and centrally computed available actions.
- Complete roll, shooter, event, and bet-change history models.
- A defined cumulative session-statistics model updated from session outcomes.
- Core bet command orchestration that delegates legality and bankroll effects to `crapssim`.
- Domain tests covering successful commands, rejected commands, transitions, history, statistics,
  ruleset behavior, and deterministic roll sequences.

## Architecture Invariants

The following rules are non-negotiable:

- `src/bubblecraps/session/` contains no PySide6, controller, GUI, application, or asset imports.
- `GameSession` is the only Bubble Craps runtime class that mutates live `crapssim` objects.
- Bubble Craps does not reproduce winning numbers, losing numbers, payout ratios, point rules, bet
  legality, removability, or bankroll calculations.
- `GameState` and `AvailableActions` are produced by `GameSession`; callers do not infer legality.
- Domain tests use explicit dice outcomes or seeds and do not depend on uncontrolled randomness.
- No controller signal behavior or GUI behavior is used as evidence of a domain transition.
- Persistence, logging, and application configuration remain separate from gameplay history.

## Decisions Required Before Implementation

The PAG and current engine leave several contracts ambiguous. These decisions should be reviewed and
recorded before implementation begins.

### Decision 1: Monetary Type

Current conflict:

- The PAG types bankroll and deltas as `int`.
- `crapssim.Player.bankroll`, bet amounts, vigs, and payouts are `float` and may produce fractional
  values.

Proposed decision:

- Use `float` for bankroll, wager amounts, bankroll deltas, shooter profit, and session profit inside
  the domain model.
- Do not truncate engine values with `int(...)`.
- Formatting and currency display remain GUI responsibilities.
- Add deterministic tests using values with exact expected payouts and `pytest.approx` where binary
  floating-point comparison requires it.
- Update the PAG document to reflect this fix after implemetation.

Approval impact:

- `GameState.bankroll`, `RollRecord.bankroll_delta`, `ShooterRecord.profit`, and
  `SessionConfiguration.starting_bankroll` change from `int` to `float`.

### Decision 2: Meaning of Immutable `GameState`

Current conflict:

- The architecture contract requires immutable GUI-facing state.
- The PAG currently places mutable `list[Bet]`, `SessionHistory`, and `SessionStatistics` objects in a
  frozen dataclass.
- A frozen outer dataclass does not prevent callers from mutating nested engine or list objects.

Proposed decision:

- `GameState` must be a detached read-only projection, not a view of live session containers.
- Use tuples for collections exposed by state.
- Add a small immutable bet projection in `state.py` only if the required GUI-facing fields can be
  agreed without duplicating game rules. Do not expose mutable live `Bet` instances as public state.
- Expose immutable history and statistics snapshots, or immutable copies, rather than the mutable
  owners used internally by `GameSession`.
- Update the PAG document to reflect this fix after implemetation.

Alternative requiring explicit acceptance:

- Retain live references and define immutability as a caller convention. This is smaller but does not
  satisfy deep immutability and permits accidental mutation outside `GameSession`.

### Decision 3: Statistics Contract

The PAG says `SessionStatistics` tracks cumulative statistics but does not define its fields.

Proposed minimum fields:

- Total rolls.
- Total shooters started.
- Points established.
- Points made.
- Seven-outs.
- Net bankroll change from the configured starting bankroll.

Statistics should be updated from recorded transitions or derived from history. They must not
recalculate game outcomes independently of `crapssim`.

### Decision 4: Bet Working Controls

The Milestone 1 `GameSession` shell contains `set_bets_on_or_off`, but `crapssim` does not currently
provide one generic public operation for changing every bet's working state. Some bet classes expose
an `always_working` override while others intentionally do not.

Proposed decision:

- Do not implement generic working-state rules in Bubble Craps.
- Before implementing this command, either add a reviewed public capability to `crapssim` or define
  an engine-owned protocol identifying supported bets and legal transitions.
- Keep the Bubble Craps method unavailable until the engine contract exists.

### Decision 5: Snapshot Boundary

The roadmap names `SessionSnapshot` in Milestone 2, while Milestone 3 owns snapshot-before-mutation,
undo restoration, serialization, and reliability.

Proposed decision:

- Milestone 2 finalizes and tests the snapshot value contract only.
- Do not push snapshots onto an undo stack and do not restore snapshots in Milestone 2.
- Deep-copy strategy, pre-mutation capture, deterministic restoration, and persistence belong to
  Milestone 3.

## In Scope

- Pure-Python domain implementation under `src/bubblecraps/session/`.
- Integration with the pinned `crapssim` APIs through `GameSession`.
- Ruleset construction for rulesets supported by the pinned engine.
- Interactive player creation with `crapssim.strategy.tools.NullStrategy`.
- State projection and available-action computation.
- Core bet placement, removal, repeat, double, clear, and supported working-state commands.
- One-roll orchestration, including deterministic test outcomes.
- Roll, shooter, event, and bet-change history.
- Cumulative session statistics.
- Session reset/new-session behavior that does not perform persistence.
- Focused domain and engine-contract tests.

## Out of Scope

- `.bcs` serialization, deserialization, metadata, migrations, or file-version checks.
- Snapshot-before-every-mutation enforcement, undo restoration, or undo determinism.
- `GameSession.save`, `GameSession.load`, and functional `GameSession.undo` behavior.
- SessionController command forwarding, action gating, or Qt signal emission.
- Application bootstrap wiring, configuration-file I/O, or logging implementation.
- GUI rendering, animation, user interaction, or asset loading.
- Session replay, strategy playback, auto-play, or developer tools.
- New game rules, payout logic, bet-resolution logic, or engine workarounds in Bubble Craps.
- Easy Craps support unless the pinned `crapssim` revision exposes and tests that ruleset.

## Detailed Work Packages

## WP2.1: Domain Contract Reconciliation

Goal:

- Resolve the type and ownership ambiguities before behavioral code is added.

Tasks:

- Approve the monetary type used by domain values.
- Approve the deep-immutability strategy for `GameState`.
- Approve the initial `SessionStatistics` fields.
- Reconcile the mini PAG's `GameSession` command names with the fuller PAG where they differ.
- Define which existing command stubs remain unavailable until later milestones or engine support.
- Update the PAG or architecture documentation when an approved decision changes a published type or
  public contract.

Deliverable:

- An agreed domain API with no unresolved `object` placeholders or contradictory ownership rules.

## WP2.2: Immutable State and Action Model

Goal:

- Produce a stable, read-only representation of the current session for future controller use.

Tasks:

- Keep `GamePhase` values aligned with the PAG.
- Implement `AvailableActions` as an immutable value.
- Implement `GameState` as an immutable, detached projection according to Decision 2.
- Define initial state before any roll: point off, no dice result, no last roll, and empty history.
- Centralize all action computation inside `GameSession`.
- Keep Milestone 3 actions unavailable: `can_undo`, `can_save`, and `can_load` remain false.
- Represent unavailable engine-dependent actions as false rather than approximating legality.
- Verify state creation does not leak mutable session containers or mutable engine ownership when the
  detached-state decision is approved.

Deliverable:

- Immutable state and action values with focused construction, equality, and mutation-resistance
  tests.

## WP2.3: Session Configuration and Ruleset Factory

Goal:

- Construct a valid engine table from explicit immutable session settings.

Tasks:

- Validate a positive starting bankroll.
- Validate supported ruleset identifiers explicitly; reject unknown values instead of silently
  falling back to another ruleset.
- Support `classic` and `crapless` only while those are the pinned engine's supported application
  rulesets.
- Construct the corresponding `crapssim.rules` object in the session layer.
- Create a new `Table`, merge approved `TableSettings` overrides into engine defaults, and preserve
  the pinned `come_out_working_policy` contract.
- Create exactly one player using `NullStrategy` so interactive sessions never receive automatic
  strategy bets.
- Keep the Crapless startup default decision deferred to Milestone 6; Milestone 2 callers must pass
  an explicit configuration or use an explicitly documented neutral test default.

Deliverable:

- Validated `SessionConfiguration` and a tested ruleset-to-engine construction boundary.

## WP2.4: History and Bet-Change Model

Goal:

- Record every roll and significant session transition without using application logs.

Tasks:

- Implement constructible `SessionHistory` collections with per-instance storage.
- Keep `RollRecord`, `ShooterRecord`, and `SessionEvent` aligned with PAG field ownership.
- Replace `RollRecord.bet_changes: list[object]` with the PAG-defined `BetChange` type.
- Add `BetAction` and `BetChangeReason` values from the full PAG unless WP2.1 approves a narrower
  contract.
- Record UTC-aware timestamps through an injectable clock or another deterministic test boundary.
- Record one `RollRecord` for every successful roll.
- Record `NEW_SESSION`, `NEW_SHOOTER`, `POINT_ESTABLISHED`, `POINT_MADE`, and `SEVEN_OUT` events from
  observed engine transitions.
- Reserve the `UNDO`, `SESSION_SAVED`, and `SESSION_LOADED` event types and the `UNDO` and `LOAD`
  bet-change reasons for Milestone 3.
- Do not infer wins, losses, or payout values by reimplementing bet rules. If the current engine does
  not expose enough result detail for accurate `BetChange` records, add that capability to
  `crapssim` and advance the pinned revision deliberately.

Deliverable:

- Complete, deterministic history values backed by engine-observed transitions.

## WP2.5: Session Statistics

Goal:

- Maintain cumulative statistics from authoritative session outcomes.

Tasks:

- Implement the fields approved in Decision 3.
- Initialize all counters and net values for a new session.
- Update statistics exactly once after each successful roll.
- Count point and shooter transitions from engine state/history events rather than duplicate rules.
- Calculate net bankroll change from engine-owned bankroll values and configured starting bankroll.
- Ensure failed or rejected commands do not change statistics.
- Define whether statistics are internally mutable with immutable state snapshots or represented as
  replacement immutable values.

Deliverable:

- A deterministic statistics update model with tests for initial state and representative roll
  sequences.

## WP2.6: GameSession Construction and State Production

Goal:

- Make `GameSession` the single constructible owner of a live session.

Tasks:

- Add an initializer accepting `SessionConfiguration` and optional test seams approved below.
- Own one `Table`, one `Player`, one history owner, one statistics owner, and immutable settings.
- Initialize an empty undo stack without capturing or restoring snapshots.
- Record the initial `NEW_SESSION` event.
- Produce the initial and post-command `GameState` values.
- Add narrow injection points for deterministic dice outcomes and timestamps. Keep production defaults
  random and UTC-based.
- Do not expose alternative mutation paths around `GameSession` in Bubble Craps runtime code.

Deliverable:

- A constructible session with deterministic initial-state tests for Classic and Crapless rulesets.

## WP2.7: Bet Command Orchestration

Goal:

- Implement core player commands while leaving all legality and bankroll effects to `crapssim`.

Tasks:

- Change `place_bet` to accept a concrete `Bet` and delegate to `Player.add_bet`.
- Add or finalize `remove_bet` and delegate removability and returned wager handling to
  `Player.remove_bet`.
- Detect rejected engine commands and return or raise a stable domain outcome without partial state
  changes. The exact outcome contract must be approved in WP2.1 for later controller translation.
- Track the most recent successful player bet set needed by repeat and double commands.
- Implement `repeat_last_bet`, `double_bet`, and `clear_all_bets` by composing public engine bet-copy,
  add, and remove operations; do not mutate bankroll directly.
- Implement `set_bets_on_or_off` only after Decision 4 has an engine-owned contract.
- Recompute available actions after every successful command.
- Verify illegal, unaffordable, non-removable, and unsupported commands leave state, history, and
  statistics unchanged.

Deliverable:

- Tested core bet commands that never bypass engine legality or bankroll ownership.

## WP2.8: Roll Orchestration and Domain Transitions

Goal:

- Advance the session by one complete engine-owned roll and record its effects.

Tasks:

- Capture only the pre-roll values needed to describe changes; do not create an undo snapshot.
- Invoke `crapssim.TableUpdate.run` exactly once for each accepted roll.
- Use the interactive player's `NullStrategy` so `TableUpdate.run_strategies` does not add bets.
- Support an explicit dice outcome test seam that passes through `TableUpdate.run(...,
  dice_outcome=...)`; do not set point, payouts, or bankroll directly in tests.
- Observe point, shooter, dice, bet, and bankroll values before and after the engine update.
- Append history records and update statistics only after successful engine completion.
- Return the session to `READY` after the synchronous domain operation. `ROLLING`, `RESOLVING`, and
  `ANIMATING` timing across Qt signals is deferred to Milestone 4/5 unless a transient phase observer
  is explicitly introduced and tested without Qt.
- Define failure atomicity: if engine execution raises, do not append partial history or statistics.
  Full rollback remains Milestone 3, so any stronger atomicity requirement must be designed there.

Deliverable:

- Deterministic roll transitions for come-out wins, point establishment, point made, seven-out, and
  representative bet outcomes under both supported rulesets.

## WP2.9: New Session and Deferred Commands

Goal:

- Complete the domain lifecycle without crossing into persistence or undo.

Tasks:

- Implement `new_session` as a clean reconstruction from validated configuration, or define a class
  factory if replacing the object is safer than mutating it in place.
- Verify no history, statistics, bets, dice result, or point state leaks from the previous session.
- Leave `undo`, `save`, and `load` explicitly unavailable and raising a stable not-supported outcome
  until Milestone 3.
- Keep snapshot restoration and persistence module behavior unimplemented.

Deliverable:

- Tested session reset behavior and explicit deferred-command behavior.

## WP2.10: Domain Test Suite and Verification

Goal:

- Prove the domain behavior and architecture boundaries needed for Milestone 3 and 4.

Tasks:

- Replace the Milestone 1 session import test with focused modules for state, settings, history,
  statistics, and `GameSession` behavior.
- Test success, rejection, and no-mutation-on-rejection for every implemented command.
- Test deterministic roll sequences with explicit dice outcomes.
- Test Classic and Crapless point behavior through the `crapssim` integration boundary.
- Test initial and updated `AvailableActions` values.
- Test history ordering, UTC timestamps, shooter records, events, bet changes, and statistics.
- Test state immutability according to the approved Decision 2 contract.
- Add runtime contract tests for every `crapssim` API newly relied upon by Bubble Craps, including
  `NullStrategy`, deterministic `TableUpdate.run`, ruleset classes, bet-copy behavior, and any new
  engine capability added for bet changes or working controls.
- Keep `tests/test_architecture.py` passing and add no Qt imports to domain tests or modules.
- Run all project quality gates.

Deliverable:

- Deterministic domain and integration tests that demonstrate all Milestone 2 acceptance criteria.

## Required Test Scenarios

At minimum, tests should cover:

- New Classic session initial state.
- New Crapless session initial state.
- Unknown ruleset and invalid bankroll rejection.
- Table-settings override without loss of engine defaults.
- Successful and rejected bet placement.
- Successful and rejected bet removal.
- Repeat, double, clear, and supported on/off behavior.
- No automatic strategy bet placement during a roll.
- Come-out natural and Classic craps outcomes through engine behavior.
- Classic point establishment, point made, and seven-out.
- Crapless extreme-point establishment for 2, 3, 11, or 12.
- Dice values, point before/after, shooter number, and bankroll delta in `RollRecord`.
- Significant event order for a deterministic multi-roll sequence.
- Shooter roll count, points made, and profit.
- Statistics after point made and seven-out sequences.
- State and action values before and after each command.
- No history/statistics changes after a rejected command.
- New-session reset with no prior-state leakage.
- Explicit not-supported behavior for Milestone 3 commands.

## Acceptance Criteria

All criteria must be true:

- `GameSession` constructs a valid single-player Classic or Crapless session from explicit settings.
- The interactive player uses no automatic betting strategy.
- `GameState` and `AvailableActions` satisfy the approved immutability contract.
- All action legality is computed by `GameSession` and all bet legality is delegated to `crapssim`.
- Every successful roll produces exactly one `RollRecord` and updates statistics exactly once.
- Point, shooter, bankroll, and bet outcomes match the pinned engine for deterministic sequences.
- Significant session events are ordered and derived from observed engine transitions.
- Core bet commands preserve engine ownership of legality and bankroll effects.
- Rejected commands do not partially mutate domain history or statistics.
- `SessionConfiguration`, `SessionHistory`, `SessionStatistics`, and the Milestone 2 portion of
  `SessionSnapshot` are constructible and tested.
- Undo restoration, save/load, Qt behavior, GUI behavior, and logging remain unimplemented.
- Session modules and tests contain zero Qt imports.
- No Bubble Craps module duplicates `crapssim` rules or payout calculations.
- Ruff formatting, Ruff lint, strict mypy, pytest, and `pip check` all pass.

## Verification Checklist

Reviewer checklist:

- Confirm all five decisions in this document were resolved and reflected in code/docs.
- Inspect every `crapssim` import and verify it occurs only in the session layer or tests.
- Verify no winning-number, losing-number, payout-ratio, or point-transition tables were copied into
  Bubble Craps.
- Verify `NullStrategy` prevents simulation-driven bets in an interactive session.
- Verify deterministic tests drive rolls through `TableUpdate`, not by manually mutating post-roll
  state.
- Verify state cannot mutate the live session through exposed containers under the approved contract.
- Verify history and statistics update once per successful roll and not for rejected commands.
- Verify unsupported rulesets and commands fail predictably.
- Run `python -m compileall -q main.py src/bubblecraps`.
- Run `python tools/check.py`.
- Run `python -m pytest -v` and inspect all domain tests discovered.
- Verify `tests/test_architecture.py` still passes.
- Verify the installed engine is the exact published `crapssim==0.4.1` package.

## Deliverables Summary

Milestone 2 is complete only when all items exist and are reviewable:

- Approved domain contract decisions and any required PAG amendments.
- Immutable state and available-action implementation.
- Validated session configuration and supported ruleset factory.
- Constructible history, bet-change, statistics, and snapshot value models.
- Constructible `GameSession` with strategy-neutral engine ownership.
- Core bet command and deterministic roll orchestration.
- New-session lifecycle and explicit deferred-command behavior.
- Focused, deterministic domain and engine-integration tests.
- Passing architecture and project quality gates.

## Risks and Mitigations

Risk: Bubble Craps accidentally becomes a second rules engine.

- Mitigation: Delegate all legality and resolution to public `crapssim` APIs and review domain tests
  for copied number or payout tables.

Risk: A frozen `GameState` leaks mutable engine objects.

- Mitigation: Resolve Decision 2 before implementation and test mutation resistance explicitly.

Risk: Monetary values are truncated or compared incorrectly.

- Mitigation: Resolve Decision 1, preserve engine values, and use appropriate approximate assertions
  only at the integration boundary.

Risk: `TableUpdate` automatically places strategy bets.

- Mitigation: Construct the interactive player with `NullStrategy` and add a regression test proving
  no automatic bets appear.

Risk: History cannot distinguish won, lost, moved, or removed bets from before/after lists.

- Mitigation: Add an engine-owned result/event capability rather than infer game rules in Bubble
  Craps.

Risk: Milestone 2 absorbs undo or persistence work.

- Mitigation: Limit snapshots to their approved value contract; defer capture stacks, restoration,
  serialization, and file handling to Milestone 3.

Risk: Transient `GamePhase` values imply asynchronous behavior in a synchronous domain call.

- Mitigation: Keep externally observable asynchronous phase transitions for the Qt event pipeline in
  Milestone 4/5 unless a pure-domain observer contract is explicitly approved.

## Milestone 2 Exit Decision

Decision options:

- Pass: All acceptance criteria are satisfied and deterministic domain tests pass.
- Pass with follow-ups: Only non-behavioral documentation issues remain with owners and target
  milestones.
- Hold: Domain state leaks mutable ownership, game rules are duplicated, deterministic transitions
  fail, or undo/persistence/controller behavior has crossed milestone boundaries.

## Review Notes

Use this section to record decisions before implementation:

- Monetary type:
- Immutable state strategy:
- Statistics fields:
- Bet working-control engine contract:
- Snapshot boundary:
- Additional approved changes:
