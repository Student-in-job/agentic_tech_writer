# AGENTS.md — Guidelines & Protocols for AI Agents

> **Canonical, vendor-neutral instruction file** for this workspace, per the Linux
> Foundation **Agentic AI Foundation (AAIF)** `AGENTS.md` standard. This is the single
> source of truth. Vendor-specific files ([`CLAUDE.md`](CLAUDE.md),
> [`GEMINI.md`](GEMINI.md)) hold only per-vendor deltas and defer to this file.

## Standards & Conformance

This workspace is configured to conform to **two aligned standards**:

- **Linux Foundation — Agentic AI Foundation (AAIF)** open standards: `AGENTS.md` as the
  canonical instruction file (this file), and **MCP (Model Context Protocol)** for tool
  and data integration (see [`mcp_config.json`](mcp_config.json)).
- **Anthropic Claude Code conventions**: `CLAUDE.md` entry point, file-based memory, MCP.

Keep shared rules here; add vendor-only rules to the corresponding vendor file. Precedence:
`AGENTS.md` → vendor file → operator's chat instructions.

## Overview & Mission

This folder (`local_documentation/`) is the workspace for the **Analyst + Technical
Writer** role and the skills/agents that extend it. Mission: from a project's business
requirements and its source code, produce **structured technical documentation** driven by
a single cross-project template, and stage it here for later manual publication to
corporate knowledge bases.

Core capabilities the role must have (built up via skills/agents):

- **Business analysis** — understand and capture business requirements.
- **Code technical analysis (multi-stack)** — connect to code repositories and, across
  different stacks, determine entry points, main endpoints, describe how the system works
  and its key algorithms.
- **Diagramming** — build the diagrams the template calls for (context/C4, sequence,
  data model, flow/state) as Mermaid.
- **Structured writing** — fill the canonical template so documentation is uniform across
  all projects.
- **Publication** — export results to corporate knowledge bases, each of which may follow
  its own corporate standard: **Confluence, Notion, Google Drive (Docs)**.

Integrations the role relies on (via MCP):

- **git / GitLab / GitHub** — inspect repositories, verify current changes, and keep
  documentation in sync with code updates.
- **Confluence / Notion / Google Docs** — deliver finished documents to the corporate KB.
- A local **`docs/`** folder holds project documents that are kept under observation
  (drift between code and docs).

> [!NOTE]
> Delivery to any KB is a manual, operator-initiated step — see Operating Principles §4
> (Staging Area — No Auto-Publish).

## Operating Principles

1. **Workspace Scoping**:
   - Full read/write authority within `local_documentation/`.
   - Read-only by default for codebase repositories unless explicitly instructed otherwise.
2. **Git & Remote Repository Operations**:
   - Use the Git MCP Server (`git_mcp_server.py`) for querying and interacting with GitHub and GitLab.
   - For GitLab (`https://git.ipoint.uz` or `https://gitlab.com`), use configured GitLab API tokens and endpoints.
   - For GitHub, use standard GitHub API tokens (`GITHUB_TOKEN` / `GH_TOKEN`).
3. **Documentation Standards**:
   - Use GitHub-flavored markdown.
   - **Link style (all agents):** reference exact file paths with clickable relative
     markdown links, optionally with a line suffix — e.g. `[file](path/to/file.md)` or
     `[file:42](path/to/file.md:42)`. Do not use absolute `file:///` URIs (they are
     local-only and break in shared/GitHub views).
   - Structure documents clearly with headers, risk matrices, sequence/Mermaid diagrams, and actionable task items.
   - Frontmatter tags for all newly authored notes:
     ```yaml
     ---
     author: System Architect Agent
     created: YYYY-MM-DD
     type: architecture | risk-analysis | specification | task
     ---
     ```
4. **Staging Area — No Auto-Publish**:
   - `local_documentation/` is a **drafting/staging area**. Documentation is written and
     worked on here, then **manually** sent to the appropriate sections of the Obsidian
     vault (`obsidian/`).
   - **Never auto-upload, auto-sync, auto-commit, or auto-push anything out of this
     folder** — to the vault, git remotes, or any external service. Publishing is an
     explicit, operator-initiated step for each document. When a draft is ready, ask
     which vault section it goes to; do not move or copy it there on your own.

## Workspace Configuration

Concrete decisions this workspace is set up around:

- **Documentation template (canonical):** [`templates/project-doc-template.md`](templates/project-doc-template.md).
  Every project's docs follow its section order — uniform across the whole portfolio.
- **Watched docs folder:** [`docs/`](docs/) — project documents kept under observation for
  drift against code. Work-in-progress lives in [`drafts/`](drafts/).
