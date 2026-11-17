"""Mermaid -> SVG / PNG / draw.io.

Rendering uses an **installed** Chrome or Edge in headless mode; nothing is installed. The page
loads a pinned Mermaid build from jsDelivr, so rendering needs network access. Diagram source
never leaves the machine (it is embedded in a local temp HTML file).

Outputs per diagram:
  <name>.svg     standalone vector (explicit width/height)
  <name>.png     2x raster — what DOCX / Google Docs embed (Google Docs cannot display SVG)
  <name>.drawio  draw.io file: the rendered diagram as an image object that carries the Mermaid
                 source in `mermaidData`, so draw.io can reopen it in its Mermaid editor
"""
from __future__ import annotations

import base64
import hashlib
import html
import json
import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

MERMAID_VERSION = "11.4.1"
MERMAID_CDN = f"https://cdn.jsdelivr.net/npm/mermaid@{MERMAID_VERSION}/dist/mermaid.min.js"

_BROWSER_CANDIDATES = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "/usr/bin/google-chrome", "/usr/bin/chromium", "/usr/bin/chromium-browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
]

_PAGE = """<!doctype html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;background:#fff}}</style>
<script src="{cdn}"></script></head><body>
<pre id="src" style="display:none">{src}</pre><div id="out"></div><pre id="res">PENDING</pre>
<script>
(async () => {{
  const res = document.getElementById('res');
  try {{
    mermaid.initialize({{startOnLoad:false, theme:'default', securityLevel:'strict',
      htmlLabels:false, flowchart:{{htmlLabels:false}}, fontFamily:'Arial, Helvetica, sans-serif'}});
    const src = document.getElementById('src').textContent;
    const r = await mermaid.render('dgm', src);
    document.getElementById('out').innerHTML = r.svg;
    const el = document.querySelector('#out svg');
    const box = el.getBoundingClientRect();
    const xml = new XMLSerializer().serializeToString(el);
    res.textContent = 'OK|' + Math.ceil(box.width) + '|' + Math.ceil(box.height) + '|' +
      btoa(unescape(encodeURIComponent(xml)));
  }} catch (e) {{ res.textContent = 'ERR|' + (e && e.message ? e.message : e); }}
}})();
</script></body></html>"""

_SHOT = """<!doctype html><html><head><meta charset="utf-8">
<style>html,body{{margin:0;background:#fff;overflow:hidden}}svg{{display:block}}</style></head>
<body>{svg}</body></html>"""


class DiagramError(RuntimeError):
    pass


@dataclass
class Diagram:
    name: str            # file stem, e.g. c4-architecture-01-c4context
    kind: str            # C4Context / flowchart / erDiagram ...
    title: str           # human caption
    source: str          # mermaid text
    svg: Path | None = None
    png: Path | None = None
    drawio: Path | None = None
    width: int = 0       # CSS px
    height: int = 0


def find_browser() -> str:
    env = os.environ.get("CHROME_PATH")
    if env and Path(env).exists():
        return env
    for c in _BROWSER_CANDIDATES:
        if Path(c).exists():
            return c
    for exe in ("chrome", "google-chrome", "chromium", "msedge"):
        p = shutil.which(exe)
        if p:
            return p
    raise DiagramError("No Chrome/Edge found. Set CHROME_PATH to a Chromium-based browser.")


def _run(browser: str, args: list[str], timeout: int = 90) -> bytes:
    with tempfile.TemporaryDirectory(prefix="docs_export_chrome_") as profile:
        cmd = [browser, "--headless=new", "--disable-gpu", "--no-first-run", "--disable-extensions",
               "--hide-scrollbars", f"--user-data-dir={profile}", *args]
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
        return proc.stdout


def kind_of(source: str) -> str:
    for line in source.splitlines():
        s = line.strip()
        if s and not s.startswith("%%"):
            return re.split(r"[\s;]", s, maxsplit=1)[0]
    return "diagram"


def _fix_svg(xml: str, width: int, height: int) -> str:
    """Make the SVG standalone: explicit pixel size instead of width=100% / max-width."""
    m = re.search(r'viewBox="([\d.\-eE ]+)"', xml)
    if m:
        parts = m.group(1).split()
        if len(parts) == 4:
            width, height = int(float(parts[2]) + 0.999), int(float(parts[3]) + 0.999)
    head_end = xml.index(">")
    head = xml[:head_end]
    head = re.sub(r'\swidth="[^"]*"', "", head)
    head = re.sub(r'\sheight="[^"]*"', "", head)
    head = re.sub(r'\sstyle="[^"]*"', "", head)
    head += f' width="{width}" height="{height}" style="background:#ffffff"'
    return head + xml[head_end:], width, height


