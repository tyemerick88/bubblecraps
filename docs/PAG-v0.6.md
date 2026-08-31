# Bubble Craps GUI Project Architecture Guide (PAG)

**Version:** 0.6

> Living architecture document for the Bubble Craps GUI application.
> Document is refered to as Project Architecture Guide (aka "PAG").

> Milestone sequencing note: The value contracts below describe the target domain architecture.
> Milestone 2 work is divided by the accepted
> [Milestone 2 plan](milestones/milestone-2-domain-core-completion.md). Persistence and undo begin in
> Milestone 3, Qt integration begins in Milestone 4, and Interblock Set Bets On/Off is deferred to
> Milestone 6 pending a published engine capability.

------------------------------------------------------------------------

# Project Overview

The goal of this project is to build a desktop **Bubble Craps**
application using **PySide6** while using **crapssim** as the game
engine.

Planned capabilities include:

-   Regular Craps
-   Crapless Craps
-   Easy Craps
-   Animated dice
-   Interactive betting
-   Session statistics
-   Strategy playback
-   Save / Load
-   Undo
-   Replace Previous Bets

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

Authenticity is considered a core design goal rather than an optional
feature.

## Interblock Bubble Craps Machine Documentation

The bubblecraps program should look, feel and behave the same way the
documentation below describes.

https://wsgc.wa.gov/sites/default/files/2025-02/Craps_Crapless_Craps_Easy_Craps_game_description_Washington-specific_v2.5.1_0.pdf

## Guiding Principle

> Every deviation from a real casino bubble craps machine should be
> optional and should never alter the underlying rules of the game.

The `crapssim` engine remains the single source of truth for all game
rules.

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
-   Replace Previous Bets button
-   Set Bets Off/On button


The goal is for the application to be visually recognizable as a casino
bubble craps machine.

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

## Future Consideration: Application Modes

### Player Mode

The default experience, designed to closely resemble a real casino
bubble craps machine.

### Developer Mode

Provides optional access to:

-   Strategy playback
-   Session replay
-   Detailed statistics
-   Debug information
-   Diagnostic tools

Application modes affect only the user interface and never the
underlying game rules.

## Design Philosophy

Every architectural and user interface decision should support the
following objective:

> Create the most authentic bubble craps experience possible while
> providing optional convenience features that enhance usability without
> compromising gameplay authenticity.

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
-   Undo
-   Save / Load
-   Produce immutable GameState

### crapssim

-   Game rules
-   Bets
-   Dice
-   Point
-   Player bankroll
-   Bet resolution

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

------------------------------------------------------------------------

# GameSession

Represents a single-player bubble craps session.

Owns:
- Table
- Player
- History
- Statistics
- Settings
- Undo stack

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
    # Retained as a future contract; initialized and used in Milestone 3.
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
    def undo(self) -> CommandResult: ...
    def save(self, filename: str) -> CommandResult: ...
    @classmethod
    def load(cls, filename: str): ...
```

Milestone 2 command outcomes are generic: `ACCEPTED`, `REJECTED`, and `NOT_IMPLEMENTED`. The engine
does not provide authoritative rejection reasons. Undo and persistence return `NOT_IMPLEMENTED` until
Milestone 3; Set Bets On/Off does so until Milestone 6.

------------------------------------------------------------------------

# GameState

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

No Qt types, mutable engine objects, or mutable session containers belong in `GameState`. WP2.2
implements this recursively immutable state model. Its rule-neutral bet projection is:

```python
@dataclass(frozen=True)
class BetState:
    bet_id: str
    bet_type: str
    amount: float
    number: int | None = None
```

WP2.4 defines the supported `bet_type` identifiers and public engine-to-projection mappings.

------------------------------------------------------------------------

# GamePhase

``` python
class GamePhase(Enum):
    READY="ready"
    ROLLING="rolling"
    RESOLVING="resolving"
    ANIMATING="animating"
