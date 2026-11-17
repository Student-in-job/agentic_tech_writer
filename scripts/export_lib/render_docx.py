"""Render parsed Markdown blocks into a .docx (python-docx). Pure — writes only the given path.

Google Docs opens these files directly. Diagrams are embedded as PNG (Google Docs cannot
display SVG); the SVG / draw.io sources live in the service's `diagrams/` folder.
"""
from __future__ import annotations

from pathlib import Path

from docx import Document
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.opc.constants import RELATIONSHIP_TYPE as RT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.shared import Cm, Pt, RGBColor

from . import mdparse

FONT, MONO = "Arial", "Courier New"
PAGE_W_CM = 17.0                                   # A4 minus 2 cm margins
ALERTS = {
    "NOTE": ("Примечание", "EAF2FB", "2F6FB5"),
    "TIP": ("Совет", "E8F5E9", "2E7D32"),
    "IMPORTANT": ("Важно", "F1EAFB", "6A3FB5"),
    "WARNING": ("Внимание", "FFF4D6", "B26A00"),
    "CAUTION": ("Осторожно", "FDECEA", "B3261E"),
    None: ("", "F5F5F5", "9E9E9E"),
}


class Ctx:
    """Per-document render context."""

    def __init__(self, doc, resolve_link=None, diagrams=None):
        self.doc = doc
        self.resolve_link = resolve_link or (lambda s: (None, None))   # span -> (url, label_override)
        self.diagrams = diagrams or {}                                  # mermaid index -> Diagram
        self.figure = 0


# ---------------------------------------------------------------- low-level helpers

def _shade(cell, hex_fill: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_fill)
    tc_pr.append(shd)


def _cell_borders(cell, left_color: str):
    tc_pr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for edge, size, color in (("top", "4", "DDDDDD"), ("bottom", "4", "DDDDDD"),
                              ("right", "4", "DDDDDD"), ("left", "24", left_color)):
        el = OxmlElement(f"w:{edge}")
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), size)
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tc_pr.append(borders)


def _style_run(run, s: dict, size: float | None = None, color: str | None = None):
    run.bold = True if s.get("b") else None
    run.italic = True if s.get("i") else None
    if s.get("code"):
        run.font.name = MONO
        rpr = run._r.get_or_add_rPr()
        fonts = rpr.find(qn("w:rFonts"))
        if fonts is None:
            fonts = OxmlElement("w:rFonts")
            rpr.append(fonts)
        for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            fonts.set(qn(attr), MONO)
        run.font.color.rgb = RGBColor(0x8A, 0x1C, 0x4A)
    if size:
        run.font.size = Pt(size - 0.5 if s.get("code") else size)
    if color:
        run.font.color.rgb = RGBColor.from_string(color)


def _hyperlink(par, url: str, s: dict, size: float | None):
    r_id = par.part.relate_to(url, RT.HYPERLINK, is_external=True)
    link = OxmlElement("w:hyperlink")
    link.set(qn("r:id"), r_id)
    run = par.add_run(s["text"])
    _style_run(run, s, size)
    run.font.color.rgb = RGBColor(0x11, 0x55, 0xCC)
    run.font.underline = True
    link.append(run._r)                              # move the run under the hyperlink element
    par._p.append(link)


def add_inline(ctx: Ctx, par, inl: list[dict], size: float | None = None, bold: bool = False):
    for s in inl:
        if not s["text"]:
            continue
        s = dict(s, b=s["b"] or bold)
        url, label = None, None
        if s.get("href") or s.get("wiki"):
            url, label = ctx.resolve_link(s)
            if label:
                s["text"] = label
        if url:
            _hyperlink(par, url, s, size)
        else:
            if s.get("wiki"):
                s["i"] = True                        # unresolved cross-reference: keep it visible
            _style_run(par.add_run(s["text"]), s, size)


def _para(container, style: str | None = None):
    try:
        return container.add_paragraph(style=style) if style else container.add_paragraph()
    except KeyError:
        return container.add_paragraph()


# ---------------------------------------------------------------- blocks

