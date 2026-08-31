# Bubble Craps

Bubble Craps is a PySide6 desktop application intended to recreate an authentic casino bubble craps
experience. It uses [crapssim](https://github.com/skent259/crapssim) as the only game-rules engine.

**Milestone 2 implementation is underway.** WP2.1-WP2.4 establish the reconciled domain contracts,
immutable state projections, validated Classic and Crapless session setup, and the approved public
bet adapter. Gameplay orchestration, persistence, controller wiring, and GUI rendering remain future
work.

Current version: `0.0.0-alpha.2.4.2026-08-31`

## Versioning

Bubble Craps follows [Semantic Versioning 2.0.0](https://semver.org/spec/v2.0.0.html). Until all
planned milestones are complete and version `0.1.0` is released, accepted work-package checkpoints
use this prerelease format:

```text
0.0.0-alpha.<milestone_number>.<work_package_number>.<completion_date>
```

- `milestone_number` is the completed roadmap milestone without leading zeroes.
- `work_package_number` is the accepted work package within that milestone without leading zeroes.
- `completion_date` uses the ISO calendar form `YYYY-MM-DD`.
- The version core remains `0.0.0` during milestone development.
- The `alpha` prerelease label indicates that the public API is unstable and may change.
- A work-package version is assigned only after that package's implementation and focused quality
  gates pass.

When a complete milestone satisfies all acceptance criteria, its release omits the work-package
identifier:

```text
0.0.0-alpha.<milestone_number>.<completion_date>
```

For example, Milestone 1 completed on July 31, 2026 is
`0.0.0-alpha.1.2026-07-31`, while WP2.1 completed on August 26, 2026 is
`0.0.0-alpha.2.1.2026-08-26`. The first planned release after all roadmap milestones are complete is
`0.1.0`.

## Requirements

- Git
- Python `>=3.14,<3.15`
- skent259/crapssim [0.4.1](https://github.com/skent259/crapssim/releases/tag/v0.4.1)

Bubble Craps installs the published `crapssim==0.4.1` package as its game engine. This remains the
engine version going forward unless an engine change is strictly necessary.

## Clean Setup

Clone the Bubble Craps repository:

```bash
git clone https://github.com/tyemerick88/bubblecraps.git
cd bubblecraps
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

Verify the interpreter and install the development environment:

```bash
python --version
python -m pip install --upgrade pip==26.2
python -m pip install -r requirements-dev.txt
python -m pip check
```

`python --version` must report a Python 3.14 patch release. The requirements install the exact
published `crapssim` engine version used by the project.

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

The tests verify that the installed engine is exactly `crapssim==0.4.1`, came from a published
package rather than a local or VCS source, and provides the expected Crapless rules API.

## Project Documentation

- [Project Architecture Guide, mini v0.6](docs/PAG-mini-v0.6.md)
- [Architecture contract](docs/architecture-contract.md)
- [Development and quality policy](docs/development.md)
- [Roadmap](docs/roadmap.md)
- [Milestone 0 specification](docs/milestones/milestone-0-foundation-and-guardrails.md)

The architecture contract is mandatory for implementation and review. In particular, Qt types never
enter the session layer, GUI code never bypasses the controller, and `crapssim` remains the single
source of game-rule behavior.