```


------------------------------------------------------------------------

# AvailableActions

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

Milestone 2 keeps `can_set_bets_on_or_off`, `can_undo`, `can_save`, and `can_load` false.

## Design Motivation

GameState no longer exposes individual action booleans. Instead, all user actions are grouped into a dedicated immutable AvailableActions object.

The GUI never determines whether an action is legal. Instead:

- GameSession computes the currently available actions.
- GameState exposes them.
- The GUI simply enables or disables controls.

GamePhase answers **what the game is currently doing**.

AvailableActions answers **what the user is currently allowed to do**.

Separating these concepts keeps gameplay rules inside GameSession while allowing the GUI to remain a passive consumer of application state.

------------------------------------------------------------------------

# SessionSnapshot

> Milestone ownership: This is a Milestone 3 runtime contract. The shell retains the `undo_stack`
> annotation, but Milestone 2 does not initialize or use it and does not create snapshots.

A `SessionSnapshot` is an immutable checkpoint of the application's session state.

Its primary purpose is to support **Undo**, allowing the application to restore the session to a previous state as though the most recent user action never occurred.

Unlike `GameState`, which exists only to present information to the GUI, a `SessionSnapshot` represents the internal state required to restore a `GameSession`.

## Responsibilities

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

---

## SessionSnapshot Stub

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

The Milestone 3 representation must restore engine state deterministically; freezing references to a
mutable `Player` or `Table` does not make a snapshot immutable.

---

## Relationship to GameState

Although both `SessionSnapshot` and `GameState` are immutable, they serve different purposes.

| Class | Purpose |
|--------|---------|
| `GameState` | Read-only view of the session used by the GUI. |
| `SessionSnapshot` | Complete checkpoint used to restore a previous `GameSession`. |

`GameState` is recreated whenever the session changes.

`SessionSnapshot` exists only to restore the session after an Undo operation.

---

## Undo Flow

> This flow begins in Milestone 3. Milestone 2 returns `NOT_IMPLEMENTED` for undo.

Every user action that modifies the session should create a snapshot **before** any changes are made.

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

---

## JSON File Save State

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
| `ruleset` | `string` | Supported `Ruleset` value (`"classic"` or `"crapless"`) | Specifies which `crapssim` ruleset should be used when restoring the session. This allows the correct game engine to be selected before deserializing session data. |
| `session_id` | `string` | UUID v4 | Globally unique identifier for the session. Remains constant for the lifetime of the session, even after multiple saves. |
| `created_timestamp` | `string` | ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`) | Timestamp indicating when the session was originally created. This value never changes after the initial save. |
| `modified_timestamp` | `string` | ISO 8601 UTC (`YYYY-MM-DDTHH:MM:SSZ`) | Timestamp indicating when the session was most recently saved. Updated every time the session is written to disk. |

---

## Design Considerations

The architecture intentionally does not prescribe how a `SessionSnapshot` is created or restored.

Possible implementations include:

- Deep-copying the session.
- Serializing and deserializing the session.
- Constructing a dedicated immutable snapshot object.

The implementation strategy may change over time without affecting the overall architecture.

The only architectural requirement is that restoring a `SessionSnapshot` returns the `GameSession` to the exact state it was in when the snapshot was created.

---

## Design Philosophy

`SessionSnapshot` completes the application's state model.

- `GameSession` represents the live application state.
- `GameState` represents the current state presented to the GUI.
- `SessionSnapshot` represents an immutable checkpoint used to restore the application.

Keeping these responsibilities separate results in a cleaner architecture and ensures that presentation concerns remain isolated from session management.

------------------------------------------------------------------------

# Supporting Classes

## SessionConfiguation
```python
class Ruleset(StrEnum):
    CLASSIC = "classic"
    CRAPLESS = "crapless"


@dataclass(frozen=True)
class SessionConfiguration:
    ruleset: Ruleset
    starting_bankroll: float
    vig_paid_on_win: bool = True
```

External identifiers are parsed with `Ruleset(value)` so unsupported rulesets are rejected. Bubble
Craps uses fixed unrounded vig and does not expose the complete mutable engine `TableSettings` object.

## SessionHistory
``` python
class SessionHistory:
    rolls: list[RollRecord]
    shooters: list[ShooterRecord]
    events: list[SessionEvent]
```

