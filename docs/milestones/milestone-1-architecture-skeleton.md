# Milestone 1: Architecture Skeleton

- Status: Complete
- Roadmap source: [docs/roadmap.md](../roadmap.md)
- Primary architecture reference: [docs/PAG-mini-v0.6.md](../PAG-mini-v0.6.md)
- Depends on: [Milestone 0](milestone-0-foundation-and-guardrails.md)

## Milestone Intent

Milestone 1 creates the code scaffolding across all architectural layers. No behavioral logic is implemented yet. The goal is to establish the structural foundation: folder organization, module stubs, import paths, and layer boundaries that will guide feature implementation in later milestones.

## Completion Summary

Milestone 1 delivered:
- A complete folder and package structure matching PAG layout.
- All planned domain modules as importable stubs (state, history, snapshot, statistics, settings, game_session).
- SessionController Qt bridge stub with placeholder signal definitions.
- GUI shell stub capable of receiving and displaying state updates.
- Placeholder modules for future persistence and configuration.
- An importable but non-functional application entry point.
- All imports resolve cleanly with no circular dependencies.
- Session/domain layer verified to contain zero Qt type imports.

## In Scope

- Create all planned folder structures and package directories.
- Create module stubs for session domain layer.
- Create SessionController stub with Qt signal contract.
- Create GUI shell stub with minimal layout structure.
- Create test directory structure and placeholder test modules.
- Create assets directory structure matching PAG.
- Establish __init__.py files and module-level docstrings.
- Verify import hygiene across layers.

## Out of Scope

- Implementing state transition logic.
- Implementing GUI rendering or interactivity.
- Implementing any game rules or session orchestration logic.
- Implementing persistence serialization.
- Creating actual asset files (images, sounds, fonts).
- Implementing tests beyond import verification.

## Detailed Work Packages

## WP1.1: Root Project Structure

Status: Complete

Goal:
- Create the top-level folder layout and entry points.

Tasks:
- Create root `main.py` as a thin application entry point.
- Create `src/bubblecraps/` and `src/bubblecraps/__init__.py` with version metadata.
- Create `src/bubblecraps/__main__.py` to support `python -m bubblecraps`.
- Create `src/bubblecraps/application/bootstrap.py` as the composition root used by both entry
  points.
- Ensure entry points import only the application bootstrap, not controller or GUI modules directly.
- Verify both entry points import without errors.

Deliverable:
- Root `main.py`, package `__main__.py`, package metadata, and application bootstrap created and
  importable.

## WP1.2: Session Domain Package Structure

Status: Complete

Goal:
- Create the pure-Python session layer with placeholder classes.

Tasks:
- Create `src/bubblecraps/session/` and its `__init__.py`.
- Create `src/bubblecraps/session/state.py` with stub class definitions:
  - GamePhase (enum)
  - AvailableActions (dataclass)
  - GameState (dataclass)
- Create `src/bubblecraps/session/history.py` with stub class definitions:
  - RollRecord (dataclass)
  - ShooterRecord (dataclass)
  - SessionEvent (dataclass)
  - SessionHistory (class)
- Create `src/bubblecraps/session/snapshot.py` with stub class:
  - SessionSnapshot (dataclass)
- Create `src/bubblecraps/session/settings.py` with stub class:
  - SessionConfiguration (dataclass)
- Create `src/bubblecraps/session/statistics.py` with stub class:
  - SessionStatistics (class)
- Create `src/bubblecraps/session/game_session.py` with stub class:
  - GameSession (class with placeholder methods: roll, undo, place_bet, etc.)
- Verify zero Qt imports in any session module.

Deliverable:
- All session modules created with minimal docstrings and stub class signatures.
- No Qt framework types present in session modules.

## WP1.3: Controller Bridge Package Structure

Status: Complete

Goal:
- Create the Qt-aware controller layer.

Tasks:
- Create `src/bubblecraps/controller/` and its `__init__.py`.
- Create `src/bubblecraps/controller/session_controller.py` with stub class:
  - SessionController(QObject) with placeholder signals:
    - state_changed = Signal(GameState)
    - session_loaded = Signal()
    - session_saved = Signal()
    - session_reset = Signal()
  - Placeholder methods: roll(), undo(), place_bet(), etc.
