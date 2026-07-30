from __future__ import annotations

import subprocess
import sys

import pytest

from tools import check as check_script


def test_main_runs_every_check_and_summarizes_failures(
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    calls: list[str] = []

    def fake_run(
        check: check_script.Check,
        color_enabled: bool,
    ) -> subprocess.CompletedProcess[str]:
        assert not color_enabled
        calls.append(check.label)
        if check.label == "Ruff format":
            output = """\033[31munformatted: File would be reformatted\033[0m
12 - ERROR_MARKERS = ("error",)
1 file would be reformatted, 4 files already formatted
"""
            return subprocess.CompletedProcess(check.arguments, 1, stdout=output)
        return subprocess.CompletedProcess(check.arguments, 0, stdout="Passed")

    monkeypatch.setattr(check_script, "_run_check", fake_run)

    assert check_script.main([]) == 1

    output = capsys.readouterr().out
    assert calls == [check.label for check in check_script.CHECKS]
    assert "CHECK 1/5: Ruff format" in output
    assert "CHECK 5/5: Pip dependency check" in output
    assert "ERROR SUMMARY" in output
    assert "Ruff format: FAILED (exit code 1)" in output
    assert "unformatted: File would be reformatted" in output
    assert "\033[" not in output
    assert '12 - ERROR_MARKERS = ("error",)' not in output.split("ERROR SUMMARY", 1)[1]


@pytest.mark.parametrize(
    ("arguments", "expected"),
    [([], False), (["--color"], True), (["--no-color"], False)],
)
def test_main_selects_requested_color_mode(
    arguments: list[str],
    expected: bool,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    observed: list[bool] = []

    def fake_run(
        check: check_script.Check,
        color_enabled: bool,
    ) -> subprocess.CompletedProcess[str]:
        observed.append(color_enabled)
        return subprocess.CompletedProcess(check.arguments, 0, stdout="")

    monkeypatch.setattr(check_script, "_run_check", fake_run)
    monkeypatch.setattr(sys.stdout, "isatty", lambda: False)

    assert check_script.main(arguments) == 0
    assert observed == [expected] * len(check_script.CHECKS)


def test_command_arguments_set_native_color_modes() -> None:
    enabled = [
        check_script._command_arguments(check, True) for check in check_script.CHECKS
    ]
    disabled = [
        check_script._command_arguments(check, False) for check in check_script.CHECKS
    ]

    assert enabled[0][2:4] == ["--color", "always"]
    assert "--color-output" in enabled[2]
    assert "--color=yes" in enabled[3]
    assert "--no-color" not in enabled[4]
    assert disabled[0][2:4] == ["--color", "never"]
    assert "--no-color-output" in disabled[2]
    assert "--color=no" in disabled[3]
    assert "--no-color" in disabled[4]


def test_auto_color_honors_no_color(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys.stdout, "isatty", lambda: True)
    monkeypatch.setenv("NO_COLOR", "1")

    assert not check_script._color_enabled("auto")


def test_run_check_streams_and_captures_output(
    capsys: pytest.CaptureFixture[str],
) -> None:
    output = "\033[31mproblem\033[0m"
    check = check_script.Check("Stream test", ("-c", f"print({output!r})"))

    result = check_script._run_check(check, color_enabled=True)

    assert result.returncode == 0
    assert result.stdout == f"{output}\n"
    assert capsys.readouterr().out == f"{output}\n"