- **Supported code stacks** (entry-point / endpoint analysis): PHP **Laravel**,
  Java **Quarkus**, Java **Spring**, Python **FastAPI**, TypeScript **Vue.js**
  (Vue = frontend entry points). Each has a knowledge-base under
  `.claude/skills/code-recon/knowledge/`; add new stacks with the **kb-author** skill.
- **Mandatory diagrams** (Mermaid): **Context/C4**, **Block**, **BPMN**
  (flowchart approximation or embedded `.bpmn`), **Sequence**, **Flow/State**.
- **First KB target:** **Confluence** (publish is manual — Operating Principles §4).
  Notion available; Google Docs planned.
- **Skills & agents** extending the role live in [`.claude/`](.claude/).

## Document Lifecycle & Storage (draft → approved → published)

Where an authored document lives is driven by its `status:` frontmatter. Two folders:

- **`drafts/`** — work in progress (`status: draft` | `review`). A scratch area; **nothing
  here is canonical** and nothing here is published.
- **`docs/`** — **approved canonical Markdown** (`status: approved`). This tree, in Git, is
  the single source of truth. It is organized by the **aggregation layer** (projects →
  services → repos), not by category alone:
  - **`docs/services/<service>/<category>/`** — service-scoped docs. Each service has an
    **`index.md`** card (bounded context, **code repositories**, doc index, integrations).
    `<category>` ∈ `requirements` · `architecture` · `api` · `readme` · `user` · `partner` ·
    `ops` · `release`.
  - **`docs/projects/<project>/`** — cross-service **business-project** docs, with an
    `index.md` card listing the member services.
  - **`docs/_shared/<category>/`** — cross-cutting docs not tied to one service.
  - **`docs/registry.yaml`** — the aggregation registry (see *Aggregation* below).

**Flow (each step operator-gated; no step is automatic):**

1. **Author** in `drafts/<name>.md` (via `doc-new`). `status: draft`.
2. **Review** — operator reads; edits happen in place; `status: review`.
3. **Approve** — on an explicit operator "go": set `status: approved`, refresh `updated:`,
   and apply the group's scheme from *Documentation Versioning* (SemVer tag for contracts,
   immutable id for ADRs, etc.).