def render_blocks(ctx: Ctx, container, blocks: list[dict], size: float = 10.5, in_cell: bool = False):
    first = in_cell
    for b in blocks:
        t = b["t"]
        if t == "h":
            if in_cell:
                p = _reuse(container, first)
                add_inline(ctx, p, b["inl"], size, bold=True)
            else:
                lvl = min(max(b["level"], 1), 6)
                if lvl == 1:
                    p = container.add_paragraph(style="Title")
                else:
                    p = container.add_heading(level=min(lvl - 1, 4))
                add_inline(ctx, p, b["inl"])
        elif t == "p":
            p = _reuse(container, first)
            add_inline(ctx, p, b["inl"], size)
        elif t == "list":
            _render_list(ctx, container, b, size, 0)
        elif t == "code":
            _render_code(container, b["text"], first)
        elif t == "table":
            _render_table(ctx, container, b)
        elif t == "quote":
            _render_alert(ctx, container, b)
        elif t == "mermaid":
            _render_diagram(ctx, container, b)
        elif t == "hr":
            pass
        first = False


def _reuse(container, first: bool):
    """A fresh table cell already holds one empty paragraph — reuse it for the first block."""
    if first and len(container.paragraphs) == 1 and not container.paragraphs[0].text:
        return container.paragraphs[0]
    return container.add_paragraph()


def _render_list(ctx: Ctx, container, block: dict, size: float, depth: int):
    base = "List Number" if block["ordered"] else "List Bullet"
    style = base if depth == 0 else f"{base} {min(depth + 1, 3)}"
    for item in block["items"]:
        p = _para(container, style)
        add_inline(ctx, p, item["inl"], size)
        for child in item["children"]:
            _render_list(ctx, container, child, size, depth + 1)


def _render_code(container, text: str, first: bool):
    table_host = container
    tbl = table_host.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    _shade(cell, "F6F8FA")
    _cell_borders(cell, "B0B7C0")
    p = cell.paragraphs[0]
    lines = text.split("\n")
    for k, line in enumerate(lines):
        run = p.add_run(line)
        _style_run(run, {"code": True}, 9)
        run.font.color.rgb = RGBColor(0x24, 0x29, 0x2E)
        if k < len(lines) - 1:
            run.add_break()
    if hasattr(container, "add_paragraph"):
        container.add_paragraph()


def _col_widths(block: dict) -> list[float]:
    cols = len(block["head"])
    weights = []
    for c in range(cols):
        cells = [block["head"][c]] + [r[c] for r in block["rows"] if c < len(r)]
        longest = max((len(mdparse.plain(x)) for x in cells), default=1)
        weights.append(min(max(longest, 6), 60))
    total = sum(weights) or 1
    return [PAGE_W_CM * w / total for w in weights]


def _render_table(ctx: Ctx, container, block: dict):
    cols = len(block["head"])
    if cols == 0:
        return
    tbl = container.add_table(rows=1, cols=cols)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    size = 9 if cols <= 4 else 8
    widths = _col_widths(block)
    for c, inl in enumerate(block["head"]):
        cell = tbl.rows[0].cells[c]
        cell.width = Cm(widths[c])
        _shade(cell, "DCE6F2")
        add_inline(ctx, cell.paragraphs[0], inl, size, bold=True)
    for row in block["rows"]:
        cells = tbl.add_row().cells
        for c in range(cols):
            cells[c].width = Cm(widths[c])
            if c < len(row):
                add_inline(ctx, cells[c].paragraphs[0], row[c], size)
    tr_pr = tbl.rows[0]._tr.get_or_add_trPr()        # repeat the header row on each page
    hdr = OxmlElement("w:tblHeader")
    hdr.set(qn("w:val"), "true")
    tr_pr.append(hdr)
    if hasattr(container, "add_paragraph"):
        container.add_paragraph()


