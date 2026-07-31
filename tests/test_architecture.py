from __future__ import annotations

import ast
import importlib
import pkgutil
from pathlib import Path

import bubblecraps

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PACKAGE_ROOT = PROJECT_ROOT / "src" / "bubblecraps"
ENTRY_POINTS = (
    PROJECT_ROOT / "main.py",
    PACKAGE_ROOT / "__main__.py",
)
BOOTSTRAP_MODULE = "bubblecraps.application.bootstrap"

FORBIDDEN_IMPORTS = {
    "application": ("crapssim",),
    "assets": (
        "bubblecraps.application",
        "bubblecraps.controller",
        "bubblecraps.gui",
        "bubblecraps.session",
        "crapssim",
    ),
    "controller": (
        "bubblecraps.application",
        "bubblecraps.assets",
        "bubblecraps.gui",
        "crapssim",
    ),
    "gui": ("bubblecraps.application", "bubblecraps.session", "crapssim"),
    "session": (
        "PySide6",
        "bubblecraps.application",
        "bubblecraps.assets",
        "bubblecraps.controller",
        "bubblecraps.gui",
    ),
}


def _resolve_from_import(path: Path, node: ast.ImportFrom) -> list[str]:
    if node.level == 0:
        return [node.module] if node.module else []

    relative_parent = path.relative_to(PACKAGE_ROOT).parent.parts
    package_parts = ["bubblecraps", *relative_parent]
    prefix_length = len(package_parts) - node.level + 1
    prefix = package_parts[: max(prefix_length, 0)]

    if node.module:
        return [".".join([*prefix, node.module])]
    return [".".join([*prefix, alias.name]) for alias in node.names]


def _imports_in(path: Path) -> list[tuple[int, str]]:
    tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
    imports: list[tuple[int, str]] = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            imports.extend((node.lineno, alias.name) for alias in node.names)
        elif isinstance(node, ast.ImportFrom):
            imports.extend(
                (node.lineno, name) for name in _resolve_from_import(path, node)
            )

    return imports


def _matches_prefix(module: str, prefix: str) -> bool:
    return module == prefix or module.startswith(f"{prefix}.")


def test_runtime_layers_follow_import_contract() -> None:
    violations: list[str] = []

    for layer, forbidden_prefixes in FORBIDDEN_IMPORTS.items():
        layer_root = PACKAGE_ROOT / layer
        for path in sorted(layer_root.rglob("*.py")) if layer_root.exists() else []:
            for line_number, module in _imports_in(path):
                if any(
                    _matches_prefix(module, prefix) for prefix in forbidden_prefixes
                ):
                    relative_path = path.relative_to(PROJECT_ROOT)
                    violations.append(f"{relative_path}:{line_number} imports {module}")

    assert not violations, "Architecture contract violations:\n" + "\n".join(violations)


def test_entry_points_import_only_the_application_bootstrap() -> None:
    violations: list[str] = []

    for path in ENTRY_POINTS:
        project_imports = [
            module
            for _, module in _imports_in(path)
            if _matches_prefix(module, "bubblecraps")
        ]
        if project_imports != [BOOTSTRAP_MODULE]:
            relative_path = path.relative_to(PROJECT_ROOT)
            violations.append(f"{relative_path} imports {project_imports}")

    assert not violations, "Entry point import violations:\n" + "\n".join(violations)


def test_all_runtime_modules_import_without_cycles() -> None:
    module_names = [
        module.name
        for module in pkgutil.walk_packages(
            bubblecraps.__path__, f"{bubblecraps.__name__}."
        )
    ]

    for module_name in module_names:
        importlib.import_module(module_name)
