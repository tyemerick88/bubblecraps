# Bubble Craps GUI Project Architecture Guide (PAG)

**Version:** 0.6

> Living architecture document for the Bubble Craps GUI application.
> Document is refered to as Project Architecture Guide (aka "PAG").

> Milestone sequencing note: The class responsibilities below describe the target application
> architecture. Milestone 2 implements only the domain subset defined in
> [Milestone 2: Domain Core Completion](milestones/milestone-2-domain-core-completion.md). Persistence
> and undo begin in Milestone 3, Qt integration begins in Milestone 4, and the Interblock Section 3.2
> Set Bets On/Off behavior is deferred to Milestone 6 pending a published engine update.

------------------------------------------------------------------------

# Project Overview

The goal of this project is to build a desktop **Bubble Craps**
application using **PySide6** while using **crapssim** as the game
engine.

Planned capabilities include:

-   Game Modes
    -   Regular Craps
    -   Crapless Craps
    -   Easy Craps (optional)
-   GUI Features
    -   Animated dice
    -   Interactive betting
    -   Animated Bet Win Total
    -   Realist Casino Bubble Craps Feel
-   Core Game Features (buttons)
    -   Roll
    -   Repeat Last Bet
    -   Double Bet
    -   Clear All Bets
    -   Set Bets On/Off
    -   Cashout
    -   etc.
-   Quality of Life Game Features
    -   Help Menu
    -   Settings Menu
    -   Save / Load
    -   Undo
    -   View Session Statistics
    -   Session Replay
    -   etc.

The GUI must never duplicate game rules implemented by `crapssim`.

------------------------------------------------------------------------

# Product Vision & Design Philosophy

## Vision

The primary objective of this project is to faithfully recreate the
experience of playing a modern casino bubble craps machine.

The application should feel immediately familiar to players who have
used a real bubble craps machine in a casino.

Whenever practical, the application should emulate the appearance,
pacing, interaction model, and overall user experience of a real
machine.

Authenticity is considered a *core* design goal rather than an optional
feature.

### Interblock Bubble Craps Machine Documentation

The bubblecraps program should look, feel and behave the same way the
Interblock documentation below describes. Use this PDF document as the source of truth
for all questions about how this program should work for all game modes.

https://wsgc.wa.gov/sites/default/files/2025-02/Craps_Crapless_Craps_Easy_Craps_game_description_Washington-specific_v2.5.1_0.pdf

## Guiding Principle

> Every deviation from a real casino bubble craps machine should be
> optional and should never alter the underlying rules of the game.

The `crapssim` engine remains the single source of truth for all game
rules. However, we may need to modify the `crapssim` project itself if
anything in the game engine divates for the Interblock game rules.

## Authenticity First

When making design decisions, authenticity takes precedence over
convenience.

Examples include:

-   Realistic table layout
-   Casino-style chip colors
-   Authentic puck behavior
-   Realistic dice animations
-   Casino-inspired sounds
-   Touchscreen-oriented interaction
-   Large betting areas


The goal is for the application to be visually recognizable as a casino
bubble craps machine, played on a desktop.

## Convenience Features

Convenience features are application-level capabilities rather than
gameplay modifications.

Examples include:

-   Save Session
-   Load Session
-   Undo
-   Auto Play
-   Strategy Playback
-   Session Statistics
-   Session Replay
-   Developer Tools

These features should remain optional and should never interfere with
authentic gameplay.

## User Interface Philosophy

The primary interface should resemble a dedicated casino gaming machine
rather than a traditional desktop application.

Design goals:

-   Single primary game screen
-   Direct interaction with the table
-   Minimal dialog windows
-   Minimal text input
-   Large touch-friendly controls
-   Immersive gameplay experience

Configuration, statistics and advanced tools should be presented as
secondary interfaces.

## Design Philosophy

Every architectural and user interface decision should support the
following objective:

> Create the most authentic bubble craps experience possible while
> providing optional convenience features that enhance usability without
> compromising gameplay authenticity.

-------------------------------------------------------------------------

# Overall Architecture

``` text
PySide6 GUI
      │
      ▼
SessionController (Qt)
      │
      ▼
GameSession (Pure Python)
      │
      ▼
crapssim
```

## Responsibilities

### PySide6

-   Render UI
-   Handle user interaction
-   Animations

### SessionController