Published state uses a detached snapshot:

```python
@dataclass(frozen=True)
class SessionHistoryState:
    rolls: tuple[RollRecord, ...] = ()
    shooters: tuple[ShooterRecord, ...] = ()
    events: tuple[SessionEvent, ...] = ()
```

## RollRecord
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

The layouts are aggregate observations. They must not be interpreted as authoritative per-bet wins,
losses, pushes, moves, removal reasons, payouts, or attributable cash changes because
`crapssim==0.4.1` publishes no per-bet settlement journal.
## ShooterRecord
``` python
@dataclass(frozen=True)
class ShooterRecord:
    shooter_number: int
    rolls: int
    point_numbers_made: tuple[int, ...]
    profit: float
```

## SessionEvent
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

SessionStatistics tracks cumulative statistics.

```python
@dataclass(frozen=True)
class SessionStatisticsState:
    total_rolls: int = 0
    total_shooters_started: int = 0
    points_established: int = 0
    points_made: int = 0
    seven_outs: int = 0
    net_total_player_cash_change: float = 0.0
```

SessionSnapshot supports undo.

SessionConfiguation stores immutable choices that define how a particular game session was created.

SessionEvent records notable events.

## SessionEvent vs RollRecord

A `SessionEvent` represents a significant milestone that occurs during the lifetime of a `GameSession`.

Unlike `RollRecord`, which records every dice roll, a `SessionEvent` records meaningful changes in the progression of the session.

Examples include:

- New Session
- New Shooter
- Point Established
- Point Made
- Seven Out
- Undo
- Session Saved
- Session Loaded

These events provide a high-level timeline of the session and may be used for history displays, debugging, statistics, replay, and future analytics.

### Relationship to RollRecord

Although both classes represent historical information, they serve different purposes.

| Class | Purpose |
|--------|---------|
| `RollRecord` | Records every roll of the dice and its effects. |
| `SessionEvent` | Records significant milestones during the lifetime of the session. |

Every roll produces a `RollRecord`.

Only noteworthy moments produce a `SessionEvent`.

For example:

```text
Roll 1
↓
RollRecord
```

```text
Point Established
↓
SessionEvent
```

```text
Seven Out
↓
RollRecord
+
SessionEvent
```

------------------------------------------------------------------------

# BetState

`BetState` is a detached, recursively immutable Bubble Craps projection built only from approved
public engine attributes. WP2.4 defines its fields and constructor mappings. Runtime state never
publishes live `crapssim.Bet` objects.

------------------------------------------------------------------------

# Application Lifecycle

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

# Session Lifecycle

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

# Roll Lifecycle

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

# New Session

Creates a new Player, Table, History, Statistics, Undo stack and initial
GameState.

# Undo

Restores the previous SessionSnapshot and rebuilds GameState.

# Save / Load

Serializes or deserializes the GameSession.

------------------------------------------------------------------------

# Event Flow

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

# SessionController

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

# BetChange

``` python
@dataclass(frozen=True)
class BetChange:
    action: BetAction
    bet: Bet
    reason: BetChangeReason
```

``` python
class BetAction(Enum):
    ADDED="added"
    REMOVED="removed"
    WON="won"
    LOST="lost"
    TURNED_ON="turned_on"
    TURNED_OFF="turned_off"
```

``` python
class BetChangeReason(Enum):
    PLAYER="player"
    ROLL_RESULT="roll_result"
    UNDO="undo"
    LOAD="load"
```

------------------------------------------------------------------------

# Replace Previous Bets

Only restores bets affected by the immediately preceding roll.

Flow:

``` text
Replace Previous Bets
 ↓
SessionController
 ↓
GameSession
 ↓
history.rolls[-1]
 ↓
Eligible BetChanges
 ↓
Recreate Bets
 ↓
Produce GameState
 ↓
GUI Refresh
```

Eligibility: - Most recent roll only - Caused by roll result - Still
legal under current game state

------------------------------------------------------------------------

# Application Configuration

## Design Goals

Application configuration stores persistent user preferences that control how the application behaves across all sessions.

Configuration is intentionally separate from session save files.

