"""Render parsed Markdown blocks into a standalone HTML page (used for PDF via headless Chrome).

Diagrams are inlined as SVG, so the PDF keeps them as vectors.
"""
from __future__ import annotations

import html
import re

ALERT_LABELS = {"NOTE": "Примечание", "TIP": "Совет", "IMPORTANT": "Важно",
                "WARNING": "Внимание", "CAUTION": "Осторожно"}

CSS = """
@page { size: A4; margin: 18mm 16mm; }
body { font-family: Arial, Helvetica, sans-serif; font-size: 10.5pt; line-height: 1.4; color: #1b1b1b; }
h1 { font-size: 22pt; color: #1f2a44; margin: 0 0 8pt; }
h2 { font-size: 15pt; color: #1f2a44; margin: 16pt 0 6pt; border-bottom: 1px solid #d5dbe5; padding-bottom: 2pt; }
h3 { font-size: 12.5pt; color: #1f2a44; margin: 12pt 0 4pt; }
h4, h5, h6 { font-size: 11pt; color: #1f2a44; margin: 10pt 0 4pt; }
code { font-family: "Courier New", monospace; font-size: 9.5pt; color: #8a1c4a; }
pre { background: #f6f8fa; border-left: 3px solid #b0b7c0; padding: 6pt 8pt; font-size: 9pt; white-space: pre-wrap; }
pre code { color: #24292e; }
table { border-collapse: collapse; width: 100%; margin: 6pt 0 10pt; font-size: 9pt; }
th, td { border: 1px solid #b8c0cc; padding: 3pt 5pt; vertical-align: top; text-align: left; }
th { background: #dce6f2; }
thead { display: table-header-group; }
tr { break-inside: avoid; }
table.meta td:first-child { background: #eef2f7; font-weight: bold; width: 28%; }
.alert { border-left: 4px solid #9e9e9e; background: #f5f5f5; padding: 5pt 9pt; margin: 6pt 0 10pt; break-inside: avoid; }
.alert.NOTE { border-color: #2f6fb5; background: #eaf2fb; } .alert.IMPORTANT { border-color: #6a3fb5; background: #f1eafb; }
.alert.WARNING { border-color: #b26a00; background: #fff4d6; } .alert.CAUTION { border-color: #b3261e; background: #fdecea; }
.alert.TIP { border-color: #2e7d32; background: #e8f5e9; }
.alert .label { font-weight: bold; margin-bottom: 2pt; }
.alert p { margin: 2pt 0; }
figure { margin: 8pt 0 12pt; text-align: center; break-inside: avoid; }
figure svg { max-width: 100%; height: auto; }
figcaption { font-size: 8.5pt; color: #606060; font-style: italic; }
a { color: #1155cc; } .wiki { font-style: italic; }
.footer { margin-top: 18pt; font-size: 8pt; color: #707070; border-top: 1px solid #d5dbe5; padding-top: 4pt; }
"""


class Ctx:
    def __init__(self, resolve_link=None, diagrams=None):
        self.resolve_link = resolve_link or (lambda s: (None, None))
        self.diagrams = diagrams or {}
        self.figure = 0


def inline(ctx: Ctx, inl: list[dict]) -> str:
    out = []
    for s in inl:
        text = s["text"]
        url = None
        if s.get("href") or s.get("wiki"):
            url, label = ctx.resolve_link(s)
            text = label or text
        t = html.escape(text)
        if s.get("code"):
            t = f"<code>{t}</code>"
        if s.get("b"):
            t = f"<strong>{t}</strong>"
        if s.get("i"):
            t = f"<em>{t}</em>"
        if url:
            t = f'<a href="{html.escape(url, quote=True)}">{t}</a>'
        elif s.get("wiki"):
            t = f'<span class="wiki">{t}</span>'
        out.append(t)
    return "".join(out)


def blocks_html(ctx: Ctx, blocks: list[dict]) -> str:
    out = []
    for b in blocks:
        t = b["t"]
        if t == "h":
            lvl = min(b["level"], 6)
            out.append(f"<h{lvl}>{inline(ctx, b['inl'])}</h{lvl}>")
        elif t == "p":
            out.append(f"<p>{inline(ctx, b['inl'])}</p>")
        elif t == "list":
            out.append(_list(ctx, b))
        elif t == "code":
            out.append(f"<pre><code>{html.escape(b['text'])}</code></pre>")
        elif t == "table":
            head = "".join(f"<th>{inline(ctx, c)}</th>" for c in b["head"])
            rows = "".join("<tr>" + "".join(f"<td>{inline(ctx, c)}</td>" for c in r) + "</tr>" for r in b["rows"])
            out.append(f"<table><thead><tr>{head}</tr></thead><tbody>{rows}</tbody></table>")
        elif t == "quote":
            kind = b["kind"] or ""
            label = ALERT_LABELS.get(kind, "")
            lab = f'<div class="label">{label}</div>' if label else ""
            out.append(f'<div class="alert {kind}">{lab}{blocks_html(ctx, b["blocks"])}</div>')
        elif t == "mermaid":
            d = ctx.diagrams.get(b["index"])
            if d is None or d.svg is None:
                out.append(f"<pre><code>{html.escape(b['text'])}</code></pre>")
            else:
                ctx.figure += 1
                svg = re.sub(r"^<\?xml[^>]*\?>", "", d.svg.read_text(encoding="utf-8")).strip()
                svg = svg.replace('id="dgm"', f'id="dgm{ctx.figure}"').replace("#dgm", f"#dgm{ctx.figure}")
                out.append(f"<figure>{svg}<figcaption>Схема {ctx.figure}. {html.escape(d.title)}</figcaption></figure>")
        elif t == "hr":
            out.append("<hr>")
    return "\n".join(out)


def _list(ctx: Ctx, b: dict) -> str:
    tag = "ol" if b["ordered"] else "ul"
    items = "".join(f"<li>{inline(ctx, it['inl'])}{''.join(_list(ctx, c) for c in it['children'])}</li>"
                    for it in b["items"])
    return f"<{tag}>{items}</{tag}>"


def build_page(*, title: str, version: str, meta_rows: list[tuple[str, str]], blocks: list[dict],
               resolve_link=None, diagrams=None) -> str:
    from . import mdparse
    ctx = Ctx(resolve_link, diagrams)
    body = list(blocks)
    head_html = ""
    if body and body[0]["t"] == "h" and body[0]["level"] == 1:
        head_html = blocks_html(ctx, [body.pop(0)])
    else:
        head_html = f"<h1>{html.escape(title)}</h1>"
    meta = "".join(f"<tr><td>{html.escape(k)}</td><td>{inline(ctx, mdparse.parse_inline(v))}</td></tr>"
                   for k, v in meta_rows)
    return (f'<!doctype html><html lang="ru"><head><meta charset="utf-8"><title>{html.escape(title)}</title>'
            f"<style>{CSS}</style></head><body>{head_html}<table class=\"meta\">{meta}</table>"
            f"{blocks_html(ctx, body)}"
            f'<div class="footer">{html.escape(title)} · версия {html.escape(str(version))}</div></body></html>')