def render(d: Diagram, out_dir: Path, browser: str | None = None, cache: bool = True) -> Diagram:
    """Render one diagram into out_dir (svg + png + drawio). Cached by source hash."""
    out_dir = out_dir.resolve()      # Chrome needs an absolute --screenshot path
    out_dir.mkdir(parents=True, exist_ok=True)
    browser = browser or find_browser()
    digest = hashlib.sha256((MERMAID_VERSION + "\n" + d.source).encode("utf-8")).hexdigest()[:16]
    svg_p, png_p, dio_p = (out_dir / f"{d.name}{ext}" for ext in (".svg", ".png", ".drawio"))
    stamp = out_dir / f".{d.name}.hash"
    if cache and stamp.exists() and stamp.read_text() == digest and svg_p.exists() and png_p.exists():
        xml = svg_p.read_text(encoding="utf-8")
        m = re.search(r' width="(\d+)" height="(\d+)"', xml)
        d.width, d.height = (int(m.group(1)), int(m.group(2))) if m else (800, 600)
    else:
        with tempfile.TemporaryDirectory(prefix="docs_export_mmd_") as tmp:
            page = Path(tmp) / "render.html"
            page.write_text(_PAGE.format(cdn=MERMAID_CDN, src=html.escape(d.source)), encoding="utf-8")
            dom = _run(browser, ["--virtual-time-budget=20000", "--dump-dom", page.as_uri()])
            text = dom.decode("utf-8", errors="replace")
            m = re.search(r'<pre id="res">([^<]*)</pre>', text)
            if not m or m.group(1).startswith("PENDING"):
                raise DiagramError(f"{d.name}: Mermaid did not render (no network to the CDN, or timeout).")
            res = html.unescape(m.group(1))
            if res.startswith("ERR|"):
                raise DiagramError(f"{d.name}: Mermaid error: {res[4:]}")
            _, w, h, b64 = res.split("|", 3)
            xml = base64.b64decode(b64).decode("utf-8")
            xml, d.width, d.height = _fix_svg(xml, int(w), int(h))
            svg_p.write_text(xml, encoding="utf-8")
            shot = Path(tmp) / "shot.html"
            shot.write_text(_SHOT.format(svg=xml), encoding="utf-8")
            if png_p.exists():
                png_p.unlink()
            _run(browser, [f"--window-size={d.width},{d.height}", "--force-device-scale-factor=2",
                           "--default-background-color=FFFFFFFF", f"--screenshot={png_p}", shot.as_uri()])
            if not png_p.exists():
                raise DiagramError(f"{d.name}: PNG screenshot was not produced.")
        stamp.write_text(digest)
    dio_p.write_text(to_drawio(d, svg_p.read_text(encoding="utf-8")), encoding="utf-8")
    d.svg, d.png, d.drawio = svg_p, png_p, dio_p
    return d


def to_drawio(d: Diagram, svg_xml: str) -> str:
    """A .drawio file holding the diagram as an image object with its Mermaid source attached."""
    esc = lambda s: html.escape(s, quote=True)  # noqa: E731
    b64 = base64.b64encode(svg_xml.encode("utf-8")).decode("ascii")
    mermaid_data = json.dumps({"data": d.source, "config": {"theme": "default"}}, ensure_ascii=False)
    style = ("shape=image;noLabel=1;verticalAlign=top;aspect=fixed;imageAspect=0;"
             f"image=data:image/svg+xml,{b64};")
    w, h = d.width or 800, d.height or 600
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<mxfile host="docs_export" agent="local_documentation/scripts/docs_export.py" version="24.7.17" type="device">\n'
        f'  <diagram id="{esc(d.name)}" name="{esc(d.title or d.name)}">\n'
        f'    <mxGraphModel dx="{w + 80}" dy="{h + 80}" grid="1" gridSize="10" guides="1" tooltips="1" connect="1" '
        f'arrows="1" fold="1" page="1" pageScale="1" pageWidth="{w + 40}" pageHeight="{h + 40}" math="0" shadow="0">\n'
        '      <root>\n        <mxCell id="0"/>\n        <mxCell id="1" parent="0"/>\n'
        f'        <UserObject label="" mermaidData="{esc(mermaid_data)}" id="2">\n'
        f'          <mxCell style="{esc(style)}" vertex="1" parent="1">\n'
        f'            <mxGeometry x="20" y="20" width="{w}" height="{h}" as="geometry"/>\n'
        '          </mxCell>\n        </UserObject>\n'
        '      </root>\n    </mxGraphModel>\n  </diagram>\n</mxfile>\n'
    )