-   Bridge between Qt and GameSession
-   Receive GUI commands
-   Emit Qt signals
-   No game rules

### GameSession

-   Own Player and Table
-   Maintain session history
-   Statistics
-   Undo (Milestone 3)
-   Save / Load (Milestone 3)
-   Produce immutable GameState

### crapssim

-   Game rules
-   Bets
-   Dice
-   Point
-   Player bankroll
-   Bet resolution

For Milestone 2, the required engine is the exact published `crapssim==0.4.1` package. Bubble Craps
uses only its public constructors, methods and attributes and does not depend on a sibling checkout.
If an Interblock requirement needs engine behavior that this release cannot express, the feature is
deferred until `crapssim` owns the behavior and publishes a new release.

------------------------------------------------------------------------

# Technology Decisions

## GUI

### [PySide6](https://pypi.org/project/PySide6/)

Reasons:
- Official Qt bindings
- Native desktop UI
- Excellent layouts
- Built-in animation support
- Cross-platform

## Game Engine

### [crapssim](https://github.com/skent259/crapssim)

All game rules remain inside the engine.

------------------------------------------------------------------------

# Project Structure

``` text
bubblecraps/
│
├── main.py
│
├── gui/
│
├── session/
│   ├── game_session.py
│   ├── state.py
│   ├── history.py
│   ├── statistics.py
│   ├── snapshot.py
│   └── settings.py
│
├── assets/
│   ├── chips/
│   ├── dice/
│   ├── table/
│   ├── puck/
│   ├── buttons/
│   ├── icons/
│   ├── fonts/
│   ├── sounds/
│   │   ├── dice/
│   │   ├── chips/
│   │   ├── ui/
│   │   └── payouts/
│   └── themes/
│
└── requirements.txt
```

This project structure section should be used as an example, rather than the
absolute final state; it is subject to change as required.

------------------------------------------------------------------------

# Psudo Code Design

## GameSession

Represents a single-player bubble craps session.

Owns:
- Table (crapssim)
- Player (crapssim), constructed with `NullStrategy` for interactive sessions
- History
- Statistics
- Settings
- Undo stack (Milestone 3, not constructed in Milestone 2)

Produces:
- GameState

Does not:
- Implement game rules
- Manage bankroll directly
- Know about PySide6

``` python
class GameSession:
    table: Table
    player: Player
    history: SessionHistory
    statistics: SessionStatistics
    settings: SessionConfiguation
    # Added in Milestone 3:
    undo_stack: list[SessionSnapshot]

    @property
    def state(self) -> GameState: ...

    def roll(self) -> CommandResult: ...
    def place_bet(self, request: BetRequest) -> CommandResult: ...
    def remove_bet(self, bet_id: str) -> CommandResult: ...
    def repeat_last_bet(self) -> CommandResult: ...
    def double_bet(self) -> CommandResult: ...
    def clear_all_bets(self) -> CommandResult: ...
    def set_bets_on_or_off(self, working: bool) -> CommandResult: ...
    def new_session(self) -> CommandResult: ...

    # Return NOT_IMPLEMENTED until their owning milestones:
    def undo(self) -> CommandResult: ...
    def save(self, filename: str) -> CommandResult: ...
    @classmethod
    def load(cls, filename: str): ...
```

Milestone 2 commands use stable generic outcomes: `ACCEPTED`, `REJECTED`, and `NOT_IMPLEMENTED`.
Published `crapssim==0.4.1` silently accepts or rejects player bet operations, so Bubble Craps must
not invent engine-specific rejection reasons. `set_bets_on_or_off` returns `NOT_IMPLEMENTED` until
Milestone 6 integrates the complete engine-owned Interblock Section 3.2 behavior.

---

### GameState

The GUI never determines whether an action is legal. Instead:

- GameSession computes the currently available actions.
- GameState exposes them.
- The GUI simply enables or disables controls.

``` python
@dataclass(frozen=True)
class GameState:
    phase: GamePhase
    actions: AvailableActions
    bankroll: float
    point: int | None
    puck_on: bool
    bets: tuple[BetState, ...]
    die1: int | None
    die2: int | None
    last_roll: RollRecord | None
    statistics: SessionStatisticsState
    history: SessionHistoryState
```

