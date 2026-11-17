"""A small Markdown parser for the subset our authored docs use. Pure, no dependencies.

Blocks (dicts with key "t"):
  h       {"level", "inl"}
  p       {"inl"}
  code    {"lang", "text"}
  mermaid {"text", "index"}             index = 1-based order of the diagram in the document
  table   {"head": [inl], "rows": [[inl]]}
  list    {"ordered", "items": [{"inl", "children": [list-blocks]}]}
  quote   {"kind": NOTE|IMPORTANT|WARNING|TIP|CAUTION|None, "blocks"}
  hr      {}

Inline = list of spans: {"text", "b", "i", "code", "href", "wiki"}.
"""
from __future__ import annotations

import re

_FENCE = re.compile(r"^(\s*)(`{3,}|~{3,})\s*([\w+-]*)\s*$")
_HEAD = re.compile(r"^(#{1,6})\s+(.*?)\s*#*\s*$")
_ITEM = re.compile(r"^(\s*)([-*+]|\d+[.)])\s+(.*)$")
_HR = re.compile(r"^\s*([-*_])(\s*\1){2,}\s*$")
_SEP = re.compile(r"^\s*\|?\s*:?-{1,}:?\s*(\|\s*:?-{1,}:?\s*)*\|?\s*$")
_ALERT = re.compile(r"^\[!(\w+)\]\s*(.*)$")

_TOKEN = re.compile(
    r"\\([\\`*_\[\]|<>#~])"                                   # 1 escape
    r"|(`+)(.+?)\2"                                           # 2,3 code span
    r"|\[\[([^\]]+)\]\]"                                      # 4 wikilink
    r"|\[([^\]]+)\]\(([^)\s]+)(?:\s+\"[^\"]*\")?\)"           # 5,6 link
    r"|\*\*(.+?)\*\*"                                         # 7 bold
    r"|(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])"             # 8 italic *
    r"|(?<![\w_])_(?!\s)(.+?)(?<!\s)_(?![\w_])"               # 9 italic _
    r"|~~(.+?)~~"                                             # 10 strike (rendered plain)
)


def span(text, b=False, i=False, code=False, href=None, wiki=None):
    return {"text": text, "b": b, "i": i, "code": code, "href": href, "wiki": wiki}


def parse_inline(text: str, b=False, i=False, href=None) -> list[dict]:
    out: list[dict] = []
    pos = 0
    for m in _TOKEN.finditer(text):
        if m.start() > pos:
            out.append(span(text[pos:m.start()], b, i, href=href))
        if m.group(1) is not None:
            out.append(span(m.group(1), b, i, href=href))
        elif m.group(2) is not None:
            out.append(span(m.group(3).strip() if m.group(3).strip() else m.group(3), b, i, code=True, href=href))
        elif m.group(4) is not None:
            target, _, alias = m.group(4).partition("|")
            out.append(span(alias or target, b, i, wiki=target.split("#")[0].strip()))
        elif m.group(5) is not None:
            out.extend(parse_inline(m.group(5), b, i, href=m.group(6)))
        elif m.group(7) is not None:
            out.extend(parse_inline(m.group(7), True, i, href))
        elif m.group(8) is not None:
            out.extend(parse_inline(m.group(8), b, True, href))
        elif m.group(9) is not None:
            out.extend(parse_inline(m.group(9), b, True, href))
        elif m.group(10) is not None:
            out.extend(parse_inline(m.group(10), b, i, href))
        pos = m.end()
    if pos < len(text):
        out.append(span(text[pos:], b, i, href=href))
    return out


def plain(inl: list[dict]) -> str:
    return "".join(s["text"] for s in inl)


def split_row(line: str) -> list[str]:
    """Split a table row on pipes that are neither escaped nor inside a code span."""
    cells, cur, in_code, i = [], [], False, 0
    s = line.strip()
    while i < len(s):
        ch = s[i]
        if ch == "\\" and i + 1 < len(s) and s[i + 1] == "|":
            cur.append("|" if in_code else "\\|")
            i += 2
            continue
        if ch == "`":
            in_code = not in_code
        if ch == "|" and not in_code:
            cells.append("".join(cur))
            cur = []
        else:
            cur.append(ch)
        i += 1
    cells.append("".join(cur))
    if cells and cells[0].strip() == "":
        cells = cells[1:]
    if cells and cells[-1].strip() == "":
        cells = cells[:-1]
    return [c.strip() for c in cells]


