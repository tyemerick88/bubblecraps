# Development Policy

## Environment Baseline

| Component | Baseline |
| --- | --- |
| Python | `>=3.14,<3.15` |
| Environment | Standard-library `venv` in `.venv` |
| Runtime source | Repository checkout; not packaged yet |
| Game engine | Published `crapssim` 0.4.1 package |
| GUI toolkit | PySide6 6.11.1 |
| Formatter and linter | Ruff 0.16.0 |
| Type checker | mypy 2.3.0, strict mode |
| Test runner | pytest 9.1.1 |

Bubble Craps supports Python `>=3.14,<3.15`, allowing any Python 3.14 patch release while excluding
future minor versions until they pass the complete quality suite. `.python-version` selects the
advisory local default; contributors may use another 3.14 patch release. Always verify with
`python --version` after activating the environment.

## Version Policy

Bubble Craps follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). During initial
milestone development, accepted work-package checkpoints use this prerelease format:

```text
0.0.0-alpha.<milestone_number>.<work_package_number>.<completion_date>
```

The milestone and work-package numbers are unpadded positive integers, and the completion date uses
`YYYY-MM-DD`. A work-package version is assigned only after its implementation and focused quality
gates pass. A completed milestone omits the work-package identifier and is assigned only after all
milestone acceptance criteria pass:

```text
0.0.0-alpha.<milestone_number>.<completion_date>
```

Until the first planned `0.1.0` release, the public API remains unstable and may change between
checkpoint versions.

The canonical runtime version is `bubblecraps.__version__`. Documentation, tests, release tags, and
future package metadata must agree with that value. Git tags may use the conventional `v` prefix,
but the semantic version value itself does not include `v`.

## Dependency Policy

Runtime dependencies belong in `requirements.txt`; development-only tools belong in
`requirements-dev.txt`. Every direct dependency uses an exact version. Add a dependency only when the
standard library and current dependencies do not reasonably solve the problem.

Bubble Craps uses the exact published `crapssim==0.4.1` release. This remains the engine version going
forward unless an engine change is strictly necessary for Bubble Craps. Any upgrade must be reviewed
as an explicit dependency change against the engine changelog and the complete Bubble Craps quality
and integration suite.

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

Mypy runs in strict mode for all first-party Python code. The published `crapssim` package is treated
as an external type-checking boundary because its typed implementation does not currently pass this
project's strict mypy settings. Runtime contract tests cover the engine APIs used here. Pytest
rejects unknown configuration options and markers.

Future CI must run the same commands on every pull request across the supported Python 3.14 range
and with the exact `crapssim` version in `requirements.txt`. CI automation itself is deferred, but
local commands are the contract it will execute.

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