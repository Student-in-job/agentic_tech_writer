#!/usr/bin/env python3
"""Documentation coverage for a service (or project).

Compares the EXPECTED document set — the coverage profile filtered by the service's facets —
against what actually exists in docs/ and drafts/, and prints a Markdown report.

Expected set:  templates/coverage-profile.yaml  ∩  registry facets
Actual set:    frontmatter `template:` + `status:` of docs under docs/ and drafts/

Usage:
  python scripts/doc_coverage.py --service mfo-service
  python scripts/doc_coverage.py --project mfo-carveout
  python scripts/doc_coverage.py --all
"""
from __future__ import annotations
import argparse, sys
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("PyYAML required: pip install pyyaml")

ROOT = Path(__file__).resolve().parent.parent
PROFILE = ROOT / "templates" / "coverage-profile.yaml"
REGISTRY = ROOT / "docs" / "registry.yaml"
DOC_DIRS = [ROOT / "docs", ROOT / "drafts"]

STATE_ORDER = {"present": 3, "draft": 2, "waived": 1, "missing": 0}
STATE_ICON = {"present": "✅ present", "draft": "🟡 draft", "waived": "➖ N/A", "missing": "❌ missing"}


def load_frontmatter(path: Path) -> dict | None:
    text = path.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return None
    parts = text.split("---", 2)
    if len(parts) < 3:
        return None
    try:
        data = yaml.safe_load(parts[1])
        return data if isinstance(data, dict) else None
    except yaml.YAMLError:
        return None


def scan_docs() -> list[dict]:
    """All authored docs (with a `template`) across docs/ and drafts/, with location."""
    found = []
    for base in DOC_DIRS:
        if not base.exists():
            continue
        for p in base.rglob("*.md"):
            fm = load_frontmatter(p)
            if not fm or not fm.get("template"):
                continue
            found.append({
                "path": p.relative_to(ROOT).as_posix(),
                "template": fm.get("template"),
                "status": (fm.get("status") or "draft").lower(),
                "service": fm.get("service"),
                "project": fm.get("project"),
                "location": "docs" if base.name == "docs" else "drafts",
            })
    return found


def doc_state(status: str) -> str:
    if status == "approved":
        return "present"
    if status == "deprecated":
        return "missing"   # a deprecated doc does not satisfy coverage
    return "draft"          # draft | review | anything else in progress


def coverage(scope: str, name: str, profile: list[dict], registry: dict, docs: list[dict]) -> dict:
    services = registry.get("services", {})
    projects = registry.get("projects", {})

    if scope == "service":
        svc = services.get(name) or {}
        facets = set(svc.get("facets") or [])
        waived = {w["template"]: w.get("reason", "") for w in (svc.get("coverage_waived") or [])}
        expected = [d for d in profile if d.get("scope") == "service"
                    and set(d.get("when") or []).issubset(facets)]
        mine = [d for d in docs if d.get("service") == name]
        header = f"service **{name}** · facets: {', '.join(sorted(facets)) or '—'}"
    else:  # project
        proj = projects.get(name) or {}
        waived = {w["template"]: w.get("reason", "") for w in (proj.get("coverage_waived") or [])}
        expected = [d for d in profile if d.get("scope") == "project"]
        mine = [d for d in docs if d.get("project") == name and not d.get("service")]
        header = f"project **{name}** · member services: {', '.join(proj.get('services') or []) or '—'}"

    # best doc per template
    by_template: dict[str, dict] = {}
    for d in mine:
        st = doc_state(d["status"])
        cur = by_template.get(d["template"])
        if cur is None or STATE_ORDER[st] > STATE_ORDER[cur["state"]]:
            by_template[d["template"]] = {"state": st, "path": d["path"], "location": d["location"]}

    rows = []
    for e in expected:
        t = e["template"]
        if t in waived:
            rows.append({**e, "state": "waived", "path": waived[t] or "(N/A)", "location": "—"})
        elif t in by_template:
            hit = by_template[t]
            rows.append({**e, "state": hit["state"], "path": hit["path"], "location": hit["location"]})
        else:
            rows.append({**e, "state": "missing", "path": "", "location": "—"})
    return {"header": header, "rows": rows, "extras": [
        d for d in mine if d["template"] not in {e["template"] for e in expected}]}


def render(scope: str, name: str, cov: dict) -> str:
    rows = cov["rows"]
    out = [f"## Coverage — {cov['header']}", ""]
    out.append("| Document (template) | Category | Tier | When | State | Location |")
    out.append("|---------------------|----------|------|------|-------|----------|")
    tier_rank = {"required": 0, "recommended": 1, "optional": 2}
    for r in sorted(rows, key=lambda r: (tier_rank.get(r["tier"], 9), STATE_ORDER[r["state"]])):
        when = ", ".join(r.get("when") or []) or "—"
        path = f"`{r['path']}`" if r["path"] else "—"
        out.append(f"| {r['template']} | {r['category']} | {r['tier']} | {when} | {STATE_ICON[r['state']]} | {path} |")
    out.append("")

    # summary
    def count(state=None, tier=None):
        return sum(1 for r in rows if (state is None or r["state"] == state) and (tier is None or r["tier"] == tier))
    total = len(rows)
    done = count("present")
    out.append(f"**Summary:** {done}/{total} present · {count('draft')} draft · "
               f"{count('missing')} missing · {count('waived')} N/A")
    for tier in ("required", "recommended", "optional"):
        tot = count(tier=tier)
        if tot:
            miss = [r["template"] for r in rows if r["tier"] == tier and r["state"] == "missing"]
            drafts = [r["template"] for r in rows if r["tier"] == tier and r["state"] == "draft"]
            line = f"- **{tier}:** {count('present', tier)}/{tot} present"
            if drafts:
                line += f" · draft: {', '.join(drafts)}"
            if miss:
                line += f" · **missing: {', '.join(miss)}**"
            out.append(line)
    if cov["extras"]:
        out.append("")
        out.append("_Extra docs (not in profile): " +
                   ", ".join(f"`{e['template']}`" for e in cov["extras"]) + "_")
    out.append("")
    return "\n".join(out)


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--service")
    g.add_argument("--project")
    g.add_argument("--all", action="store_true")
    args = ap.parse_args()

    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass
    profile = yaml.safe_load(PROFILE.read_text(encoding="utf-8"))["documents"]
    registry = yaml.safe_load(REGISTRY.read_text(encoding="utf-8"))
    docs = scan_docs()

    blocks = []
    if args.service:
        blocks.append(render("service", args.service, coverage("service", args.service, profile, registry, docs)))
    elif args.project:
        blocks.append(render("project", args.project, coverage("project", args.project, profile, registry, docs)))
    else:
        for s in registry.get("services", {}):
            blocks.append(render("service", s, coverage("service", s, profile, registry, docs)))
        for p in registry.get("projects", {}):
            blocks.append(render("project", p, coverage("project", p, profile, registry, docs)))
    print("\n".join(blocks))


if __name__ == "__main__":
    main()
