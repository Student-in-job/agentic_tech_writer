---
name: doc-coverage
description: >-
  Assess documentation completeness for a service or business project: compare the EXPECTED
  document set (coverage profile filtered by the service's facets) against what exists in
  docs/ and drafts/, report the gaps, and decide with the operator which missing docs to
  create, defer, or mark N/A. Use when asked "what docs are missing", "is the documentation
  complete", "what should we still write for <service>", or to review doc coverage.
---

# doc-coverage — documentation completeness

Tells the operator **which documents are still missing** for a service/project and drives the
decision of what to create next. It does **not** write the documents — it finds gaps and hands
chosen ones to `doc-new`.

## Inputs

- **Profile** — [`templates/coverage-profile.yaml`](../../../templates/coverage-profile.yaml):
  document type → `tier` (`required|recommended|optional`) + `when` (required facets) + `scope`.
- **Registry** — [`docs/registry.yaml`](../../../docs/registry.yaml): each service's `facets`
  and `coverage_waived`, and each project's member services.
- **Actual docs** — every `.md` under `docs/` and `drafts/`, matched by frontmatter `template:`
  + `service:`/`project:` and graded by `status:` (`approved`→present, `draft`/`review`→draft).

## Process

1. **Resolve target** — a service (default), a project, or all (from the registry).
2. **Compute coverage** — run the engine (deterministic):
   ```bash
   python scripts/doc_coverage.py --service <name>     # or --project <name> / --all
   ```
   It prints the Markdown matrix: each expected doc → `present | draft | missing | N/A`, with
   per-tier summary and the explicit gap list.
3. **Save/refresh the report** — write it to `docs/services/<service>/coverage.md`
   (or `docs/projects/<project>/coverage.md`), so coverage is itself a tracked document.
4. **Discuss the gaps with the operator** — do **not** auto-create. Present the missing
   **required** (then recommended) docs and, via a question, let the operator choose per gap:
   - **Create now** → hand the type to `doc-new` (template-library) to start a draft in `drafts/`.
   - **Defer** → leave as a known gap (stays flagged next run).
   - **N/A** → record a waiver in `registry.yaml` under the service's `coverage_waived:`
     (`[{template, reason}]`), so it stops being flagged. Always capture a reason.
5. **Re-run** after creating/waiving to show the updated matrix.

## Rules

- Read-only on the code repos; this works only on `local_documentation` docs + registry.
- Never invent that a doc exists — "present" requires an `approved` doc with that `template`.
- A gap is a prompt for a decision, not an order: respect Defer / N/A.
- Keep the profile and registry facets in sync with reality; when a service gains a capability
  (e.g. a UI), add the facet and re-run — new expected docs will surface.
- Operator-gated throughout: creating drafts and editing the registry happen on an explicit "go".