- Verify controller imports GameState without creating circular dependencies.

Deliverable:
- SessionController stub created with Qt signal contract.

## WP1.4: GUI Package Structure

Status: Complete

Goal:
- Create the GUI layer with minimal shell scaffolding.

Tasks:
- Create `src/bubblecraps/gui/` and its `__init__.py`.
- Create `src/bubblecraps/gui/main_window.py` with stub class:
  - MainWindow(QMainWindow)
  - Placeholder layout with title, status bar, central widget.
- Create `src/bubblecraps/gui/table_widget.py` with stub class:
  - TableWidget (QWidget or QGraphicsView) for craps table rendering.
- Create `src/bubblecraps/gui/animations.py` with a stub for future animation logic.
- Create `src/bubblecraps/gui/styles.py` with a stub for stylesheets.
- Verify GUI modules do not import from session domain directly.

Deliverable:
- GUI shell structure created with placeholder widget classes.

## WP1.5: Application and Persistence Placeholders

Status: Complete

Goal:
- Place infrastructure stubs in the layer that owns each responsibility.

Tasks:
- Create `src/bubblecraps/application/` and its `__init__.py`.
- Create `src/bubblecraps/application/configuration.py` for application-preference loading stubs.
- Create `src/bubblecraps/application/logging.py` for centralized logging setup stubs.
- Create `src/bubblecraps/session/persistence.py` for future `.bcs` serialization stubs.
- Keep session rules and action legality in `GameSession` and `AvailableActions`; do not add generic
  validation helpers.
- Keep constants in their owning modules; do not create a generic `utils` or `constants` package.

Deliverable:
- Application configuration, logging, and session persistence ownership is represented by importable
  stubs.

## WP1.6: Asset Directory Structure

Status: Complete

Goal:
- Create the asset folder hierarchy per PAG.

Tasks:
- Create `src/bubblecraps/assets/` and its `__init__.py`.
- Create `src/bubblecraps/assets/asset_manager.py` with the semantic `AssetManager` interface.
- Create the repository-level physical `assets/` directory with subdirectories:
  - assets/chips/
  - assets/dice/
  - assets/table/
  - assets/puck/
  - assets/buttons/
  - assets/icons/
  - assets/fonts/
  - assets/sounds/ with subdirectories:
    - sounds/dice/
    - sounds/chips/
    - sounds/ui/
    - sounds/payouts/
  - assets/themes/
- Create .gitkeep files in empty directories so folder structure is preserved.

Deliverable:
- AssetManager package and physical asset directory structure created and tracked in git.

## WP1.7: Test Scaffold

Status: Complete

Goal:
- Create test directory structure and placeholder tests.

Tasks:
- Add focused import and public-contract tests under the existing `tests/` directory.
- Add test modules mirroring each new package; do not add empty placeholder tests.
- Verify all tests import cleanly and can be discovered by pytest.

Deliverable:
- Import and public-contract tests for the skeleton modules.

## WP1.8: Configuration Placeholders

Status: Complete

Goal:
- Create placeholders for future session and app configuration loading.

Tasks:
- Keep application preferences in `application/configuration.py`.
- Keep session configuration models in `session/settings.py`.
- Keep `.bcs` session persistence in `session/persistence.py`.
- Add module docstrings describing each format boundary without implementing serialization.

Deliverable:
- Application preferences, session settings, and session persistence have distinct owners.

## WP1.9: Dependency Graph Verification

Status: Complete

Goal:
- Ensure import structure matches architecture contract.

Tasks:
- Verify the import dependency graph:
  - session modules contain no Qt imports.
  - controller imports session state but not GUI, assets, application, or `crapssim`.
  - GUI imports controller and assets but not session or `crapssim`.
  - assets import no application, controller, GUI, session, or `crapssim` modules.
  - root `main.py` and package `__main__.py` import only the application bootstrap.
- Create a simple import test that confirms no circular dependencies exist.
- Keep `tests/test_architecture.py` passing as each package is introduced.
- Reference the Milestone 0 architecture contract rather than duplicating dependency policy in code
  comments.

Deliverable:
- Import graph verification test or documentation.

## WP1.10: Root README Updates

