# Bubble Craps

Bubble Craps is a PySide6 desktop application intended to recreate an authentic casino bubble craps
experience. It uses [crapssim](https://github.com/skent259/crapssim) as the only game-rules engine.

**Milestone 1: Architecture Skeleton is complete.** The repository now has importable application,
session, controller, GUI, and asset shells while preserving the architecture, environment, and
executable quality checks established in Milestone 0. Gameplay, persistence, resource loading, and
GUI rendering remain future work.

Current version: `0.0.0-alpha.1.2026-07-31`

## Versioning

Bubble Craps follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). Until all
planned milestones are complete and version `0.1.0` is released, milestone completion versions use
this prerelease format:

```text
0.0.0-alpha.<milestone_number>.<completion_date>
```

- `milestone_number` is the completed roadmap milestone without leading zeroes.
- `completion_date` uses the ISO calendar form `YYYY-MM-DD`.
- The version core remains `0.0.0` during milestone development.
- The `alpha` prerelease label indicates that the public API is unstable and may change.
- A milestone version is assigned only when that milestone satisfies its acceptance criteria.

For example, Milestone 1 completed on July 31, 2026 is
`0.0.0-alpha.1.2026-07-31`. The first planned release after all roadmap milestones are complete is
`0.1.0`.

## Requirements

- Git
- Python 3.14.6
- A local checkout of `crapssim` beside this repository

Bubble Craps requires unreleased Crapless support from the local engine source. The two repositories
must have this layout:

```text
workspace/
├── bubblecraps/
└── crapssim/
```

This sibling-checkout requirement is temporary. Bubble Craps v0.1.0 will first be completed and
validated against the pinned checkout so application development can reveal any engine changes it
still needs. Once that behavior is stable, the project will request crapssim v0.5.0, replace the
editable checkout with `crapssim==0.5.0`, and rerun the complete integration suite before releasing
Bubble Craps v0.1.0. Contributors should not assume the sibling layout will remain required after
crapssim v0.5.0 is available.

## Clean Setup

Clone both repositories into one parent directory:

```bash
mkdir bubblecraps-workspace
cd bubblecraps-workspace
git clone https://github.com/skent259/crapssim.git
git clone https://github.com/tyemerick88/bubblecraps.git
git -C crapssim checkout --detach "$(cat bubblecraps/.crapssim-revision)"
cd bubblecraps
```

In Windows PowerShell, use this checkout command instead of the Bash command substitution above:

```powershell
git -C crapssim checkout --detach (Get-Content bubblecraps/.crapssim-revision)
```

Create and activate the virtual environment on macOS or Linux:

```bash
python3.14 -m venv .venv
source .venv/bin/activate
```

On Windows PowerShell:

```powershell
py -3.14 -m venv .venv
.venv\Scripts\Activate.ps1
```

Verify the exact interpreter and install the development environment:

```bash
python --version
python -m pip install --upgrade pip==26.2
python -m pip install -r requirements-dev.txt
python -m pip check
```

`python --version` must report `Python 3.14.6`. The requirements install `../crapssim` in editable
mode, so committed changes in the sibling checkout are immediately available without reinstalling.

## Run Status

Milestone 1 provides non-functional application entry points. The bootstrap currently exits
successfully without creating a GUI, game session, or persisted state:

```bash
python main.py
PYTHONPATH=src python -m bubblecraps
```

Validate the importable package from the repository checkout by exposing the `src` root first:

```bash
export PYTHONPATH=src
python -c 'import bubblecraps; print(bubblecraps.__version__)'
```

## Project Structure

The Milestone 1 source layout separates runtime responsibilities by the architecture contract:

```text
main.py                         # Thin application entry point
src/bubblecraps/
├── application/                # Bootstrap, preferences, and diagnostics ownership
├── assets/                     # Semantic AssetManager interface
├── controller/                 # Qt SessionController bridge
├── gui/                        # Window, table, animation, and style shells
└── session/                    # Pure-Python session models and orchestration boundary
assets/                         # Physical images, fonts, sounds, and themes
tests/                          # Import, contract, and architecture checks
```

