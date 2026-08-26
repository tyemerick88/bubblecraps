from __future__ import annotations

import re
import sys
from pathlib import Path
from urllib.parse import urlsplit

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def _markdown_files() -> list[Path]:
    root_documents = [PROJECT_ROOT / "README.md", PROJECT_ROOT / "CONTRIBUTING.md"]
    documentation_root = PROJECT_ROOT / "docs"
    documentation = [
        path
        for path in documentation_root.rglob("*.md")
        if not any(
            part.startswith(".")
            for part in path.relative_to(documentation_root).parts[:-1]
        )
    ]
    return [*root_documents, *sorted(documentation)]


def test_markdown_files_ignore_hidden_directories(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(sys.modules[__name__], "PROJECT_ROOT", tmp_path)
    (tmp_path / "README.md").touch()
    (tmp_path / "CONTRIBUTING.md").touch()
    (tmp_path / "docs" / "visible").mkdir(parents=True)
    (tmp_path / "docs" / "visible" / "included.md").touch()
    (tmp_path / "docs" / "visible" / ".private").mkdir()
    hidden_document = tmp_path / "docs" / "visible" / ".private" / "ignored.md"
    hidden_document.touch()

    markdown_files = _markdown_files()

    assert tmp_path / "docs" / "visible" / "included.md" in markdown_files
    assert hidden_document not in markdown_files


def test_local_markdown_links_resolve() -> None:
    missing_links: list[str] = []

    for document in _markdown_files():
        text = document.read_text(encoding="utf-8")
        for target in MARKDOWN_LINK.findall(text):
            path_text = target.split("#", 1)[0]
            if not path_text or urlsplit(path_text).scheme:
                continue

            if not (document.parent / path_text).resolve().exists():
                relative_document = document.relative_to(PROJECT_ROOT)
                missing_links.append(f"{relative_document} -> {target}")

    assert not missing_links, "Missing local Markdown links:\n" + "\n".join(
        missing_links
    )