A saved session represents **what game is being played**, while application configuration represents **how the application behaves**.

Examples of application configuration include:

- Theme
- Sound volume
- Animation speed
- Window layout
- Developer Mode

These preferences apply regardless of which session is currently loaded.

---

# Design Principles

Application configuration should be:

- Human-readable.
- Easy to edit.
- Easy to debug.
- Versioned.
- Backward compatible whenever practical.
- Independent of saved game sessions.

Configuration must never modify the rules of craps.

---

# Session vs Configuration

The application distinguishes between session data and configuration.

| Session Data | Application Configuration |
|--------------|---------------------------|
| Current bankroll | Theme |
| Active bets | Window layout |
| Roll history | Sound volume |
| Statistics | Animation speed |
| Table state | Developer Mode |
| Session history | Auto-save preferences |

Session data is stored in a `.bcs` session file.

Application configuration is stored independently and applies to every session.

---

# Configuration File Specification

| Property | Value |
|-----------|-------|
| **Format** | JSON |
| **Extension** | `.json` |
| **Encoding** | UTF-8 |
| **Human Readable** | Yes |
| **Versioned** | Yes |
| **GUI State Stored** | Yes (persistent UI preferences only) |
| **Session Data Stored** | No |

---

# Example Configuration File

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

---

# Configuration Categories

## Appearance

Controls the visual presentation of the application.

Examples:

- Theme
- Fullscreen mode
- Window size
- Window position
- High DPI options

---

## Audio

Controls application sound.

Examples:

- Master volume
- Effects volume
- Mute

---

## Gameplay

Controls convenience features without affecting game rules.

Examples:

- Animation speed
- Confirm New Session
- Auto-save
- Remember last ruleset
- Automatically replace previous bets (optional)

These settings affect only the user experience.

They must never modify the underlying game rules implemented by `crapssim`.

---

## Developer

Controls optional tools intended for development and debugging.

Examples:

- Developer Mode
- Debug overlays
- Verbose logging
- Animation diagnostics
- Hitbox visualization

These settings should not be visible during normal gameplay unless Developer Mode is enabled.

---

# ConfigurationManager

The application uses a dedicated `ConfigurationManager` to manage application configuration.

```text
Application
      │
      ▼
ConfigurationManager
      │
      ▼
Configuration
      │
      ▼
config.json
```

`ConfigurationManager` is responsible for:

- Loading configuration.
- Saving configuration.
- Creating default configuration.
- Validating configuration.
- Migrating older configuration versions.

The rest of the application should never read or write the configuration file directly.

---

# Configuration Stub

```python
@dataclass(frozen=True)
class Configuration:
    """Immutable application configuration."""
    appearance: AppearanceConfiguration
    audio: AudioConfiguration
    gameplay: GameplayConfiguration
    developer: DeveloperConfiguration
```

```python
class ConfigurationManager:
    """Loads, validates, and persists application configuration."""

    @property
    def configuration(self) -> Configuration:
        ...

    def load(self):
        ...

    def save(self):
        ...

    def reset_to_defaults(self):
        ...
```

---

# Configuration Storage

Application configuration should be stored in the operating system's standard user configuration directory.

Examples include:

- Windows: `%APPDATA%`
- macOS: `~/Library/Application Support`
- Linux: `~/.config`

The application should use Qt's `QStandardPaths` to locate the appropriate directory rather than hardcoding platform-specific paths.

If no configuration file exists, the application should automatically create one using the default configuration.

---

# Relationship to SessionConfiguation

Application configuration is distinct from `SessionConfiguation`.

Application configuration stores persistent user preferences that apply across every session.

`SessionConfiguation` (if retained) should contain only settings that are intended to be saved as part of an individual session.

This separation prevents saved sessions from changing a user's personal application preferences.

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

## Relationship to Session History

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

# Design Philosophy

-   Single source of truth is GameSession.
-   GameState is immutable.
-   GUI renders GameState.
-   SessionController isolates Qt from the application model.
-   AssetManager isolates widgets from resource storage.
-   GameSession remains pure Python.
-   crapssim owns all game rules.
