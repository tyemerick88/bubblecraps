"""Run the complete Bubble Craps quality gate suite."""

from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys
from collections.abc import Sequence
from dataclasses import dataclass
from pathlib import Path
from typing import Literal, cast

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SEPARATOR = "=" * 80
SUBSEPARATOR = "-" * 80
SUMMARY_LINE_LIMIT = 8
ANSI_ESCAPE = re.compile(r"\x1b\[[0-?]*[ -/]*[@-~]")
ColorMode = Literal["always", "auto", "never"]
CYAN = "\033[36m"
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"
ERROR_MARKERS = (
    "broken requirement",
    "error",
    "fail",
    "not found",
    "traceback",
    "would be reformatted",
)


@dataclass(frozen=True, slots=True)
class Check:
    """Describe one quality command and its display label."""

    label: str
    arguments: tuple[str, ...]


CHECKS = (
    Check("Ruff format", ("-m", "ruff", "format", "--check", ".")),
    Check("Ruff lint", ("-m", "ruff", "check", ".")),
    Check("Mypy", ("-m", "mypy", ".")),
    Check("Pytest", ("-m", "pytest")),
    Check("Pip dependency check", ("-m", "pip", "check")),
)


def _diagnostic_lines(output: str) -> list[str]:
    output = ANSI_ESCAPE.sub("", output)
    lines = [line.strip() for line in output.splitlines() if line.strip()]
    diagnostics = [
        line
        for line in lines
        if not line.lstrip("0123456789 ").startswith(("+", "-"))
        and any(marker in line.lower() for marker in ERROR_MARKERS)
    ]
    return diagnostics or lines[-SUMMARY_LINE_LIMIT:]


def _style(text: str, color: str, enabled: bool) -> str:
    return f"{color}{text}{RESET}" if enabled else text


def _color_enabled(mode: ColorMode) -> bool:
    if mode == "always":
        return True
    if mode == "never":
        return False
    return sys.stdout.isatty() and "NO_COLOR" not in os.environ


def _command_arguments(check: Check, color_enabled: bool) -> list[str]:
    arguments = list(check.arguments)
    module = arguments[1]

    if module == "ruff":
        arguments[2:2] = ["--color", "always" if color_enabled else "never"]
    elif module == "mypy":
        arguments.insert(2, "--color-output" if color_enabled else "--no-color-output")
    elif module == "pytest":
        arguments.insert(2, f"--color={'yes' if color_enabled else 'no'}")
    elif module == "pip" and not color_enabled:
        arguments.append("--no-color")

    return arguments


def _print_check_header(check: Check, index: int, color_enabled: bool) -> None:
    arguments = _command_arguments(check, color_enabled)
    print(_style(SEPARATOR, CYAN, color_enabled))
    heading = f"CHECK {index}/{len(CHECKS)}: {check.label}"
    print(_style(heading, CYAN, color_enabled))
    print(f"COMMAND: python {' '.join(arguments)}")
    print(_style(SUBSEPARATOR, CYAN, color_enabled))


def _print_error_summary(
    failures: list[tuple[Check, subprocess.CompletedProcess[str]]],
    color_enabled: bool,
) -> None:
    summary_color = RED if failures else GREEN
    print(_style(SEPARATOR, summary_color, color_enabled))
    print(_style("ERROR SUMMARY", summary_color, color_enabled))
    print(_style(SUBSEPARATOR, summary_color, color_enabled))

    if not failures:
        print(_style("No errors. All checks passed.", GREEN, color_enabled))
        return

    for check, result in failures:
        diagnostics = _diagnostic_lines(result.stdout)
        failure = f"{check.label}: FAILED (exit code {result.returncode})"
        print(_style(failure, RED, color_enabled))
        for line in diagnostics[:SUMMARY_LINE_LIMIT]:
            print(f"  {line}")
        if len(diagnostics) > SUMMARY_LINE_LIMIT:
            remaining = len(diagnostics) - SUMMARY_LINE_LIMIT
            print(
                f"  ... {remaining} more diagnostic line(s); see the full output above."
            )


def _run_check(check: Check, color_enabled: bool) -> subprocess.CompletedProcess[str]:
    arguments = _command_arguments(check, color_enabled)
    environment = os.environ.copy()
    if color_enabled:
        environment["FORCE_COLOR"] = "1"
        environment.pop("NO_COLOR", None)
    else:
        environment["NO_COLOR"] = "1"
        environment.pop("FORCE_COLOR", None)

    process = subprocess.Popen(
        [sys.executable, *arguments],
        cwd=PROJECT_ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        env=environment,
        bufsize=1,
        text=True,
    )
    assert process.stdout is not None

    output_lines: list[str] = []
    for line in process.stdout:
        output_lines.append(line)
        print(line, end="", flush=True)

    return subprocess.CompletedProcess(
        process.args,
        process.wait(),
        stdout="".join(output_lines),
    )


def _parse_color_mode(arguments: Sequence[str] | None) -> ColorMode:
    parser = argparse.ArgumentParser(description=__doc__)
    color_group = parser.add_mutually_exclusive_group()
    color_group.add_argument(
        "--color",
        action="store_const",
        const="always",
        dest="color_mode",
        help="force colored output",
    )
    color_group.add_argument(
        "--no-color",
        action="store_const",
        const="never",
        dest="color_mode",
        help="disable colored output",
    )
    parser.set_defaults(color_mode="auto")
    namespace = parser.parse_args(arguments)
    return cast(ColorMode, namespace.color_mode)


def main(arguments: Sequence[str] | None = None) -> int:
    """Run every quality check and return a process exit status."""
    color_enabled = _color_enabled(_parse_color_mode(arguments))
    failures: list[tuple[Check, subprocess.CompletedProcess[str]]] = []

    for index, check in enumerate(CHECKS, start=1):
        _print_check_header(check, index, color_enabled)
        result = _run_check(check, color_enabled)
        if not result.stdout:
            print("(no output)")
        elif not result.stdout.endswith("\n"):
            print()
        print(_style(SUBSEPARATOR, CYAN, color_enabled))
        status = "PASS" if result.returncode == 0 else "FAIL"
        result_color = GREEN if result.returncode == 0 else RED
        result_text = f"RESULT: {status} (exit code {result.returncode})"
        print(_style(result_text, result_color, color_enabled))
        print()

        if result.returncode != 0:
            failures.append((check, result))

    _print_error_summary(failures, color_enabled)
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
