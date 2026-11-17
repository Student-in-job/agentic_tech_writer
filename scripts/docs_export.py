#!/usr/bin/env python3
"""docs_export — scan approved docs of a service/project and export them to a destination.

    python scripts/docs_export.py <type> <source> <destination> [--dry-run] [--links FILE]

  type         gdocs | pdf | notion | confluence
  source       a service or project name from docs/registry.yaml
  destination  gdocs      -> a Google Drive folder reachable through Google Drive for desktop:
                             absolute path, path under the Drive mount, or a folder name
               pdf        -> a local directory
               notion /
               confluence -> a label of the target (parent page / space); recorded in the
                             manifest for the agent that performs the MCP transport

Layout written under the destination (one tree per service):

    docs/<project>/services/<service>/
        <service> — оглавление.<ext>          table of contents with links
        <Type>/<document>.<ext>               one folder per document type (API, Architecture, …)
        diagrams/<diagram>.drawio|.svg        diagram sources

What each type does:
  gdocs       builds .docx (Google Docs opens them natively) and copies the tree into the
              synced Drive folder. Links between documents need Drive URLs, which only exist
              after the sync: resolve them (agent, via the Drive MCP) into a JSON file
              {"<path under docs/…>": {"id": "...", "url": "..."}} and re-run with --links.
  pdf         builds PDFs (headless Chrome) into the destination directory.
  notion /
  confluence  builds a transport bundle in out/export/<type>/<source>/ (normalised Markdown +
              rendered diagrams + manifest.json). The actual create/update is done by the
              agent through the configured MCP (see .claude/commands/docs-export.md).

Everything is first built in out/export/<type>/<source>/ (gitignored) and only then copied.
State (ids / urls / versions) is kept in publish/publish-map.yaml.
"""
from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import shutil
import sys
import urllib.parse
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

from export_lib import diagrams as dg          # noqa: E402
from export_lib import mdparse                 # noqa: E402

DOCS = ROOT / "docs"
REGISTRY = DOCS / "registry.yaml"
STAGING = ROOT / "out" / "export"
MAP_FILE = ROOT / "publish" / "publish-map.yaml"
EXPORTER_VERSION = "1"

TYPES = ("gdocs", "pdf", "notion", "confluence")
EXT = {"gdocs": ".docx", "pdf": ".pdf", "notion": ".md", "confluence": ".md"}
FOLDER_NAMES = {"api": "API", "adr": "ADR", "architecture": "Architecture", "requirements": "Requirements",
                "readme": "Readme", "ops": "Ops", "release": "Release", "user": "User", "partner": "Partner"}
SKIP_FILES = {"index.md", "coverage.md"}            # aggregation pages, not documents
MAP_HEADER = ("# publish-map — state for idempotent MD -> KB publishing / export.\n"
              "# Written by the doc-publish skill and scripts/docs_export.py. No secrets here: ids/urls only.\n"
              "# Key = repo-relative path of the canonical .md (or '<service dir>/#index', '#diagram/<name>').\n\n")


# ------------------------------------------------------------------ helpers

def load_frontmatter(path: Path) -> tuple[dict, str]:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {}, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return {}, text
    meta = yaml.safe_load(parts[1]) or {}
    return (meta if isinstance(meta, dict) else {}), parts[2].lstrip("\n")


def folder_name(part: str) -> str:
    return FOLDER_NAMES.get(part.lower(), part[:1].upper() + part[1:])


def version_label(meta: dict) -> str:
    """Every exported document shows a version. Numbered docs use `version`; docs that are
    versioned with the service code fall back to the schema snapshot or the revision date."""
    v = meta.get("version")
    if v not in (None, ""):
        return str(v)
    if meta.get("schema_version"):
        return f"схема {meta['schema_version']}"
    if meta.get("last_verified_commit"):
        return f"по коду @{str(meta['last_verified_commit'])[:10]}"
    return f"ред. {meta.get('updated') or meta.get('created') or 'n/a'}"


