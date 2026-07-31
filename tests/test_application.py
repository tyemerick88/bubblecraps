from __future__ import annotations

import bubblecraps
from bubblecraps.application import configuration
from bubblecraps.application.logging import LoggingManager


def test_application_infrastructure_placeholders_are_importable() -> None:
    assert configuration.__doc__ is not None
    assert LoggingManager.__doc__ is not None


def test_package_exposes_the_milestone_release_version() -> None:
    assert bubblecraps.__version__ == "0.0.0-alpha.1.2026-07-31"