No Qt types, mutable engine objects, or mutable session containers belong in `GameState`. A frozen
outer dataclass is insufficient by itself: all nested values must also be detached and recursively
immutable. `BetState` is an application-owned descriptive projection built only from reviewed public
engine attributes; it does not contain a live `Bet` or encode game rules.

#### GamePhase

``` python
class GamePhase(Enum):
    READY="ready"
    ROLLING="rolling"
    RESOLVING="resolving"
    ANIMATING="animating"
```

#### AvailableActions

```python
@dataclass(frozen=True)
class AvailableActions:
    can_roll: bool
    can_place_bets: bool
    can_remove_bets: bool
    can_repeat_last_bet: bool
    can_double_bets: bool
    can_clear_bets: bool
    can_set_bets_on_or_off: bool
    can_undo: bool
    can_save: bool
    can_load: bool
```

Action flags are conservative permission to attempt a command, not guarantees that the engine will
accept it. Milestone 2 keeps `can_set_bets_on_or_off`, `can_undo`, `can_save`, and `can_load` false.

------------------------------------------------------------------------

### SessionSnapshot

> Milestone ownership: This is a Milestone 3 contract. Milestone 2 does not create
> `SessionSnapshot` values, capture snapshots, or maintain an undo stack.

A `SessionSnapshot` is an immutable checkpoint of the application's session state.

Its primary purpose is to support **Undo**, allowing the application to restore the session to a previous state as though the most recent user action never occurred.

Unlike `GameState`, which exists only to present information to the GUI, a `SessionSnapshot` represents the internal state required to restore a `GameSession`.

A `SessionSnapshot` is responsible for:

- Capturing the complete state of a `GameSession`.
- Providing an immutable checkpoint for Undo.
- Restoring the session after an Undo operation.
- Remaining independent of any GUI framework.

A `SessionSnapshot` is **not** responsible for:

- Rendering the user interface.
- Storing Qt objects.
- Managing animations.
- Representing application presentation state.

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class SessionSnapshot:
    """Immutable checkpoint of a GameSession."""
    engine_state: EngineSnapshot
    history: SessionHistoryState
    statistics: SessionStatisticsState
    settings: SessionConfiguration
```

The exact Milestone 3 snapshot representation must be able to restore engine state deterministically
without treating a frozen reference to a mutable `Player` or `Table` as immutable.

### GameState vs. SessionSnapshot

| Class | Purpose |
|--------|---------|
| `GameState` | Read-only view of the session used by the GUI. |
| `SessionSnapshot` | Complete checkpoint used to restore a previous `GameSession`. |

------------------------------------------------------------------------

### SessionConfiguation
```python
@dataclass(frozen=True)
class SessionConfiguration:
    ruleset: str
    table_settings: TableSettings # matches crapssim class
    casino_profile: str | None
    starting_bankroll: float
```

Milestone 2 accepts only `classic` and `crapless`, requires a finite positive bankroll, and constructs
the engine with its committed defaults. Custom `TableSettings` overrides and `casino_profile` are not
part of the Milestone 2 configuration contract.

------------------------------------------------------------------------

### SessionHistory
``` python
class SessionHistory:
    rolls: list[RollRecord]
    shooters: list[ShooterRecord]
    events: list[SessionEvent]

    def snapshot(self) -> SessionHistoryState: ...
```

`SessionHistory` is the internal append-only owner. Published state uses a recursively immutable
`SessionHistoryState` snapshot with tuple collections.

#### RollRecord
``` python
@dataclass(frozen=True)
class RollRecord:
    die1: int
    die2: int
    total: int
    timestamp: datetime
    shooter_number: int
    point_before: int | None
    point_after: int | None
    total_player_cash_delta: float
    bets_before: tuple[BetState, ...]
    bets_after: tuple[BetState, ...]
```

`RollRecord` is aggregate history. The before/after layouts are observations and must not be labeled
as per-bet wins, losses, pushes, moves, removal reasons, payouts, or attributable cash changes because
`crapssim==0.4.1` does not publish an authoritative per-bet settlement journal. Accepted player
commands may be recorded separately as player-command changes.
#### ShooterRecord
``` python
@dataclass(frozen=True)
class ShooterRecord:
    shooter_number: int
    rolls: int
    point_numbers_made: tuple[int, ...]
    profit: float
