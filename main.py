"""Launch the Bubble Craps application."""

from __future__ import annotations

import sys
from pathlib import Path

# Expose the source-layout package before importing the sole runtime dependency.
sys.path.insert(0, str(Path(__file__).parent / "src"))

from bubblecraps.application.bootstrap import main as bootstrap_main

if __name__ == "__main__":
    raise SystemExit(bootstrap_main())
