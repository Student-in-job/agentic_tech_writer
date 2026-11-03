"""md_to_gdocs — canonical Markdown -> Google Docs batchUpdate requests. PURE (no network).

SKELETON. The doc-publish skill feeds the result to the Google Docs connector /
`google-workspace` skill. This script never calls Google.

    python md_to_gdocs.py docs/business/requirements/frd.md
"""
from __future__ import annotations

import argparse
import json

from frontmatter import load


def convert(meta: dict, body: str) -> dict:
    """Return a Google Docs create payload + batchUpdate requests for one document."""
    title = meta.get("title") or "Untitled"

    # TODO: real Markdown -> Docs requests.
    #   - insertText + updateParagraphStyle for headings, createParagraphBullets for lists
    #   - insertTable for tables; code -> monospace text runs
    #   - Mermaid -> insertInlineImage of a rendered diagram
    #   - rewrite relative links / [[wikilinks]] via publish-map.yaml
    requests = [{"insertText": {"location": {"index": 1}, "text": body}}]

    return {
        "backend": "gdocs",
        "title": title,
        "folder_target": (meta.get("target") or "").strip(),
        "requests": requests,
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="MD -> Google Docs requests (pure, no publish)")
    ap.add_argument("doc", help="path to the canonical .md")
    args = ap.parse_args()
    meta, body = load(args.doc)
    if (meta.get("backend") or "").lower() not in ("gdocs", "md", ""):
        raise SystemExit(f"doc backend is {meta.get('backend')!r}, not gdocs")
    print(json.dumps(convert(meta, body), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