```

#### SessionEvent
```python
from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class SessionEventType(Enum):
    NEW_SESSION = "new_session"
    NEW_SHOOTER = "new_shooter"

    POINT_ESTABLISHED = "point_established"
    POINT_MADE = "point_made"
    SEVEN_OUT = "seven_out"

    UNDO = "undo"

    SESSION_SAVED = "session_saved"
    SESSION_LOADED = "session_loaded"


@dataclass(frozen=True)
class SessionEvent:
    """A significant event that occurred during a GameSession."""
    timestamp: datetime
    event_type: SessionEventType
    description: str
```

#### RollRecord vs SessionEvent

| Class | Purpose |
|--------|---------|
| `RollRecord` | Records every roll of the dice and its effects. |
| `SessionEvent` | Records significant milestones during the lifetime of the session. |

Milestone 2 reserves `UNDO`, `SESSION_SAVED`, and `SESSION_LOADED` for Milestone 3. Its minimum
statistics are total rolls, shooters started, points established, points made, seven-outs, and net
total-player-cash change from the configured starting bankroll. Statistics are derived from public
engine transitions and aggregate history, never by recalculating game outcomes.

------------------------------------------------------------------------

## SessionController

Bridge between Qt and GameSession

``` python
class SessionController(QObject):

    state_changed = Signal(GameState)

    session_loaded = Signal()
    session_saved = Signal()
    session_reset = Signal()

    @property
    def state(self): ...

    def roll(self): ...
    def undo(self): ...
    def new_session(self): ...
    def save(self, filename): ...
    def load(self, filename): ...
```

------------------------------------------------------------------------

# Lifecycles and Flows

## Application Lifecycle

``` text
Launch
 ↓
Load Settings
 ↓
Create GameSession
 ↓
Create MainWindow
 ↓
Bind SessionController
 ↓
Display GameState
 ↓
Qt Event Loop
```

------------------------------------------------------------------------

## Session Lifecycle

``` text
New Session
 ↓
Waiting For Bets
 ↓
Roll Requested
 ↓
Resolve Roll
 ↓
Update History
 ↓
Update Statistics
 ↓
Produce GameState
 ↓
Waiting For Bets
```

------------------------------------------------------------------------

## Roll Lifecycle

``` text
Roll Button
 ↓
SessionController.roll()
 ↓
GameSession.roll()
 ↓
crapssim.TableUpdate.run() exactly once
 ↓
Observe public engine state
 ↓
Append one aggregate RollRecord
 ↓
Update SessionStatistics exactly once
 ↓
Produce GameState
 ↓
GUI Animation
 ↓
READY
```

Animations never modify game state.

------------------------------------------------------------------------

## Undo Flow

> Milestone ownership: Undo is implemented in Milestone 3. Milestone 2 returns `NOT_IMPLEMENTED` and
> does not create snapshots or an undo stack.

Once Milestone 3 is implemented, every user action that modifies the session should create a
snapshot **before** any changes are made.

```text
User Action
      │
      ▼
Create SessionSnapshot
      │
      ▼
Modify GameSession
      │
      ▼
Produce new GameState
```

Undo performs the reverse operation.

```text
Undo
      │
      ▼
Restore SessionSnapshot
      │
      ▼
Rebuild GameSession
      │
      ▼
Produce new GameState
```

------------------------------------------------------------------------

## Event Flow

``` text
GUI
 ↓
SessionController
 ↓
GameSession
 ↓
crapssim
 ↓
GameSession
 ↓
GameState
 ↓
SessionController
 ↓
Qt Signal
 ↓
