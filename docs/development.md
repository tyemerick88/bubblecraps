# Development Policy

## Environment Baseline

| Component | Baseline |
| --- | --- |
| Python | 3.14.6 |
| Environment | Standard-library `venv` in `.venv` |
| Runtime source | Repository checkout; not packaged yet |
| Game engine | Editable sibling checkout at `../crapssim` until v0.5.0 |
| Engine revision | Value in `.crapssim-revision` until v0.5.0 |
| GUI toolkit | PySide6 6.11.1 |
| Formatter and linter | Ruff 0.16.0 |
| Type checker | mypy 2.3.0, strict mode |
| Test runner | pytest 9.1.1 |

Python is fixed to one patch release so local development and future CI use the same language
features and standard-library behavior. `.python-version` is advisory for version managers; always
verify with `python --version` after activating the environment.

## Dependency Policy

Runtime dependencies belong in `requirements.txt`; development-only tools belong in
`requirements-dev.txt`. Every direct dependency uses an exact version. Add a dependency only when the
standard library and current dependencies do not reasonably solve the problem.

`crapssim` is a temporary, intentional exception to registry version pinning because Bubble Craps
requires unreleased Crapless support. The editable sibling checkout is pinned operationally by
`.crapssim-revision` and verified by tests. A change to that file is a dependency update and must be
reviewed with the corresponding engine changelog and Bubble Craps integration tests.

Keep this workflow until Bubble Craps v0.1.0 is feature-complete. Application integration is expected
to validate the new engine API and may identify corrections that should be included in crapssim
v0.5.0. Delaying the engine release avoids publishing successive engine versions solely to finish the
first Bubble Craps release.

Do not copy, vendor, or patch `crapssim` rules inside this repository. Make engine changes in the
sibling repository, commit them, then advance `.crapssim-revision` in a dedicated change.

### Engine Release Transition

Once the Bubble Craps v0.1.0 engine contract is stable, request crapssim v0.5.0. After it is
published, replace the editable requirement with `crapssim==0.5.0`, remove the local-revision guard
and sibling-checkout setup, recreate the environment, and run the full quality and integration suite.
Bubble Craps v0.1.0 must not be released while it still depends on an unpublished local checkout.

This changes only how the engine is installed. `crapssim` remains the sole owner of game rules after
the transition, and future engine versions remain exact direct dependencies under the normal pinning
policy.

Until a cross-platform lock file is introduced, exact direct pins are the compatibility baseline;
transitive packages may receive resolver-compatible updates. Before a release candidate, generate
and commit a platform-aware lock using the dependency workflow selected at that milestone.

## Quality Gates

Run the quality-gate script from the repository root with `.venv` active:

```bash
python tools/check.py
```

The script streams command output as it is produced, preserves each tool's native ANSI colors when
stdout is a terminal, labels each block, runs every check even when an earlier check fails, prints an
ANSI-free bounded error summary, and exits nonzero if any command fails. Use `--color` to force color
or `--no-color` to disable it; automatic mode also honors the standard `NO_COLOR` environment
variable. It is the convenience entry point for these authoritative commands:

```bash
python -m ruff format --check .
python -m ruff check .
python -m mypy .
python -m pytest
python -m pip check
```

All commands must exit successfully. Warnings from a tool are failures when that tool returns a
nonzero status; lint suppressions and type ignores require a narrow reason at the affected line.

### Python Style and Ruff

Project Python should follow the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
and Google-style docstrings as closely as Ruff can enforce them. Ruff is the sole formatter, linter,
and import sorter. Its configuration is the mechanical authority when a written convention is
ambiguous.

Ruff formats at 88 characters with double quotes. The width intentionally matches Black's default so
contributors moving between Bubble Craps and crapssim see minimal formatting churn; it is a
documented exception to Google's general 80-character preference. Ruff's Google docstring convention
applies to production code. Tests are exempt from mandatory docstrings but retain all other lint
rules. Documentation is excluded to preserve historical code examples in the PAG.

Linting covers annotations, unused arguments, bug risks, comprehensions, complexity, Google-style
docstrings, import sorting, naming, performance, Pylint-derived checks, pathlib usage, return flow,
simplification, and Python-version upgrades. McCabe complexity is capped at 10, and Pylint-derived
limits are explicit in `pyproject.toml`. These checks approximate the automatable parts of Google
style; reviewers still own design clarity that static tools cannot assess. See
[CONTRIBUTING.md](../CONTRIBUTING.md) for examples and contributor expectations.

Mypy starts in strict mode for all first-party Python code. The local `crapssim` checkout is treated
as an external type-checking boundary because its current `py.typed` source does not pass this
project's strict settings; runtime contract tests cover the APIs used here. Pytest rejects unknown
configuration and markers.

Future CI must run the same commands on every pull request using Python 3.14.6 and the recorded
`crapssim` revision. CI automation itself is deferred, but local commands are the contract it will
execute.

## Commit Policy

Contributor commits follow the Conventional Commits subset defined in
[CONTRIBUTING.md](../CONTRIBUTING.md). Commit subjects communicate change category and optional
architectural ownership; bodies record motivation and tradeoffs when the subject is insufficient.
The policy is review-enforced during the initial milestones. Automated commit-message validation may
be added with CI if inconsistent history becomes a recurring problem.

## Test Policy

- New domain or orchestration behavior requires focused tests for success, failure, and state
  transition behavior.
- Every bug fix includes a regression test that fails before the fix.
- Game-rule expectations are tested at the `crapssim` integration boundary; rule algorithms remain
  in the engine's own suite.
- Controller tests verify commands, legal-action gating, and signal emission without relying on GUI
  rendering.
- Persistence tests verify version rejection, round trips, and deterministic undo restoration.
- GUI tests focus on state rendering and interaction wiring; animations never serve as evidence that
  domain state changed.
- Tests must be deterministic. Random engine behavior uses explicit seeds or controlled dice.

Coverage percentages are not a milestone 0 gate. Risk-based behavior coverage is required now; a
numeric threshold may be introduced after the milestone 1 skeleton establishes measurable modules.

## Milestone 1 Handoff

Milestone 1 should create only importable shells for these planned modules:

| Package | Initial modules |
| --- | --- |
| `application` | `bootstrap.py`, `configuration.py`, `logging.py` |
| `assets` | `asset_manager.py` |
| `controller` | `session_controller.py` |
| `gui` | `main_window.py` |
| `session` | `game_session.py`, `history.py`, `persistence.py`, `settings.py`, `snapshot.py`, `state.py`, `statistics.py` |

Each package receives `__init__.py`; `main.py` is the process entry point; tests mirror package names
under `tests/`. Stubs expose signatures and ownership without implementing gameplay, persistence, or
GUI behavior. The architecture test must still pass after every skeleton module is introduced.