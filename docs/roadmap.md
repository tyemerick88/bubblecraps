## Bubble Craps Roadmap

This roadmap is milestone-driven and aligned with the architecture and design constraints in [PAG-mini-v0.6.md](PAG-mini-v0.6.md).

## Milestone 0: Foundation and Guardrails

Objective:
- Establish project guardrails, tooling defaults, and architecture boundaries.

Scope:
- Confirm architecture contracts from PAG.
- Define package boundaries and allowed dependency directions.
- Define baseline quality gates for linting, typing, and tests.
- Expand repository usage and setup documentation in [README.md](../README.md).

Exit Criteria:
- Architecture constraints are documented and agreed.
- Development setup is reproducible from repository documentation.

## Milestone 1: Architecture Skeleton

Objective:
- Create a complete code skeleton across core layers without implementing full behavior.

Scope:
- Add folder/package structure for application, session, controller, GUI, assets, and tests.
- Add module stubs for state, history, snapshot, statistics, settings, and game session.
- Add SessionController and GUI shell stubs.
- Add placeholders for session persistence and configuration loading.

Exit Criteria:
- All planned modules exist and import cleanly.
- Session/domain layer is free of Qt framework types.

## Milestone 2: Domain Core Completion

Objective:
- Implement the pure Python domain model and session orchestration.

Scope:
- Implement immutable GameState, GamePhase, and AvailableActions.
- Implement SessionHistory, RollRecord, ShooterRecord, and SessionEvent.
- Implement SessionSnapshot and SessionConfiguration.
- Implement SessionStatistics update model.
- Implement GameSession orchestration using crapssim as the single rules source.

Exit Criteria:
- Domain tests pass for state transitions and history/statistics updates.
- No game-rule logic exists outside crapssim integration points.

## Milestone 3: Persistence and Undo Reliability

Objective:
- Make session state durable and reversible.

Scope:
- Implement .bcs serialization and deserialization with metadata and file version checks.
- Implement snapshot-before-mutation behavior for all mutating session actions.
- Add roundtrip save/load validation and undo determinism tests.

Exit Criteria:
- Save/load roundtrip reproduces equivalent session state.
- Undo consistently restores pre-action state.

## Milestone 4: Qt Bridge and Event Pipeline

Objective:
- Implement a stable bridge between GUI and domain.

Scope:
- Implement SessionController signals and command methods.
- Enforce legal action gating using AvailableActions.
- Emit lifecycle and state change signals on successful domain mutations.

Exit Criteria:
- Controller tests validate signal emission behavior.
- Illegal actions are rejected predictably without state corruption.

## Milestone 5: GUI Baseline and Authentic Interaction Shell

Objective:
- Deliver a cohesive state-driven game screen shell aligned with PAG authenticity goals.

Scope:
- Build main game surface and table interaction shell.
- Implement AssetManager abstraction so widgets do not hardcode asset paths.
- Drive control enablement exclusively from AvailableActions.
- Represent the Interblock Set Bets On/Off control as unavailable until Milestone 6 adds the required
  published engine capability and domain integration.
- Add animation scaffolding where visuals reflect, but never mutate, game state.

Exit Criteria:
- End-to-end flow from controller state to GUI rendering is stable.
- Asset access occurs through AssetManager only.

## Milestone 6: Ruleset Compliance and Diagnostics Hardening

Objective:
- Validate initial gameplay alignment and strengthen operational diagnostics.

Scope:
- Set Crapless as the default startup ruleset.
- Validate representative behavior against PAG-aligned Interblock requirements.
- Add the complete Interblock Section 3.2 Set Bets On/Off behavior to `crapssim`, release it as a
  published engine version, and update Bubble Craps to that exact version.
- Integrate engine-owned next-roll suppression for Place, Lay, Buy, Odds, and Hard Ways bets,
  including the documented command exclusions and automatic point and seven-out transitions.
- Implement `GameSession.set_bets_on_or_off`, detached working-state projection, history, snapshots,
  undo, available actions, controller forwarding, and GUI activation against the published engine
  capability.
- Implement centralized LoggingManager with rotating file handling and crash capture.
- Keep application diagnostics separate from gameplay history structures.

Exit Criteria:
- Compliance checklist exists with pass/fail evidence for core scenarios.
- Interblock Section 3.2 behavior passes engine, domain, persistence, controller, and GUI tests
  without Bubble Craps duplicating working-state or settlement rules.
- Set Bets On/Off is enabled only when the installed published engine reports the required behavior.
- Logging rotation and crash capture paths are verified.

## Milestone 7: Release Candidate for Core Experience

Objective:
- Stabilize the core experience for an initial release candidate.

Scope:
- Run regression across domain, persistence, controller, and GUI shell.
- Perform manual authenticity review against PAG goals.
- Freeze initial file format and configuration defaults.
- Confirm the exact published `crapssim` version selected in Milestone 6 satisfies the finalized
  Bubble Craps v0.1.0 engine contract, including Interblock Section 3.2.
- Record known gaps and post-release priorities.

Exit Criteria:
- Critical tests are passing.
- The exact published crapssim package passes the full Bubble Craps integration suite.
- Bubble Craps v0.1.0 requires no local or VCS crapssim checkout.
- Remaining issues are triaged with severity and follow-up plans.

## Parallel Workstreams

- Workstream A: Domain and persistence implementation.
- Workstream B: Controller integration and signal behavior validation.
- Workstream C: GUI shell and asset abstraction.
- Workstream D: Compliance verification and logging hardening.

## Scope Boundaries

Included in this roadmap:
- Core architecture layers.
- Domain correctness and state model.
- Persistence and undo reliability.
- Controller bridge and GUI baseline shell.
- Initial compliance and diagnostics hardening.

Deferred until after milestone completion of core release candidate:
- Advanced convenience features such as strategy playback and auto-play.
- Expanded theme variations beyond initial authentic presentation.
- Non-essential developer tooling enhancements.