The dependency direction is `application -> gui -> controller -> session -> crapssim`, with GUI
asset access flowing through `bubblecraps.assets.AssetManager`. The session layer has no Qt
dependency. See the [Project Architecture Guide](docs/PAG-mini-v0.6.md) and the
[architecture contract](docs/architecture-contract.md) for the authoritative boundaries.

Confirm that the required unreleased Crapless engine is active:

```bash
python -c "from crapssim.rules import CraplessRules; print(CraplessRules().point_numbers())"
```

Expected output:

```text
[2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
```

## Development Commands

Run all quality gates from the repository root with `.venv` active:

```bash
python tools/check.py
```

The runner streams each command's output live, preserves native tool colors when attached to a
terminal, labels each output block, continues after failures, and ends with a plain-text error
summary. It exits with status 1 when any gate fails. Color can be controlled explicitly:

```bash
python tools/check.py --color     # Force color, including redirected output
python tools/check.py --no-color  # Disable color
NO_COLOR=1 python tools/check.py  # Standard environment opt-out
```

The script runs these commands in order:

```bash
python -m ruff format --check .
python -m ruff check .
python -m mypy .
python -m pytest
python -m pip check
```

Apply formatting with:

```bash
python -m ruff format .
```

Ruff owns formatting, linting, and import sorting. Its settings follow the Google Python Style Guide
and Google-style docstrings as closely as practical while retaining Black-compatible 88-character
formatting for contributors who also work on crapssim. See [CONTRIBUTING.md](CONTRIBUTING.md) for the
enforced rules and documented exceptions.

The tests also verify that `../crapssim` is at the revision recorded in `.crapssim-revision`, has no
staged, unstaged, or untracked package and packaging changes, and provides the expected Crapless
rules API. Unrelated untracked files outside those engine paths do not fail this check.

## Updating crapssim

Until crapssim v0.5.0 is released, treat an engine revision change as a reviewed dependency update:

1. Make and test the rule change in `../crapssim`.
2. Commit the engine change; do not depend on an uncommitted working tree.
3. Replace `.crapssim-revision` with the full output of `git -C ../crapssim rev-parse HEAD`.
4. Reinstall only if engine packaging metadata or dependencies changed.
5. Run every Bubble Craps quality gate.

Never copy engine logic into this repository to avoid advancing the dependency. If required behavior
is absent or differs from the Interblock specification, fix it in `crapssim` first.

### Transition to crapssim v0.5.0

Do not request or adopt the engine release merely because its current unreleased work is usable. The
local checkout remains intentional while Bubble Craps v0.1.0 is being completed, because integration
work may expose additional rule-engine changes that belong in crapssim v0.5.0.

When Bubble Craps v0.1.0 is feature-complete and its engine contract is stable:

1. Ensure every required engine change is committed and validated in crapssim.
2. Request the crapssim v0.5.0 release.
3. Replace `-e ../crapssim` with the exact registry pin `crapssim==0.5.0`.
4. Remove the sibling-revision setup and checks that are no longer applicable.
5. Recreate the Bubble Craps environment and run every quality and integration gate.
6. Release Bubble Craps v0.1.0 only after the published package passes those checks.

## Project Documentation

- [Project Architecture Guide, mini v0.6](docs/PAG-mini-v0.6.md)
- [Architecture contract](docs/architecture-contract.md)
- [Development and quality policy](docs/development.md)
- [Roadmap](docs/roadmap.md)
- [Milestone 0 specification](docs/milestones/milestone-0-foundation-and-guardrails.md)

The architecture contract is mandatory for implementation and review. In particular, Qt types never
enter the session layer, GUI code never bypasses the controller, and `crapssim` remains the single
source of game-rule behavior.
