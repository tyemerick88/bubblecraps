from __future__ import annotations

import re
from pathlib import Path
from urllib.parse import urlsplit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MARKDOWN_LINK = re.compile(r"\[[^]]+\]\(([^)]+)\)")


def _markdown_files() -> list[Path]:
    root_documents = [PROJECT_ROOT / "README.md", PROJECT_ROOT / "CONTRIBUTING.md"]
    return [*root_documents, *sorted((PROJECT_ROOT / "docs").rglob("*.md"))]


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
