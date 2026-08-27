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
- **Release tag** after the merge to `main`, SemVer `vX.Y.Z`:
  - **Z (patch):** syntax fixes, edits/additions inside existing files, small fixes.
  - **Y (minor):** new skills / agents / commands, or any change to the rules in
    `AGENTS.md` or `CLAUDE.md` — the significant changes.
  - **X (major):** bumped **manually only**, on an explicit "new version / bump major"
    command from the operator.

> [!NOTE]
> Per the harness defaults, commit/push/PR are still operator-gated actions — this section
> defines the *shape* of the flow; the approval gate above is the explicit checkpoint.

## Agent Workflows & Task Execution

### 1. Integration Risk Analysis
- Trace cross-system dependencies between repositories (e.g. `nasiya-api`, `file-bridge`, `autopay`, `hermes`, `broker`).
- Document payload schemas, breaking change hazards, and sync/async boundary risks.

### 2. Solution & Architecture Design
- Draft Architecture Decision Records (ADRs).
- Break down monolithic changes into modular, system-by-system tasks.

### 3. Git & Remote Repository Sync
- Leverage the local Git MCP server to inspect remote commits, Merge Requests (GitLab), Pull Requests (GitHub), and pipeline statuses across both platforms.
