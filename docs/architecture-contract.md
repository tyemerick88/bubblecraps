# Architecture Contract

- Status: Accepted
- Contract version: 1
- Architecture source: [PAG mini v0.6](PAG-mini-v0.6.md)
- Applies from: Milestone 0

## Purpose

This contract turns the Project Architecture Guide into rules that can be checked during
implementation and review. A change that cannot obey this contract must update the contract and the
PAG deliberately; convenience is not an implicit exception.

## Sources of Truth

The project uses the following authorities, in order:

1. The Interblock game description referenced by the PAG defines intended game behavior.
2. `crapssim` implements game rules, bet legality, dice resolution, payouts, points, and bankroll
   effects, except for the explicitly reviewed Bubble Craps product-surface availability filter.
3. The PAG defines Bubble Craps product and application architecture.
4. This contract defines package ownership and dependency direction.

When `crapssim` differs from the intended Interblock behavior, fix or extend `crapssim` and consume
that change here. Bubble Craps must not compensate by implementing a second rules engine in its
session, controller, or GUI code.

The sole current exception is the fixed Classic/Crapless availability matrix in
[Bet Adapter Contract](bet-adapter-contract.md). The pinned engine permits Lay, Big 6, and Big 8 in
Crapless because these bets are available at some live Crapless tables. The adapter may reject
Interblock-unavailable identifiers before construction, but may not duplicate amount, timing,
parent-bet, bankroll, removability, payout, or settlement legality. Any broader exception requires
an explicit contract review.

The required engine is the exact published `crapssim==0.4.1` package. Bubble Craps will use this
version going forward unless an engine change is strictly necessary. Any necessary engine change
must be made and released by the `crapssim` project, then consumed here as a reviewed exact-version
dependency update that passes the complete quality and integration suite. This release policy does
not permit game rules to move into Bubble Craps.

## Runtime Layers

```text
main.py
   |
   v
application (composition root)
   |-----------------------|
   v                       v
gui -----------------> controller
 |                       |
 v                       v
assets                  session
                           |
                           v
                       crapssim
```

Arrows mean "may import." Standard-library dependencies are omitted. Tests may import any runtime
layer for verification but may not become a runtime dependency.

### `application`

Owns process startup, shutdown, application configuration, centralized logging, and construction of
the concrete runtime object graph. It is the only composition root and may import the other runtime
packages to wire them together.

It must not implement game rules, resolve bets, mutate `crapssim` objects directly, or become a
general-purpose shared package.

### `session`

Owns `GameSession`, immutable GUI-facing state, session history, statistics, snapshots, session
configuration, persistence models, and orchestration of `crapssim`.

It may import the Python standard library and `crapssim`. It must remain usable without a Qt
installation: no `PySide6`, controller, GUI, application, or asset imports are allowed. All session
mutations enter through `GameSession`; every state-changing action will take its undo snapshot before
mutation once undo is implemented.

### `controller`

Owns `SessionController`, Qt signals and slots, command forwarding, action gating, and translation of
domain failures into stable controller outcomes.

It may import `session` and `PySide6`. It must not import GUI widgets, application startup code,
assets, or `crapssim`. It never computes game outcomes or bypasses `GameSession` to mutate engine
objects.

### `gui`

Owns windows, widgets, layouts, animation, visual state, and user interaction. It renders controller
state and forwards user intent through controller commands.

It may import `controller`, `assets`, and `PySide6`. It must not import `session` or `crapssim`, infer
whether actions are legal, calculate payouts, change bankrolls, or let animation mutate game state.
Control enablement comes only from `AvailableActions` exposed through the controller.

### `assets`

Owns `AssetManager`, resource lookup, loading, caching, and the mapping from semantic asset names to
physical files or Qt resources. It may use `PySide6` where required to construct presentation
resources.

It must not import application, session, controller, GUI, or `crapssim`. Widgets request semantic
assets from `AssetManager`; they never hardcode paths to physical assets.

## Import Policy

Allowed examples:

```python
# controller/session_controller.py
from bubblecraps.session.game_session import GameSession
from PySide6.QtCore import QObject, Signal

# session/game_session.py
from crapssim import Player, Table

# gui/main_window.py
from bubblecraps.assets.asset_manager import AssetManager
from bubblecraps.controller.session_controller import SessionController
```

Forbidden examples:

```python
# session/state.py: Qt cannot enter the domain/session layer.
from PySide6.QtCore import QObject

# gui/table_widget.py: GUI cannot bypass the controller.
from bubblecraps.session.game_session import GameSession

# controller/session_controller.py: only GameSession may orchestrate the engine.
from crapssim import Table
```

Type-checking imports follow the same policy. `TYPE_CHECKING` is not a boundary exception. Put shared
domain types in `session` and expose them to the GUI through the controller's public interface.

## State and Mutation Rules

- `GameSession` is the single source of truth for a live session.
- `GameState` and `AvailableActions` are immutable values produced by `GameSession`.
- The controller publishes state but does not maintain a competing state model.
- The GUI renders published state and does not optimistically mutate domain state.
- `crapssim` remains authoritative for rules and resolution; session code coordinates it and records
  resulting history and statistics.
- Application diagnostics and gameplay history remain separate. Logs are never used to reconstruct
  a session.
- Saved sessions and application preferences are separate formats with separate ownership.

## Repository Ownership

Milestone 1 will use a `src` layout:

```text
main.py
src/bubblecraps/
    application/
    assets/
    controller/
    gui/
    session/
tests/
```

Packages and modules use lowercase `snake_case`; classes use `PascalCase`; tests are named
`test_<behavior>.py`. Avoid generic `common`, `helpers`, or `utils` modules. Place code in the package
that owns the behavior, and add a focused abstraction only when ownership cannot otherwise be stated
clearly.

Physical images, fonts, and sounds will live outside Python modules under the repository-level
`assets/` tree. Access to them still flows through `bubblecraps.assets.AssetManager`.

## Enforcement

`tests/test_architecture.py` checks forbidden imports with Python's AST. The guard is intentionally
active before the runtime package exists and begins checking each layer as files are added.

Reviewers must also reject behavioral boundary violations that imports alone cannot detect, including
duplicated payout logic, GUI action inference, direct engine mutation outside `GameSession`, and asset
path literals in widgets.