def rel(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


# ------------------------------------------------------------------ scanning

class Doc:
    def __init__(self, path: Path, service: str, service_dir: Path):
        self.path = path
        self.service = service
        self.meta, self.body = load_frontmatter(path)
        self.key = rel(path)
        self.stem = path.stem
        self.title = str(self.meta.get("title") or self.stem)
        self.version = version_label(self.meta)
        parts = path.relative_to(service_dir).parts[:-1]
        self.folders = [folder_name(p) for p in parts]            # e.g. ["Architecture", "ADR"]
        self.blocks = mdparse.parse(self.body)
        self.diagrams: dict[int, dg.Diagram] = {}

    def aliases(self) -> set[str]:
        a = {self.stem, f"{self.service}-{self.stem}"}
        if self.stem.startswith("service-"):
            a.add(f"{self.service}-{self.stem[len('service-'):]}")
        for extra in (self.meta.get("aliases") or []):
            a.add(str(extra))
        if self.meta.get("id"):
            a.add(str(self.meta["id"]))
        return {x.lower() for x in a}

    def dest_rel(self, base: str, ext: str) -> str:
        return "/".join([base, *self.folders, self.stem + ext])


def scan_service(service: str) -> list[Doc]:
    sdir = DOCS / "services" / service
    docs = []
    if not sdir.is_dir():
        return docs
    for p in sorted(sdir.rglob("*.md")):
        if p.name in SKIP_FILES and p.parent == sdir:
            continue
        d = Doc(p, service, sdir)
        if not d.meta.get("template") and p.parent == sdir:
            continue
        status = str(d.meta.get("status") or "").lower()
        if status in ("draft", "deprecated", "superseded"):
            continue
        docs.append(d)
    return docs


def resolve_source(source: str, registry: dict) -> tuple[str, list[str]]:
    """-> (project, [services]). A service name selects one service; a project name all members."""
    services, projects = registry.get("services", {}), registry.get("projects", {})
    if source in services:
        return str(services[source].get("project") or "_unassigned"), [source]
    if source in projects:
        return source, list(projects[source].get("services") or [])
    sys.exit(f"'{source}' is neither a service nor a project in docs/registry.yaml. "
             f"Services: {', '.join(services)}. Projects: {', '.join(projects)}.")


def attach_diagrams(doc: Doc):
    """Name every mermaid block: <stem>-<NN>-<kind>, captioned by the nearest heading above it."""
    heading = doc.title

    def walk(blocks):
        nonlocal heading
        for b in blocks:
            if b["t"] == "h":
                heading = re.sub(r"^(§\s*)?\d+(\.\d+)*[.)]?\s+", "", mdparse.plain(b["inl"]))   # drop "1. "
            elif b["t"] == "quote":
                walk(b["blocks"])
            elif b["t"] == "mermaid":
                kind = dg.kind_of(b["text"])
                name = f"{doc.stem}-{b['index']:02d}-{slug(kind)}"
                doc.diagrams[b["index"]] = dg.Diagram(name=name, kind=kind, title=heading, source=b["text"])
    walk(doc.blocks)


# ------------------------------------------------------------------ destination

def drive_roots() -> list[Path]:
    roots = []
    env = os.environ.get("GDRIVE_ROOT")
    if env:
        roots.append(Path(env))
    if os.name == "nt":
        for letter in "GHIJKLMNOPQRSTUVWXYZDEF":
            for name in ("My Drive", "Мой диск"):
                p = Path(f"{letter}:/{name}")
                if p.is_dir():
                    roots.append(p)
    else:
        home = Path.home()
        roots += [p for p in (home / "Google Drive" / "My Drive", home / "Google Drive") if p.is_dir()]
        cloud = home / "Library" / "CloudStorage"
        if cloud.is_dir():
            roots += [p / "My Drive" for p in cloud.glob("GoogleDrive-*") if (p / "My Drive").is_dir()]
    return roots


def resolve_drive_destination(dest: str) -> Path:
    p = Path(dest)
    if p.is_absolute():
        if not p.is_dir():
            sys.exit(f"Destination folder does not exist: {p}")
        return p
    roots = drive_roots()
    if not roots:
        sys.exit("Google Drive for desktop mount not found. Install/sign in, or set GDRIVE_ROOT, "
                 "or pass an absolute path.")
    for r in roots:
        if (r / dest).is_dir():
            return r / dest
    for r in roots:                                   # search by folder name, 3 levels deep
        level = [r]
        for _ in range(3):
            nxt = []
            for d in level:
                try:
                    for c in d.iterdir():
                        if c.is_dir() and not c.name.startswith((".", "$")):
                            if c.name == dest:
                                return c
                            nxt.append(c)
                except OSError:
                    continue
            level = nxt
    sys.exit(f"Folder '{dest}' not found under {', '.join(map(str, roots))}.")


# ------------------------------------------------------------------ state (publish-map)

def load_map() -> dict:
    if MAP_FILE.exists():
        return yaml.safe_load(MAP_FILE.read_text(encoding="utf-8")) or {}
    return {}


def save_map(data: dict):
    MAP_FILE.write_text(MAP_HEADER + yaml.safe_dump(data, allow_unicode=True, sort_keys=True, width=120),
                        encoding="utf-8")


def merge_links(pmap: dict, backend: str, links_file: Path) -> int:
    """links JSON: {"docs/<project>/services/<svc>/API/api-contract.docx": {"id","url"} | "<id>", …}."""
    links = json.loads(links_file.read_text(encoding="utf-8"))
    by_path = {v[backend]["path"]: k for k, v in pmap.items()
               if isinstance(v, dict) and backend in v and v[backend].get("path")}
    n = 0
    for path, info in links.items():
        if isinstance(info, str):                     # short form: {path: "<file id>"}
            info = {"id": info}
        if info.get("id") and not info.get("url") and backend == "gdocs":
            info["url"] = f"https://drive.google.com/file/d/{info['id']}/view"
        key = by_path.get(path.replace("\\", "/"))
        if key and info.get("url"):
            pmap[key][backend].update({k: info[k] for k in ("id", "url") if info.get(k)})
            n += 1
    return n


# ------------------------------------------------------------------ export

def meta_rows(doc: Doc, project: str, today: str) -> list[tuple[str, str]]:
    m = doc.meta
    rows = [("Версия", doc.version), ("Статус", str(m.get("status") or "—")),
            ("Обновлён", str(m.get("updated") or "—")), ("Владелец", str(m.get("owner") or "—")),
            ("Сервис / проект", f"{doc.service} / {project}")]
    if m.get("applies_to"):
        rows.append(("Описывает", f"`{m['applies_to']}`"))
    if getattr(doc, "generated", False):
        rows.append(("Источник", f"сгенерировано из `docs/services/{doc.service}/`"))
    else:
        rows.append(("Источник", f"`{doc.key}` (канонический Markdown)"))
    rows.append(("Экспорт", today))
    return rows


def make_resolver(doc: Doc, alias_index: dict[str, Doc], url_of):
    def resolve(span: dict):
        if span.get("wiki"):
            target = alias_index.get(span["wiki"].lower())
            return (url_of(target.key), None) if target else (None, None)
        href = span.get("href") or ""
        if re.match(r"^(https?:|mailto:)", href):
            return href, None
        if href.split("#")[0].endswith(".md"):
            try:
                target = (doc.path.parent / href.split("#")[0]).resolve()
                return url_of(rel(target)), None
            except (ValueError, OSError):
                return None, None
        return None, None
    return resolve


def index_markdown(service: str, project: str, docs: list[Doc], base: str, ext: str, url_of, card: dict) -> str:
    def cell(text: str) -> str:
        return text.replace("|", "\\|")

    def link(text: str, key: str) -> str:
        url = url_of(key)
        return f"[{cell(text)}]({url})" if url else cell(text)

    lines = [f"# {service} — оглавление документации", ""]
    if card.get("bounded_context"):
        lines += [str(card["bounded_context"]).strip(), ""]
    lines += ["## Документы", "", "| Раздел | Документ | Версия | Статус | Обновлён | Файл |",
              "|---|---|---|---|---|---|"]
    for d in sorted(docs, key=lambda d: (d.folders, d.stem)):
        path = d.dest_rel(base, ext)[len(base) + 1:]
        lines.append(f"| {cell(' / '.join(d.folders))} | {link(d.title, d.key)} | {cell(d.version)} | "
                     f"{d.meta.get('status') or '—'} | {d.meta.get('updated') or '—'} | `{path}` |")
    figures = [(d, g) for d in docs for g in d.diagrams.values()]
    if figures:
        sdir = f"docs/services/{service}"
        lines += ["", "## Схемы", "", "| Схема | Документ | draw.io | SVG |", "|---|---|---|---|"]
        for d, g in figures:
            lines.append(f"| {cell(g.title)} | {link(d.title, d.key)} | "
                         f"{link(g.name + '.drawio', f'{sdir}/#diagram/{g.name}.drawio')} | "
                         f"{link(g.name + '.svg', f'{sdir}/#diagram/{g.name}.svg')} |")
    lines += ["", "> [!NOTE]", "> Канонический источник — Markdown в репозитории документации. Эти файлы — "
              "экспортированная копия; правки вносятся в Markdown и экспортируются заново.", ""]
    return "\n".join(lines)


def export(args) -> int:
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    project, services = resolve_source(args.source, registry)
    kind, ext = args.type, EXT[args.type]
    today = dt.date.today().isoformat()
    now = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    dest_root: Path | None = None
    if kind == "gdocs":
        dest_root = resolve_drive_destination(args.destination)
    elif kind == "pdf":
        dest_root = Path(args.destination).expanduser()
        if not dest_root.is_absolute():
            dest_root = (Path.cwd() / dest_root)

    pdf_links = kind == "pdf" and _have_pymupdf()            # without PyMuPDF PDFs carry no cross-links
    pmap = load_map()
    if args.links:
        n = merge_links(pmap, kind, Path(args.links))
        print(f"links: {n} url(s) recorded from {args.links}")

    def url_of(key: str, frm: str | None = None):
        entry = (pmap.get(key) or {}).get(kind) or {}
        if kind == "pdf":                                    # PDFs link to each other by relative path
            if not (frm and entry.get("path") and pdf_links):
                return None
            relpath = os.path.relpath(entry["path"], os.path.dirname(frm)).replace(os.sep, "/")
            return urllib.parse.quote(relpath)
        return entry.get("url")

    all_docs: dict[str, list[Doc]] = {s: scan_service(s) for s in services}
    alias_index: dict[str, Doc] = {}
    for s in registry.get("services", {}):            # cross-service links resolve too
        for d in (all_docs.get(s) or scan_service(s)):
            for a in d.aliases():
                alias_index.setdefault(a, d)

    stage = STAGING / kind / args.source
    manifest = {"type": kind, "source": args.source, "project": project, "generated_at": now,
                "destination": str(dest_root) if dest_root else args.destination,
                "services": [], "skipped": []}
    plan: list[tuple[Path, str]] = []                 # (staged file, path under destination)
    if not args.dry_run and stage.exists():
        shutil.rmtree(stage, ignore_errors=True)      # staging is rebuilt from scratch every run

    for service in services:
        docs = all_docs[service]
        if not docs:
            manifest["skipped"].append({"service": service, "reason": "no approved documents"})
            print(f"skip  {service}: no approved documents (only a service card)")
            continue
        base = f"docs/{project}/services/{service}"
        sdir_key = f"docs/services/{service}"
        entry = {"service": service, "root": base, "documents": [], "diagrams": [], "index": None}
        for d in docs:
            attach_diagrams(d)
            pmap.setdefault(d.key, {}).setdefault(kind, {})["path"] = d.dest_rel(base, ext)
            for g in d.diagrams.values():
                for suffix in (".drawio", ".svg"):
                    pmap.setdefault(f"{sdir_key}/#diagram/{g.name}{suffix}", {}).setdefault(kind, {})["path"] =                         f"{base}/diagrams/{g.name}{suffix}"
        pmap.setdefault(f"{sdir_key}/#index", {}).setdefault(kind, {})["path"] =             f"{base}/{service} — оглавление{ext}"
        print(f"\n{service}: {len(docs)} document(s), "
              f"{sum(len(d.diagrams) for d in docs)} diagram(s)  ->  {base}/")
        for d in docs:
            print(f"  {d.dest_rel(base, ext)[len(base) + 1:]:55} {d.version}")
        if args.dry_run:
            continue

        ddir = stage / base / "diagrams"
        browser = None
        for d in docs:
            for g in d.diagrams.values():
                browser = browser or dg.find_browser()
                dg.render(g, STAGING / "_diagram-cache" / service, browser)
                ddir.mkdir(parents=True, exist_ok=True)
                for src, suffix in ((g.drawio, ".drawio"), (g.svg, ".svg")):
                    out = ddir / f"{g.name}{suffix}"
                    shutil.copyfile(src, out)
                    relp = f"{base}/diagrams/{g.name}{suffix}"
                    plan.append((out, relp))
                    key = f"{sdir_key}/#diagram/{g.name}{suffix}"
                    pmap.setdefault(key, {}).setdefault(kind, {}).update({"path": relp, "published_at": now})
                entry["diagrams"].append({"name": g.name, "kind": g.kind, "title": g.title, "document": d.key})

        for d in docs:
            relp = d.dest_rel(base, ext)
            out = stage / relp
            build_one(kind, out, d, project, today,
                      make_resolver(d, alias_index, lambda key, _f=relp: url_of(key, _f)))
            plan.append((out, relp))
            pmap.setdefault(d.key, {}).setdefault(kind, {}).update(
                {"path": relp, "doc_version": d.version, "published_at": now})
            entry["documents"].append({"source": d.key, "title": d.title, "version": d.version,
                                       "status": d.meta.get("status"), "path": relp, "url": url_of(d.key)})

        # table of contents
        card = (registry.get("services") or {}).get(service) or {}
        idx_name = f"{service} — оглавление{ext}"
        idx_rel = f"{base}/{idx_name}"
        idx_md = index_markdown(service, project, docs, base, ext, lambda key: url_of(key, idx_rel), card)
        idx_doc = _IndexDoc(service, idx_md, today, project)
        build_one(kind, stage / idx_rel, idx_doc, project, today,
                  lambda s: (s.get("href") or None, None), index=True)   # links are already resolved
        plan.append((stage / idx_rel, idx_rel))
        pmap.setdefault(f"{sdir_key}/#index", {}).setdefault(kind, {}).update(
            {"path": idx_rel, "doc_version": today, "published_at": now})
        entry["index"] = {"path": idx_rel, "url": url_of(f"{sdir_key}/#index")}
        entry["links_resolved"] = sum(1 for x in entry["documents"] if x["url"])
        manifest["services"].append(entry)

    if args.dry_run:
        print("\ndry-run: nothing built, nothing written.")
        return 0

    stage.mkdir(parents=True, exist_ok=True)
    (stage / "manifest.json").write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    save_map(pmap)

    if dest_root is not None:
        state_file = STAGING / f".state-{kind}-{slug(args.source)}.json"
        state = json.loads(state_file.read_text(encoding="utf-8")) if state_file.exists() else {}
        copied = unchanged = 0
        for staged, relp in plan:
            digest = _content_digest(staged)
            target = dest_root / relp
            if state.get(relp) == digest and target.exists():
                unchanged += 1
                continue
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(staged, target)           # overwrite in place: the Drive file id is kept
            state[relp] = digest
            copied += 1
        # Files this exporter wrote earlier that are no longer produced (renamed diagram, removed doc).
        planned = {relp for _, relp in plan}
        roots = tuple(s["root"] + "/" for s in manifest["services"])
        stale = sorted(r for r in state if r not in planned and r.startswith(roots))
        for relp in stale:
            if not args.prune:
                continue
            target = dest_root / relp
            if target.exists():
                target.unlink()                       # in a Drive folder this moves the file to the Drive trash
            state.pop(relp, None)
            for key in [k for k, v in pmap.items() if (v.get(kind) or {}).get("path") == relp]:
                pmap[key].pop(kind, None)
                if not pmap[key]:
                    pmap.pop(key)
        if stale:
            verb = "removed" if args.prune else "left in place (re-run with --prune to remove)"
            print(f"stale files {verb}:")
            for r in stale:
                print(f"  {r}")
            if args.prune:
                save_map(pmap)
        state_file.write_text(json.dumps(state, ensure_ascii=False, indent=1), encoding="utf-8")
        print(f"\nwritten to {dest_root}: {copied} file(s) copied, {unchanged} unchanged")
    else:
        print(f"\nbundle ready: {rel(stage)} (transport is done by the agent via MCP)")
    print(f"manifest: {rel(stage / 'manifest.json')}")
    unresolved = [x["path"] for s in manifest["services"] for x in s["documents"] if not x["url"]]
    if kind == "gdocs" and unresolved:
        print(f"note: {len(unresolved)} document(s) have no Drive URL yet — resolve them and re-run with --links.")
    return 0


class _IndexDoc:
    """Duck-typed Doc for the generated table of contents."""

    def __init__(self, service: str, md: str, today: str, project: str):
        self.service, self.body, self.key = service, md, f"docs/services/{service}/#index"
        self.generated = True
        self.title = f"{service} — оглавление документации"
        self.version = today
        self.meta = {"status": "generated", "updated": today, "owner": "doc-tooling"}
        self.blocks = mdparse.parse(md)
        self.diagrams = {}


def _content_digest(path: Path) -> str:
    """Stable digest: .docx is a zip with timestamps, so hash its XML/media members instead."""
    h = hashlib.sha256()
    if path.suffix == ".docx":
        import zipfile
        with zipfile.ZipFile(path) as z:
            for name in sorted(z.namelist()):
                if name == "docProps/core.xml":
                    continue
                h.update(name.encode())
                h.update(z.read(name))
    elif path.suffix == ".pdf":
        data = path.read_bytes()
        data = re.sub(rb"/(CreationDate|ModDate) ?\([^)]*\)", b"", data)
        h.update(re.sub(rb"/ID ?\[[^\]]*\]", b"", data))
    else:
        h.update(path.read_bytes())
    return h.hexdigest()


def _have_pymupdf() -> bool:
    try:
        import pymupdf  # noqa: F401
        return True
    except ImportError:
        return False


def _relativize_pdf_links(pdf: Path):
    """Chrome turns relative hrefs into absolute file:// URLs of the staging folder. Rewrite
    them back to relative URIs so links between exported PDFs survive the copy."""
    import pymupdf
    here = pdf.parent.resolve()
    doc = pymupdf.open(str(pdf))
    changed = False
    for page in doc:
        for link in page.get_links():
            target = link.get("file") or link.get("uri") or ""
            if target.startswith("file:"):
                target = urllib.parse.unquote(urllib.parse.urlparse(target).path)
            if not target.lower().endswith((".pdf", ".svg", ".drawio")) or "://" in target:
                continue
            target_path = Path(target.lstrip("/") if re.match(r"^/[A-Za-z]:", target) else target)
            try:
                relpath = os.path.relpath(target_path, here).replace(os.sep, "/")
            except ValueError:
                continue
            page.delete_link(link)
            page.insert_link({"kind": pymupdf.LINK_URI, "from": link["from"],
                              "uri": urllib.parse.quote(relpath)})
            changed = True
    if changed:
        tmp = pdf.with_suffix(".tmp.pdf")
        doc.save(str(tmp), garbage=3, deflate=True)
        doc.close()
        tmp.replace(pdf)
    else:
        doc.close()


def build_one(kind: str, out: Path, doc, project: str, today: str, resolver, index: bool = False):
    out.parent.mkdir(parents=True, exist_ok=True)
    rows = meta_rows(doc, project, today)
    if kind == "gdocs":
        from export_lib import render_docx
        render_docx.build_document(out, title=doc.title, version=doc.version, meta_rows=rows,
                                   blocks=doc.blocks, header=f"{project} / {doc.service}",
                                   author=str(doc.meta.get("author") or ""), resolve_link=resolver,
                                   diagrams=doc.diagrams)
    elif kind == "pdf":
        from export_lib import render_html
        page = render_html.build_page(title=doc.title, version=doc.version, meta_rows=rows,
                                      blocks=doc.blocks, resolve_link=resolver, diagrams=doc.diagrams)
        html_path = out.with_suffix(".html")
        html_path.write_text(page, encoding="utf-8")
        if out.exists():
            out.unlink()
        dg._run(dg.find_browser(), ["--no-pdf-header-footer", f"--print-to-pdf={out.resolve()}",
                                    html_path.resolve().as_uri()])
        html_path.unlink(missing_ok=True)
        if not out.exists():
            raise RuntimeError(f"PDF was not produced: {out}")
        _relativize_pdf_links(out)
    else:                                             # notion / confluence bundle: normalised Markdown
        table = "\n".join(["| Поле | Значение |", "|---|---|"] + [f"| {k} | {v} |" for k, v in rows])
        body = doc.body
        if not index:
            names = iter(sorted(doc.diagrams.items()))

            def repl(_m):
                try:
                    _, g = next(names)
                    return f"![{g.title}](diagrams/{g.name}.svg)\n"
                except StopIteration:
                    return _m.group(0)
            body = re.sub(r"```mermaid\n.*?```\n?", repl, body, flags=re.S)
        head, _, rest = body.partition("\n")
        text = f"{head}\n\n{table}\n{rest}" if head.startswith("# ") else f"# {doc.title}\n\n{table}\n\n{body}"
        out.write_text(text, encoding="utf-8")


def main() -> int:
    ap = argparse.ArgumentParser(description="Export approved docs of a service/project.",
                                 formatter_class=argparse.RawDescriptionHelpFormatter, epilog=__doc__)
    ap.add_argument("type", choices=TYPES)
    ap.add_argument("source", help="service or project name (docs/registry.yaml)")
    ap.add_argument("destination", help="Drive folder / local directory / target label")
    ap.add_argument("--dry-run", action="store_true", help="print the plan; build and write nothing")
    ap.add_argument("--links", help="JSON {dest path: {id, url}} with resolved URLs of exported files")
    ap.add_argument("--prune", action="store_true",
                    help="remove files written by an earlier export that are no longer produced")
    args = ap.parse_args()
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    return export(args)


if __name__ == "__main__":
    sys.exit(main())