GUI
```

Event categories:

-   User Events
-   Game Events
-   UI Events
-   System Events

------------------------------------------------------------------------

# JSON File Spec

## Save State File

Extension with be `.bcs` rather than `.json`

```json
{
  "metadata": {
    "file_format": "bubble-craps-session",
    "file_version": 1,
    "application_version": "0.0.1",
    "ruleset": "crapless",
    "session_id": "9f237fe4-2a48-46b7-a4a5-26b6db6c89bb",
    "created_timestamp": "2026-07-04T03:15:42Z",
    "modified_timestamp": "2026-07-04T04:27:08Z"
  },
  "player": {},
  "table": {},
  "history": {
    "rolls": [],
    "shooters": [],
    "events": []
  },
  "statistics": {},
  "settings": {}
}
```

### Metadata Fields

| Field | Type | Format | Purpose |
|-------|------|--------|---------|
| `file_format` | `string` | Fixed identifier (e.g. `"bubble-craps-session"`) | Identifies the file type and allows the application to verify that the file is a valid Bubble Craps session file. |
| `file_version` | `integer` | Positive integer | Version of the save file format. Used to support backward compatibility and data migration as the format evolves. |
| `application_version` | `string` | Semantic Versioning (e.g. `"0.5.0"`) | Version of the Bubble Craps application that created or last saved the session. Primarily used for diagnostics and troubleshooting. |
| `ruleset` | `string` | Registered ruleset identifier (e.g. `"classic"`, `"crapless"`, `"high-point"`) | Specifies which `crapssim` ruleset should be used when restoring the session. This allows the correct game engine to be selected before deserializing session data. |
| `session_id` | `string` | UUID v4 | Globally unique identifier for the session. Remains constant for the lifetime of the session, even after multiple saves. |
| `created_timestamp` | `string` | ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`) | Timestamp indicating when the session was originally created. This value never changes after the initial save. |
| `modified_timestamp` | `string` | ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`) | Timestamp indicating when the session was most recently saved. Updated every time the session is written to disk. |

------------------------------------------------------------------------

## Configuation File

| Property | Value |
|-----------|-------|
| **Format** | JSON |
| **Extension** | `.json` |
| **Encoding** | UTF-8 |
| **Human Readable** | Yes |
| **Versioned** | Yes |
| **GUI State Stored** | Yes (persistent UI preferences only) |
| **Session Data Stored** | No |

### Example File

```json
{
  "metadata": {
    "file_format": "bubble-craps-config",
    "file_version": 1,
    "application_version": "0.1.0",
    "created_timestamp": "2026-07-04T03:15:42Z",
    "modified_timestamp": "2026-07-04T04:27:08Z"
  },

  "appearance": {},

  "audio": {},

  "gameplay": {},

  "developer": {}
}
```

### Configuration Storage

Application configuration should be stored in the operating system's standard user configuration directory.

Examples include:

- Windows: `%APPDATA%`
- macOS: `~/Library/Application Support`
- Linux: `~/.config`

The application should use Qt's `QStandardPaths` to locate the appropriate directory rather than hardcoding platform-specific paths.

If no configuration file exists, the application should automatically create one using the default configuration.

------------------------------------------------------------------------

# Application Logging

## Design Goals

The Bubble Craps application uses a centralized logging system to record application behavior, diagnose problems, and assist with debugging.

Logging is intended for application diagnostics rather than gameplay history.

Gameplay events are already represented by `SessionHistory`, `RollRecord`, and `SessionEvent`, and therefore should not be duplicated in the application log.

---

## Design Principles

The logging system should be:

- Reliable.
- Cross-platform.
- Low maintenance.
- Easy to configure.
- Helpful for troubleshooting.
- Independent of gameplay logic.

The logging system must never become the authoritative source of game history.

---

## Logging Responsibilities

The logging system is responsible for recording application behavior, including:

- Application startup and shutdown.
- Configuration loading and saving.
- Session loading and saving.
- Asset loading failures.
- Recoverable warnings.
- Unexpected exceptions.
- Internal application diagnostics.

The logging system is **not** responsible for recording:

- Dice rolls.
- Bet results.
- Session history.
- Player statistics.
- Gameplay events.

These are already represented by the application's session model.

---

## Logging Categories

### Application Logging

Records normal operation of the application.

Examples include:

- Application started
- Configuration loaded
- Session loaded
- Session saved
- Asset loaded
- Asset missing

This log is intended to assist with troubleshooting user issues.

---

### Developer Logging

Provides detailed diagnostic information intended for development.

Examples include:

- Rebuilding `GameState`
- Rendering `TableWidget`
- Loading Qt resources
- Animation state changes
- Signal emissions
- Internal application flow

Developer logging should normally be disabled unless Developer Mode is enabled.

---

### Crash Logging

Unexpected exceptions should be recorded automatically.

Crash logs should include:

- Timestamp
- Exception type
- Error message
- Stack trace

This information is intended to assist with debugging and bug reporting.

---

## Relationship to SessionHistory

The application intentionally separates gameplay history from application logging.

| Component | Responsibility |
|-----------|----------------|
| `RollRecord` | Records every dice roll. |
| `SessionEvent` | Records significant gameplay milestones. |
| `SessionHistory` | Maintains the complete gameplay history for the session. |
| `LoggingManager` | Records application behavior and diagnostics. |

This separation prevents duplication while keeping each component focused on a single responsibility.

---

## LoggingManager

The application uses a dedicated `LoggingManager` to configure and manage logging.

```text
Application
      │
      ▼
