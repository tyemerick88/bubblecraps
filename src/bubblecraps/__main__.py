"""Support launching Bubble Craps as a module."""

from __future__ import annotations

from bubblecraps.application.bootstrap import main as bootstrap_main

if __name__ == "__main__":
    raise SystemExit(bootstrap_main())