4. **Promote** — **move** `drafts/<name>.md` → `docs/<target>`. The filename stays stable
   (it is the document's identity in the publish map). See `target:` semantics below.
5. **Commit** — Git history *is* the version record (*Documentation Versioning*). Tag when
   the group's scheme calls for it.
6. **Publish (optional)** — a separate, operator-initiated step: `doc-publish` renders a copy
   to the KB backend and records it in the publish map. The `.md` under `docs/` stays
   canonical; the KB copy never becomes the source.

**`target:` semantics** — the document's destination *for its `backend:`*:
- `backend: md` → a **repo-relative path under this repo**, e.g.
  `docs/services/mfo-service/architecture/data-model.md` (service-scoped),
  `docs/projects/<project>/<name>.md` (cross-service), or `docs/_shared/<category>/<name>.md`.
  This is where *Promote* moves the file; the `service:` / `project:` frontmatter picks the
  branch.
- `backend: confluence | notion | gdocs` → the **KB space / parent / Drive folder**; the
  canonical `.md` still lives under the matching `docs/…` path by *Promote*.

> [!IMPORTANT]
> **Ownership / canonical home.** A document may *describe* a repo we do **not** own
> (read-only analysis targets such as `nasiya/backend/mfo-service`). Its canonical home is
> **always this repo's `docs/`**, regardless of which service it is about. Mirroring an
> approved doc into the owning service's repo (true docs-as-code, next to the code) is a
> **separate, optional MR to that team** — never the default, and never treated as the source
> of truth here.

### Aggregation (projects → services → repos)

`docs/` is organized by an aggregation layer so documents group by what they describe, not
only by category. This layer is **self-contained** — it is **not** derived from, and does not
depend on, `SDLC/*.yaml` (this workspace's doc-tooling is standalone). Its purpose is the
reverse: the approved docs under `docs/` are **pre-made knowledge that `sdlc-init` /
`sdlc-analyze` consume as input**, so those stages start from an existing service picture
instead of analyzing from scratch.

- **`docs/registry.yaml`** — the single machine-readable map: each **service** → its **code
  repositories**, bounded context, database, integrations, and doc folder; each **project** →
  its member services. Produced/maintained by the doc-tooling agents; kept in sync with the
  `docs/services|projects/` trees.
- **Service card** (`docs/services/<service>/index.md`) — the human-readable counterpart:
  what the service is, which repos make it up, the index of its docs (by category, with
  status), and its integration points.
- **Project card** (`docs/projects/<project>/index.md`) — a business project that spans
  **one or more services**, listing its member services and cross-service docs.

A **service** is composed of one or more **code repositories** (e.g. backend + frontend); the
registry's `repos:` list is the source for that mapping. A document joins the layer through
its `service:` / `project:` frontmatter.

## Documentation Format & Publication

### Format — Markdown is the single source of truth

- All documentation is **authored and maintained locally in Markdown (`.md`)** with YAML
  frontmatter. The `.md` file in Git is the **canonical version** — the one we write,
  review, version, and diff. Everything else is derived from it.
- Copies in Confluence / Notion / Google Docs are **rendered outputs, never the source.**
  Changes flow **MD → backend**, not back. If someone edits a published page, reconcile the
  change into the `.md` first, then re-publish — do not treat the backend copy as truth.

### Publication — MD → backends via MCP + scripts (operator-gated)

Publishing is a separate, **operator-initiated** step (Operating Principles §4 — no
auto-publish). It is **not** done on save, in bulk, or automatically. The pipeline for one
document (see [`publish/README.md`](publish/README.md) for the concrete spec):

1. **Route** — the `backend` + `target` frontmatter decide the destination (Confluence
   space/parent · Notion parent · Google Drive folder). `unit: multi` → parent + children.
2. **Convert** — a pure **script** turns canonical Markdown into the backend's format
   (Confluence storage/ADF · Notion blocks · Google Docs requests), rewriting relative
   links/`[[wikilinks]]` and handling images/attachments. Scripts are deterministic and
   side-effect-free; they do not call out anywhere.
3. **Transport via MCP** — the publish skill performs the actual create/update through the
   backend's **MCP**: **Notion MCP** (`notion-create-pages` / `notion-update-page`),
   **Google Docs connector**; **Confluence** via its REST API script until an Atlassian MCP
   is wired. MCP calls live in the skill/agent, never inside the conversion scripts.
4. **Idempotent create-or-update** — a sidecar **publish map**
   ([`publish/publish-map.yaml`](publish/README.md)) records `doc → {backend: page/file id,
   version, published_at}`, so re-publishing **updates the existing page** instead of
   creating a duplicate. The map is state, kept out of the `.md` so documents stay clean.
5. **Confirm** — report each page created/updated with its link; never publish without an
   explicit operator "go".

## Git Workflow & Versioning (tooling repo)

Applies to **this** repository only — `local_documentation/`, whose origin is GitHub
`Student-in-job/agentic_tech_writer` (the Agentic tooling: settings, commands/actions,
rules, skills, agents, KB, templates). Analysis-target code repos on GitLab stay read-only.

- **Branch:** do all work on **`dev`**. Never commit directly to `main`.
- **Commits:** describe changes from the **Agentic-workflow** standpoint — what was added or
  changed in *settings, actions/commands, rules, skills, agents, knowledge bases, templates*.
- **Push:** push `dev` to origin.
- **PR → main:** open a Pull Request `dev → main`.
- **Approval gate (always):** ask the operator for explicit approval **before** opening /
  merging the PR into `main`. Never merge without a clear "yes".
- **Release tag** after the merge to `main`, `vX.Y.Z`:
  - **Z (patch):** syntax fixes, edits/additions inside existing files, small fixes.
  - **Y (minor):** new skills / agents / commands, or any change to the rules in
    `AGENTS.md` or `CLAUDE.md` — the significant changes.
  - **X (major):** bumped **manually only**, on an explicit "new version / bump major"
    command from the operator.
  - **PATCH starts at `1`, never `0`.** A `.0` reads like an unfinished draft, so a release
    is never tagged `vX.Y.0`. On a **Y (minor)** or **X (major)** bump, the first release at
    that version is tagged `.1` (e.g. `v0.3.1`, not `v0.3.0`); further patches on it go `.2`,
    `.3`, … So the sequence is `…v0.2.z → v0.3.1 → v0.3.2 → …`.

> [!NOTE]
> Per the harness defaults, commit/push/PR are still operator-gated actions — this section
> defines the *shape* of the flow; the approval gate above is the explicit checkpoint.

## Documentation Versioning (authored docs)

> [!IMPORTANT]
> This is a **different scope** from the section above. *Git Workflow & Versioning* versions
> **this tooling repo** (skills/agents/templates). This section governs how the
> **documentation we author** (the output of the templates) is versioned once it lives
> beside a project's code or in a KB.

**Core principle — do not version the documentation as one monolith.** Each group of
documents has its own reason to change, so each gets its own versioning scheme. The only
things they share: **Git as the single source of history**, and **frontmatter metadata** in
every file.

### Frontmatter metadata (every authored document)

Every document carries a YAML frontmatter block. It extends the base authoring block
(Operating Principles §3) with lifecycle/version fields:

```yaml
---
title: Payment service — architecture
author: System Architect Agent
owner: payments-team          # accountable owner (mirrors CODEOWNERS)
created: 2026-10-28
updated: 2026-10-28
version: 1.3.0                 # per-group scheme (see table); omit when "= service release"
status: approved              # draft | review | approved | deprecated
type: architecture | risk-analysis | specification | task | documentation
service: payment-service             # aggregation key → docs/services/<service>/ (registry.yaml)
project: payments-platform           # optional — business project the service belongs to
applies_to: payment-service >= 2.4   # optional — the code/version this describes
depends_on: [payment-api@2.x]        # optional — compat via links, not synced versions
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: single
---
```

Markdown + frontmatter is readable by people, agents, and scripts (registry/CI can parse it).
`service:` / `project:` tie the document into the aggregation layer (*Document Lifecycle &
Storage* → *Aggregation*); a cross-service document sets `project:` and omits `service:`.

### Scheme per group

| Group (our template ids) | How to version |
|--------------------------|----------------|
| **API contracts** — `api-contract`, `api-library` (OpenAPI/AsyncAPI/proto) | **Strict SemVer**: MAJOR = breaking, MINOR = new fields/endpoints, PATCH = descriptions. Live beside the service; CI checks backward-compat (`oasdiff`, `buf breaking`). |
| **Architecture / data model / README** — `c4-architecture`, `data-model`, `service-readme` | Live **with the service code**; usually **no separate number** — version = the service's commit / release tag. Leave `version` out, set `applies_to`. |
| **ADR** — `adr` | **Immutable & numbered** (`0007-use-kafka.md`). Never edited. If a decision changes, write a **new** ADR and mark the old `status: deprecated` + "superseded by 0012". A journal of decisions. |
| **Requirements (PRD/SRS)** — `vision`, `frd`, `nfr`, `glossary` | Document `version` + a **changelog at the end**. Tag the repo on approval (`prd-billing-v2.0`). Every requirement keeps a **stable ID** (`REQ-BILL-014`) so tasks/tests/code can reference it. |
| **User documentation** — `user-guide`, `admin-guide`, `developer-portal` | Tied to **product releases**: a branch or folder per supported major (`/docs/v3`, `/docs/v4`). Tools like Docusaurus or MkDocs + `mike` do this natively. |
| **Partner documentation** — `integration-registry`, `partner-spec-snapshot`, `partner-integration` | Store a **snapshot with the partner's version** (`partners/acme-pay/api-v5.2-2026-09.pdf`). The integration registry records which partner API version we currently run on. |
| **Operations** — `runbook`, `deployment` (runbook, IaC) | **As code, no numbers** — the current `main` branch is authoritative. |
| **Release notes** — `release-notes` | Per product release; doubles as the user-facing changelog. |

### Keeping the parts consistent

- **Documentation registry/index:** a single file/page **generated by a script from the
  frontmatter** — summary of document, version, status, owner, `updated`, and which service
  version it applies to.
- **Compatibility via links, not synchronized versions:** a document references a specific
  version of another (`applies_to`, `depends_on: payment-api@2.x`) instead of waiting for a
  shared "documentation release".
- **Snapshots on key dates:** for an external audit, a milestone handover, or a major
  release, tag the whole repo (`docs-release-2026-Q4`) for a consistent cross-section of all
  documents at that moment.
- **CI checks:** frontmatter validity, broken links, API backward-compat, and a staleness
  signal (an `approved` document not updated in > N months → flag for review).
- **CODEOWNERS:** every documentation folder has an owner; changes are not merged without
  that owner's review. Keep `owner:` in frontmatter aligned with CODEOWNERS.

**In short:** Git for history, SemVer **only** for contracts, immutable ADRs, release-tied
versions for user docs, snapshots for partner docs; consistency comes from frontmatter, the
registry, and tags — not from one global version number.

## Agent Workflows & Task Execution

### 1. Integration Risk Analysis
- Trace cross-system dependencies between repositories (e.g. `nasiya-api`, `file-bridge`, `autopay`, `hermes`, `broker`).
- Document payload schemas, breaking change hazards, and sync/async boundary risks.

### 2. Solution & Architecture Design
- Draft Architecture Decision Records (ADRs).
- Break down monolithic changes into modular, system-by-system tasks.

### 3. Git & Remote Repository Sync
- Leverage the local Git MCP server to inspect remote commits, Merge Requests (GitLab), Pull Requests (GitHub), and pipeline statuses across both platforms.
