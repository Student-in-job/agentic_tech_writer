"""Parse a document's YAML frontmatter + Markdown body. Pure — no network, no side effects.

A published document (in docs/) has exactly ONE frontmatter block at the top:

    ---
    title: ...
    backend: confluence
    target: ...
    ---
    # Heading
    body...

Usage:
    from frontmatter import load
    meta, body = load("docs/business/vision.md")
"""
from __future__ import annotations

import pathlib
from typing import Tuple

try:
    import yaml  # PyYAML
except ImportError as e:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from e


def split(text: str) -> Tuple[dict, str]:
    """Return (meta, body). If there is no frontmatter, meta is {}."""
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].strip() != "---":
        return {}, text
    for i in range(1, len(lines)):
        if lines[i].strip() == "---":
            meta = yaml.safe_load("".join(lines[1:i])) or {}
            body = "".join(lines[i + 1:]).lstrip("\n")
            if not isinstance(meta, dict):
                raise ValueError("frontmatter is not a mapping")
            return meta, body
    raise ValueError("unterminated frontmatter block")


def load(path: str | pathlib.Path) -> Tuple[dict, str]:
    return split(pathlib.Path(path).read_text(encoding="utf-8"))


if __name__ == "__main__":
    import json
    import sys

    meta, body = load(sys.argv[1])
    print(json.dumps({"meta": meta, "body_chars": len(body)}, ensure_ascii=False, indent=2))
