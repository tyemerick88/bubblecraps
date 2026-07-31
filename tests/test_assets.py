from __future__ import annotations

from pathlib import Path

from bubblecraps.assets import AssetManager

PROJECT_ROOT = Path(__file__).resolve().parents[1]
ASSET_DIRECTORIES = (
    "chips",
    "dice",
    "table",
    "puck",
    "buttons",
    "icons",
    "fonts",
    "sounds/dice",
    "sounds/chips",
    "sounds/ui",
    "sounds/payouts",
    "themes",
)
ASSET_METHODS = (
    "chip",
    "die_face",
    "puck",
    "table_background",
    "icon",
    "sound",
    "font",
)


def test_asset_manager_exposes_the_pag_semantic_interface() -> None:
    assert all(callable(getattr(AssetManager, method)) for method in ASSET_METHODS)


def test_physical_asset_directories_are_preserved() -> None:
    asset_root = PROJECT_ROOT / "assets"

    assert all(
        (asset_root / directory / ".gitkeep").is_file()
        for directory in ASSET_DIRECTORIES
    )
