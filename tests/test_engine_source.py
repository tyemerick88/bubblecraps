from __future__ import annotations

import subprocess
from pathlib import Path

from crapssim.rules import CraplessRules

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ENGINE_ROOT = PROJECT_ROOT.parent / "crapssim"
REVISION_FILE = PROJECT_ROOT / ".crapssim-revision"


def _git(*arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", *arguments],
        cwd=ENGINE_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )


def test_crapssim_checkout_matches_recorded_revision() -> None:
    assert (ENGINE_ROOT / ".git").exists(), f"Missing sibling checkout: {ENGINE_ROOT}"

    expected_revision = REVISION_FILE.read_text(encoding="utf-8").strip()
    revision_result = _git("rev-parse", "HEAD")

    assert revision_result.returncode == 0, revision_result.stderr
    assert revision_result.stdout.strip() == expected_revision

    status_result = _git(
        "status",
        "--porcelain=v1",
        "--untracked-files=all",
        "--",
        "crapssim",
        "project.toml",
        "setup.cfg",
        "setup.py",
    )
    assert status_result.returncode == 0, status_result.stderr
    assert not status_result.stdout.strip(), (
        "crapssim package or packaging files differ from the recorded commit. Commit the engine "
        "change and advance .crapssim-revision intentionally:\n"
        f"{status_result.stdout}"
    )


def test_crapless_rules_are_available_from_engine() -> None:
    rules = CraplessRules()

    assert rules.point_numbers() == [2, 3, 4, 5, 6, 8, 9, 10, 11, 12]
    assert rules.come_out_winners() == [7]
    assert rules.come_out_losers() == []
    assert not rules.allow_dont_pass()
    assert not rules.allow_dont_come()
