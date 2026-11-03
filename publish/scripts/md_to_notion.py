"""md_to_notion — canonical Markdown -> Notion blocks. PURE (no network).

SKELETON. The doc-publish skill feeds the result to the Notion MCP
(`notion-create-pages` / `notion-update-page`). This script never calls Notion.

    python md_to_notion.py docs/business/requirements/frd.md
"""
from __future__ import annotations

import argparse
import json

from frontmatter import load


def _paragraph(text: str) -> dict:
    return {
        "object": "block",
        "type": "paragraph",
        "paragraph": {"rich_text": [{"type": "text", "text": {"content": text}}]},
    }


def convert(meta: dict, body: str) -> dict:
    """Return a Notion create/update payload for one document."""
    title = meta.get("title") or "Untitled"

    # TODO: real Markdown -> Notion blocks.
    #   - headings -> heading_1/2/3, lists -> bulleted/numbered_list_item, tables -> table
    #   - code fences -> code blocks; Mermaid -> code(language="mermaid") or image
    #   - rewrite relative links / [[wikilinks]] via publish-map.yaml
    blocks = [_paragraph(line) for line in body.splitlines() if line.strip()]

    return {
        "backend": "notion",
        "title": title,
        "parent_target": (meta.get("target") or "").strip(),
        "properties": {"title": title, "status": meta.get("status"), "version": meta.get("version")},
        "children": blocks,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="MD -> Notion blocks (pure, no publish)")
    ap.add_argument("doc", help="path to the canonical .md")
    args = ap.parse_args()
    meta, body = load(args.doc)
    if (meta.get("backend") or "").lower() not in ("notion", ""):
        raise SystemExit(f"doc backend is {meta.get('backend')!r}, not notion")
    print(json.dumps(convert(meta, body), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
