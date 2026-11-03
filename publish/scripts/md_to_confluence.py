"""md_to_confluence — canonical Markdown -> Confluence payload. PURE (no network).

SKELETON. Structure + CLI + contract are defined; the full Markdown -> Confluence
*storage format* (XHTML) mapping is TODO and is filled when publishing against a live
space. This script NEVER publishes — the doc-publish skill takes this payload and performs
the REST create/update (or an Atlassian MCP, once wired).

    python md_to_confluence.py docs/architecture/c4-context.md        # prints payload (dry run)
"""
from __future__ import annotations

import argparse
import json

from frontmatter import load


def convert(meta: dict, body: str) -> dict:
    """Return the Confluence create/update payload for one document."""
    title = meta.get("title") or "Untitled"
    space = (meta.get("target") or "").strip()  # e.g. "CORE/Parent page"

    # TODO: real Markdown -> Confluence storage format.
    #   - headings/lists/tables/code -> storage XHTML (or convert via a library)
    #   - Mermaid -> Mermaid macro if the space has it, else attach rendered image + .mmd
    #   - rewrite relative links / [[wikilinks]] to Confluence links using publish-map.yaml
    #   - collect images as attachments
    storage_body = f"<ac:structured-macro ac:name=\"note\"><ac:rich-text-body>"             f"<p>TODO: convert Markdown to storage format. {len(body)} chars.</p>"             f"</ac:rich-text-body></ac:structured-macro>"

    return {
        "backend": "confluence",
        "title": title,
        "space_target": space,
        "representation": "storage",
        "body": storage_body,
        "labels": [meta.get("category", "doc")],
    }


def main() -> None:
    ap = argparse.ArgumentParser(description="MD -> Confluence payload (pure, no publish)")
    ap.add_argument("doc", help="path to the canonical .md")
    args = ap.parse_args()
    meta, body = load(args.doc)
    if (meta.get("backend") or "").lower() not in ("confluence", ""):
        raise SystemExit(f"doc backend is {meta.get('backend')!r}, not confluence")
    print(json.dumps(convert(meta, body), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