Status: Complete

Goal:
- Add pointers from README to Milestone 1 structure documentation.

Tasks:
- Add a "Project Structure" section to README explaining the folder layout.
- Reference [docs/PAG-mini-v0.6.md](../PAG-mini-v0.6.md) for architecture.
- Add a validation command: "python -c 'import bubblecraps; print(bubblecraps.__version__)'"

Deliverable:
- README updated with structure overview and verification command.

## Deliverables Summary

All Milestone 1 deliverables are complete and reviewable:

- [x] Folder and package structure matching the PAG template.
- [x] All planned session domain modules as importable stubs.
- [x] SessionController stub with Qt signal contract.
- [x] GUI shell stub with placeholder widgets.
- [x] Focused import and public-contract tests mirroring the runtime packages.
- [x] Asset directory structure preserved with tracked marker files.
- [x] Application configuration, logging, and session persistence placeholders.
- [x] Automated dependency-graph, entry-point, and circular-import verification.
- [x] Updated README with structure overview and validation commands.

## Acceptance Criteria

All criteria are satisfied:

- [x] All planned `src/bubblecraps` packages exist and are importable.
- [x] Root `main.py` and package `__main__.py` can be invoked without errors.
- [x] Session domain modules contain zero Qt imports.
- [x] Controller and GUI modules follow the dependency direction policy from Milestone 0.
- [x] The test suite is discoverable and passes under `pytest -v`.
- [x] The asset directory structure is preserved in git via `.gitkeep` files.

## Verification Checklist

Completed reviewer checklist:

- [x] Confirm all folders and modules match the structure defined in
  [docs/PAG-mini-v0.6.md](../PAG-mini-v0.6.md) project structure section.
- [x] Confirm `src/bubblecraps/session/state.py`, `history.py`, and the other session modules exist and are
  importable.
- [x] Confirm SessionController exists with placeholder signal definitions.
- [x] Confirm both entry points invoke the application bootstrap without bypassing it.
- [x] Confirm pytest discovers all test modules.
- [x] Run `python -m compileall -q main.py src/bubblecraps` to verify syntax.
- [x] Run `python tools/check.py`, including the automated architecture test.
- [x] Verify README contains a "Project Structure" section.

## Risks and Mitigations

Risk: Circular import dependencies introduced early.
- Mitigation: Use import verification test to catch early; enforce Milestone 0 policy strictly.

Risk: Missing stub classes cause later milestones to fail type checking.
- Mitigation: Ensure all referenced class names are defined as stubs even if empty.

Risk: Asset directories are not preserved in git.
- Mitigation: Use .gitkeep files in empty directories.

Risk: Incomplete module stubs lack necessary docstrings.
- Mitigation: Add module-level and class-level docstrings referencing PAG for future implementation guidance.

## Milestone 1 Exit Decision

**Decision: Pass.** All acceptance criteria are satisfied, all planned modules are importable, the
documented structure is present, and the Milestone 0 dependency boundaries remain enforced.

## Signoff Evidence

- Signoff date: 2026-07-31.
- Engine source: pinned sibling `crapssim` checkout at
  `a785b6a55e7f87b4302526ada30c5086be983574`.
- Package verification: `import bubblecraps` reports version
  `0.0.0-alpha.1.2026-07-31`.
- Entry points: root `main.py` and `python -m bubblecraps` both exit successfully through the
  application bootstrap.
- Architecture verification: runtime-layer boundaries, entry-point imports, and complete package
  imports pass automated tests.
- Session boundary: no Qt imports exist under `src/bubblecraps/session/`.
- Test result: 21 tests passed, including application, assets, controller, GUI, session,
  architecture, documentation, check-runner, and engine contract coverage.
- Quality gates: Ruff format passed, Ruff lint passed, strict first-party mypy passed, pytest passed,
  and `pip check` reported no broken requirements.
- Asset structure: every required directory is preserved with a tracked `.gitkeep` file.
- Scope audit: no gameplay rules, persistence implementation, controller behavior, GUI rendering,
  or asset-loading behavior was introduced.
- Handoff: Milestone 2 planning is captured in
  [milestone-2-domain-core-completion.md](milestone-2-domain-core-completion.md).