def _is_table_start(lines: list[str], i: int) -> bool:
    return "|" in lines[i] and i + 1 < len(lines) and bool(_SEP.match(lines[i + 1])) and "-" in lines[i + 1]


def parse(text: str) -> list[dict]:
    lines = text.replace("\r\n", "\n").replace("\t", "    ").split("\n")
    counter = {"mermaid": 0}
    return _blocks(lines, counter)


def _blocks(lines: list[str], counter: dict) -> list[dict]:
    out: list[dict] = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue
        if line.lstrip().startswith("<!--"):
            while i < n and "-->" not in lines[i]:
                i += 1
            i += 1
            continue
        m = _FENCE.match(line)
        if m:
            fence, lang, indent = m.group(2), m.group(3).lower(), len(m.group(1))
            body, i = [], i + 1
            while i < n and not re.match(rf"^\s*{re.escape(fence[0])}{{{len(fence)},}}\s*$", lines[i]):
                body.append(lines[i][indent:] if lines[i][:indent].strip() == "" else lines[i])
                i += 1
            i += 1
            if lang == "mermaid":
                counter["mermaid"] += 1
                out.append({"t": "mermaid", "text": "\n".join(body).strip() + "\n", "index": counter["mermaid"]})
            else:
                out.append({"t": "code", "lang": lang, "text": "\n".join(body).rstrip()})
            continue
        m = _HEAD.match(line)
        if m:
            out.append({"t": "h", "level": len(m.group(1)), "inl": parse_inline(m.group(2))})
            i += 1
            continue
        if _HR.match(line):
            out.append({"t": "hr"})
            i += 1
            continue
        if line.lstrip().startswith(">"):
            body = []
            while i < n and lines[i].lstrip().startswith(">"):
                body.append(re.sub(r"^\s*>\s?", "", lines[i]))
                i += 1
            kind = None
            if body:
                am = _ALERT.match(body[0].strip())
                if am:
                    kind = am.group(1).upper()
                    body = ([am.group(2)] if am.group(2) else []) + body[1:]
            out.append({"t": "quote", "kind": kind, "blocks": _blocks(body, counter)})
            continue
        if _is_table_start(lines, i):
            head = [parse_inline(c) for c in split_row(lines[i])]
            i += 2
            rows = []
            while i < n and lines[i].strip() and "|" in lines[i]:
                cells = split_row(lines[i])
                cells = (cells + [""] * len(head))[:max(len(head), len(cells))]
                rows.append([parse_inline(c) for c in cells])
                i += 1
            out.append({"t": "table", "head": head, "rows": rows})
            continue
        if _ITEM.match(line):
            block, i = _list(lines, i)
            out.append(block)
            continue
        para = [line.strip()]
        i += 1
        while i < n and lines[i].strip() and not _starts_block(lines, i):
            para.append(lines[i].strip())
            i += 1
        out.append({"t": "p", "inl": parse_inline(" ".join(para))})
    return out


def _starts_block(lines: list[str], i: int) -> bool:
    s = lines[i]
    return bool(_FENCE.match(s) or _HEAD.match(s) or _HR.match(s) or s.lstrip().startswith(">")
                or _ITEM.match(s) or _is_table_start(lines, i))


def _list(lines: list[str], i: int) -> tuple[dict, int]:
    n = len(lines)
    m = _ITEM.match(lines[i])
    base = len(m.group(1))
    ordered = m.group(2)[0].isdigit()
    items: list[dict] = []
    while i < n:
        m = _ITEM.match(lines[i])
        if not m:
            break
        indent = len(m.group(1))
        if indent < base:
            break
        if indent > base + 1 and items:                       # nested list
            child, i = _list(lines, i)
            items[-1]["children"].append(child)
            continue
        if m.group(2)[0].isdigit() != ordered and indent == base:
            break
        text = [m.group(3).strip()]
        i += 1
        while i < n:
            nxt = lines[i]
            if not nxt.strip():
                j = i + 1                                     # blank: continue only if list goes on
                while j < n and not lines[j].strip():
                    j += 1
                nm = _ITEM.match(lines[j]) if j < n else None
                if nm and len(nm.group(1)) >= base:
                    i = j
                break
            if _ITEM.match(nxt) or _FENCE.match(nxt) or _HEAD.match(nxt) or nxt.lstrip().startswith(">"):
                break
            if _is_table_start(lines, i):
                break
            text.append(nxt.strip())
            i += 1
        items.append({"inl": parse_inline(" ".join(text)), "children": []})
    return {"t": "list", "ordered": ordered, "items": items}, i