def _render_alert(ctx: Ctx, container, block: dict):
    label, fill, edge = ALERTS.get(block["kind"], ALERTS[None])
    tbl = container.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.rows[0].cells[0]
    _shade(cell, fill)
    _cell_borders(cell, edge)
    blocks = block["blocks"]
    if label:
        p = cell.paragraphs[0]
        run = p.add_run(label)
        run.bold = True
        run.font.size = Pt(10)
        run.font.color.rgb = RGBColor.from_string(edge)
    render_blocks(ctx, cell, blocks, size=10, in_cell=True)   # non-empty first paragraph is kept
    if hasattr(container, "add_paragraph"):
        container.add_paragraph()


def _render_diagram(ctx: Ctx, container, block: dict):
    d = ctx.diagrams.get(block["index"])
    if d is None or d.png is None:
        _render_code(container, block["text"], False)
        return
    ctx.figure += 1
    p = container.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    width_cm = min(PAGE_W_CM, d.width / 96 * 2.54)   # natural size, capped to the page width
    p.add_run().add_picture(str(d.png), width=Cm(width_cm))
    cap = container.add_paragraph()
    cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = cap.add_run(f"Схема {ctx.figure}. {d.title} — исходники: diagrams/{d.name}.svg, "
                      f"diagrams/{d.name}.drawio")
    run.italic = True
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(0x60, 0x60, 0x60)


# ---------------------------------------------------------------- document

def _base_document(title: str, header_text: str, footer_text: str):
    doc = Document()
    sec = doc.sections[0]
    sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)
    sec.left_margin = sec.right_margin = Cm(2.0)
    sec.top_margin = sec.bottom_margin = Cm(2.0)
    normal = doc.styles["Normal"]
    normal.font.name = FONT
    normal.font.size = Pt(10.5)
    normal.element.rPr.rFonts.set(qn("w:eastAsia"), FONT)
    for name in ("Title", "Heading 1", "Heading 2", "Heading 3", "Heading 4"):
        st = doc.styles[name]
        st.font.name = FONT
        rpr = st.element.get_or_add_rPr()
        fonts = rpr.find(qn("w:rFonts"))
        if fonts is None:
            fonts = OxmlElement("w:rFonts")
            rpr.append(fonts)
        for attr in ("w:ascii", "w:hAnsi", "w:cs", "w:eastAsia"):
            fonts.set(qn(attr), FONT)
        st.font.color.rgb = RGBColor(0x1F, 0x2A, 0x44)
    doc.styles["Title"].font.size = Pt(22)
    for text, part in ((header_text, sec.header), (footer_text, sec.footer)):
        p = part.paragraphs[0]
        run = p.add_run(text)
        run.font.size = Pt(8)
        run.font.color.rgb = RGBColor(0x70, 0x70, 0x70)
    doc.core_properties.title = title
    return doc


def meta_table(ctx: Ctx, rows: list[tuple[str, str]]):
    tbl = ctx.doc.add_table(rows=0, cols=2)
    tbl.style = "Table Grid"
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    for key, value in rows:
        cells = tbl.add_row().cells
        cells[0].width, cells[1].width = Cm(4.0), Cm(PAGE_W_CM - 4.0)
        _shade(cells[0], "EEF2F7")
        r = cells[0].paragraphs[0].add_run(key)
        r.bold = True
        r.font.size = Pt(9)
        add_inline(ctx, cells[1].paragraphs[0], mdparse.parse_inline(value), 9)
    ctx.doc.add_paragraph()


def build_document(path: Path, *, title: str, version: str, meta_rows: list[tuple[str, str]],
                   blocks: list[dict], header: str, author: str = "", resolve_link=None,
                   diagrams=None) -> Path:
    """Write one document. The version is shown in the metadata table, the footer and the file
    properties."""
    doc = _base_document(title, header, f"{title} · версия {version}")
    doc.core_properties.author = author or ""
    doc.core_properties.version = str(version)
    ctx = Ctx(doc, resolve_link, diagrams)
    body = list(blocks)
    if body and body[0]["t"] == "h" and body[0]["level"] == 1:
        render_blocks(ctx, doc, [body.pop(0)])
    else:
        doc.add_paragraph(title, style="Title")
    meta_table(ctx, meta_rows)
    render_blocks(ctx, doc, body)
    path.parent.mkdir(parents=True, exist_ok=True)
    doc.save(str(path))
    return path
