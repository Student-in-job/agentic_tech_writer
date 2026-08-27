# local_documentation — Analyst & Technical Writer Workspace

Workspace for the **Analyst + Technical Writer** role: turn a project's business
requirements and source code into **structured technical documentation**, staged here and
later published manually to corporate knowledge bases.

## What this space is for

- Analyze **business requirements** and the **source code** of projects (multi-stack).
- Determine **entry points, main endpoints**, describe **how the system works** and its
  **key algorithms**.
- Produce **diagrams** (Context/C4, Block, BPMN, Sequence, Flow/State) as Mermaid.
- Write documentation against a **single cross-project template**, so every project's docs
  look and read the same.
- **Stage** finished documents here, then publish them **manually** to the corporate KB
  (Confluence / Notion / Google Docs).
- Keep local project docs under `docs/` **observed** for drift against code changes.

## Standards

Configured to conform to two aligned standards (details in
[`AGENTS.md`](AGENTS.md#standards--conformance)):

| Standard | What it gives us |
|----------|------------------|
| **Anthropic Claude Code** | `CLAUDE.md` entry point, file-based memory, MCP |
| **Linux Foundation — Agentic AI Foundation (AAIF)** | `AGENTS.md` as canonical instruction file; **MCP** for all tool/data integration |

**Precedence:** `AGENTS.md` (canonical) → vendor file (`CLAUDE.md` / `GEMINI.md`, deltas
only) → operator's chat instructions.

## Instruction files

| File | Role |
|------|------|
| [`AGENTS.md`](AGENTS.md) | **Canonical** source of truth (AAIF standard) — all shared rules |
| [`CLAUDE.md`](CLAUDE.md) | Claude-specific deltas; defers to `AGENTS.md` |
| [`GEMINI.md`](GEMINI.md) | Gemini-specific deltas; defers to `AGENTS.md` |

## Integrations (MCP)

| Purpose | MCP | Status |
|---------|-----|--------|
| Inspect repos, verify current changes, keep docs in sync | git / GitLab / GitHub | active — [`git_mcp_server.py`](git_mcp_server.py), [`mcp_config.json`](mcp_config.json) |
| Publish to corporate KB | Notion | available |
| Publish to corporate KB | Confluence | planned |
| Publish to corporate KB | Google Drive (Docs) | planned |

## Layout

```
local_documentation/
├── AGENTS.md / CLAUDE.md / GEMINI.md   # instruction files
├── README.md                           # this file
├── mcp_config.json / git_mcp_server.py # git MCP server
├── .claude/
│   ├── skills/    code-recon · doc-template · diagram-builder · confluence-publish · doc-watch · kb-author
│   ├── agents/    tech-writer · code-analyst · analyst
│   └── commands/  /recon · /document · /diagram · /doc-watch · /add-stack · /publish
├── templates/
│   └── project-doc-template.md         # the cross-project documentation template
├── docs/                               # project documents under observation (empty)
└── drafts/                             # work-in-progress documents (empty)
```

## Commands (slash-command triggers for skills)

| Command | Triggers | Does |
|---------|----------|------|
| `/recon <repo>` | code-recon | detect stack, map entry points & endpoints |
| `/document <project>` | tech-writer + skills | full doc from the canonical template → `drafts/` |
| `/diagram <type> for <subject>` | diagram-builder | one mandatory Mermaid diagram |
| `/doc-watch [doc/repo]` | doc-watch | check `docs/` drift vs code |
| `/add-stack <framework>` | kb-author | add a knowledge-base for a new stack |
| `/publish <doc>` | confluence-publish | manual delivery to Confluence |

## Supported stacks & diagrams

- **Code stacks** (entry-point / endpoint analysis): PHP **Laravel**, Java **Quarkus**,
  Java **Spring**, Python **FastAPI**, TypeScript **Vue.js** (frontend entry points).
- **Mandatory diagrams** (Mermaid): **Context/C4**, **Block**, **BPMN**
  (flowchart approximation or embedded `.bpmn`), **Sequence**, **Flow/State**.

## Ground rules

- **Read-only** for code repositories by default; full read/write only inside
  `local_documentation/`.
- **No auto-publish** — nothing is auto-uploaded, auto-synced, auto-committed, or
  auto-pushed out of this folder. Delivery to a KB is an explicit, per-document step
  initiated by the operator (`AGENTS.md` Operating Principles §4).
- New authored notes carry frontmatter (`author`, `created`, `type`).
- Reference files with clickable **relative** markdown links, not `file:///` URIs.
