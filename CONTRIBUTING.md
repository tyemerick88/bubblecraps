# Contributing to Bubble Craps

## Style Convention

Bubble Craps follows the [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
and [Google-style Python docstrings](https://google.github.io/styleguide/pyguide.html#38-comments-and-docstrings)
as closely as Ruff can enforce them. New Ruff settings should preserve or improve that alignment
unless a documented project constraint requires an exception.

Ruff is the single tool for formatting, linting, and import sorting in this repository. This differs
from crapssim's use of Black, but Ruff's formatter intentionally follows Black's style closely. The
project uses an 88-character line length to match Black's default and reduce formatting friction for
contributors working in both repositories. This is a deliberate exception to Google's general
80-character preference.

The formatter owns layout. Do not hand-format code to fight Ruff, and do not run Black or isort on
this repository. Format and lint before submitting a change:

```bash
python -m ruff format .
python -m ruff check --fix .
python -m ruff format --check .
python -m ruff check .
```

Review automatic fixes before committing them. Some findings require design judgment and are not
fixable automatically.

## Enforced Python Style

The Ruff configuration in `pyproject.toml` enforces the automatable parts of the project convention:

- Google-style docstrings for production modules, classes, functions, and methods.
- PEP 8 naming, imports, statement correctness, and common runtime-error checks.
- Explicit function annotations, supplemented by strict mypy checks.
- Deterministic import ordering through Ruff's isort-compatible rules.
- Common bug, simplification, return-flow, performance, and modern-Python checks.
- Pylint-derived design checks and a maximum McCabe complexity of 10.
- Double-quoted strings and Ruff's Black-compatible formatting at 88 characters.

Tests are exempt from mandatory docstrings because descriptive test names communicate behavior more
clearly than repetitive docstrings. Tests remain subject to every other selected Ruff rule. The
`docs/` directory is excluded because Ruff would otherwise rewrite historical Python examples inside
the Project Architecture Guide; executable examples should be covered by tests when introduced.

Ruff cannot enforce the entire Google guide. Contributors and reviewers remain responsible for
clear module ownership, focused functions and classes, useful comments, exception design, and
readable APIs. When Ruff and the written project conventions differ, `pyproject.toml` defines the
mechanical result and this document should be updated to explain the exception.

## Docstrings and Types

Use a one-line imperative summary for simple APIs. Use Google-style `Args`, `Returns`, `Raises`, and
`Yields` sections when those details add information that is not obvious from the signature. Do not
repeat type annotations in docstrings.

All production functions and methods require parameter and return annotations. Run strict type
checking with:

```bash
python -m mypy .
```

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) for commits created in
this repository:

```text
<type>[optional scope][!]: <summary>

[optional body]

[optional footer(s)]
```

Examples:

```text
feat(session): add immutable game state shell
fix(controller): reject roll while animation is active
docs: clarify local crapssim release workflow
test(architecture): reject Qt imports in session modules
build(deps): advance crapssim revision
feat(persistence)!: change session metadata schema
```

Use one of these types:

| Type | Purpose |
| --- | --- |
| `feat` | Add user-visible or domain capability. |
| `fix` | Correct a defect. |
| `docs` | Change documentation only. |
| `test` | Add or correct tests without changing production behavior. |
| `refactor` | Restructure code without changing behavior. |
| `perf` | Improve performance without changing behavior. |
| `build` | Change dependencies, packaging, or build configuration. |
| `ci` | Change continuous-integration configuration. |
| `chore` | Perform repository maintenance not covered above. |
| `revert` | Revert an earlier commit. |

Scopes are optional and should name the owning package or a stable concern, such as `session`,
`controller`, `gui`, `assets`, `application`, `architecture`, or `deps`. Do not invent a scope for a
change that is clearer without one.

Write the summary in lowercase imperative mood, without a trailing period. Keep the complete subject
line at 72 characters or fewer when practical. Describe what the commit does, not what was done:
prefer `add snapshot restore contract` over `added snapshot restore contract`.

Use a body when the motivation, tradeoff, or non-obvious behavior matters. Separate it from the
subject with a blank line and wrap prose at 72 characters. Reference issues or pull requests in
footers, for example `Refs: #42` or `Closes: #42`.

Mark an incompatible contract or file-format change with `!` and explain it in a `BREAKING CHANGE:`
footer. Before Bubble Craps v1.0.0, breaking changes are still marked because downstream files,
engine integration, and contributor workflows may depend on them.

Keep commits atomic: one coherent behavior or policy change per commit, including its tests and
documentation. Do not mix unrelated formatting, refactoring, and feature work. Merge commits created
by GitHub and automated version or release commits are exempt from the subject format.

## Full Validation

Follow the setup in [README.md](README.md), then run the complete labeled validation suite:

```bash
python tools/check.py
```

The runner streams native colored output when connected to a terminal, continues through failures,
and prints a plain-text error summary at the bottom. Use `--color` to force color, `--no-color` to
disable it, or set the standard `NO_COLOR` environment variable. The runner executes these gates:

```bash
python -m ruff format --check .
python -m ruff check .
python -m mypy .
python -m pytest
python -m pip check
```

All commands must pass before a change is ready for review. Architecture and game-engine ownership
requirements are defined in [docs/architecture-contract.md](docs/architecture-contract.md).