LoggingManager
      │
      ▼
Python logging
      │
      ▼
Rotating Log Files
```

`LoggingManager` is responsible for:

- Initializing the logging system.
- Configuring log levels.
- Configuring log destinations.
- Managing log rotation.
- Formatting log messages.
- Enabling developer logging.
- Recording unhandled exceptions.

The rest of the application should not configure the logging system directly.

---

## Logging Implementation

The application uses Python's built-in `logging` module.

Using the standard library avoids introducing additional dependencies while providing mature support for:

- Multiple log levels.
- Rotating log files.
- Multiple log handlers.
- Console logging.
- File logging.
- Custom formatting.

---

## Log Levels

The application follows the standard Python logging levels.

| Level | Purpose |
|--------|---------|
| `DEBUG` | Detailed developer diagnostics. |
| `INFO` | Normal application operation. |
| `WARNING` | Recoverable problems that do not prevent continued execution. |
| `ERROR` | Operations that failed but allow the application to continue running. |
| `CRITICAL` | Fatal errors that prevent normal application operation. |

During normal use, the application should log at the `INFO` level.

When Developer Mode is enabled, the application may automatically increase logging to the `DEBUG` level.

---

## Log Storage

Application logs should be stored using the operating system's standard application log location.

The application should use Qt's `QStandardPaths` to determine the appropriate location for each platform rather than hardcoding paths.

Log files should never be stored alongside save files or application configuration.

---

## Log Rotation

Log files should automatically rotate to prevent unbounded growth.

The application should use Python's `RotatingFileHandler` (or an equivalent implementation) to maintain a fixed number of historical log files.

Example:

```text
bubblecraps.log
bubblecraps.log.1
bubblecraps.log.2
bubblecraps.log.3
```

Older log files should be removed automatically according to the configured retention policy.

---

## Future Consideration: Diagnostic Reports

A future version of the application may provide a **Generate Diagnostic Report** feature.

The report could include:

- Application version.
- Operating system.
- Current configuration.
- Recent log entries.
- Recent exceptions.

This information would simplify bug reporting and troubleshooting while avoiding the need to manually locate log files.

---

## Design Philosophy

Application logs describe how the application behaves.

Gameplay history describes what happened during the game.

Keeping these concerns separate results in a cleaner architecture, avoids duplicate sources of information, and reinforces the project's guiding principle of maintaining clear separation between the application layer and the game model.

------------------------------------------------------------------------

# Asset Organization

## Goals

Assets include dice, chips, table artwork, puck images, buttons, icons,
fonts and sounds.

Assets should be organized by purpose rather than file type.

## Themes

A themes directory is reserved for future support even though only one
theme is planned initially.

## AssetManager

Widgets should never reference filenames directly.

Instead:

``` text
GUI Widgets
      │
      ▼
AssetManager
      │
      ▼
Qt Resources
```

Responsibilities:

-   Load images
-   Load sounds
-   Load fonts
-   Cache resources
-   Hide filenames
-   Support future themes

Avoid:

``` python
QPixmap("assets/chips/red25.png")
```

Prefer:

``` python
chip = AssetManager.chip(25)
dice = AssetManager.die_face(6)
sound = AssetManager.sound("dice_roll")
```

Example interface:

``` python
class AssetManager:

    def chip(self, denomination: int): ...
    def die_face(self, value: int): ...
    def puck(self): ...
    def table_background(self): ...
    def icon(self, name: str): ...
    def sound(self, name: str): ...
    def font(self, name: str): ...
```

The AssetManager provides a single abstraction between widgets and
physical resources, allowing assets to move to Qt's resource system
(.qrc) later without affecting the rest of the GUI.

------------------------------------------------------------------------

# IMPORTANT Final Considerations

-   Single source of truth is GameSession.
-   GameState is immutable.
-   GUI renders GameState.
-   SessionController isolates Qt from the application model.
-   AssetManager isolates widgets from resource storage.
-   GameSession remains pure Python.
-   crapssim owns all game rules.
