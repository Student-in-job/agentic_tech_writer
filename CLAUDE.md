# CLAUDE.md — Claude Agentic Workspace Directives

> **Canonical source of truth:** [`AGENTS.md`](AGENTS.md).
> This file holds only Claude-specific deltas. When anything here and `AGENTS.md`
> disagree, `AGENTS.md` wins.

## Executive Instructions for Claude Models

When operating within `local_documentation/`:

1. **Working Directory Focus**:
   - `local_documentation/` is the active working directory for drafting architectural
     notes, specifications, diagrams, and integration analyses.
   - Full read/write authority inside `local_documentation/`. Read-only by default for
     codebase repositories unless explicitly instructed otherwise.
2. **Git & Repository Integration**:
   - Use the Git MCP server ([`git_mcp_server.py`](git_mcp_server.py)) to query local
     Git status, diffs, commits, as well as GitHub and GitLab APIs.
   - Default GitLab URL: `https://git.ipoint.uz` (configurable via `GITLAB_URL`
     environment variable).
   - Credentials come from the environment (`GITLAB_TOKEN`, `GITHUB_TOKEN` / `GH_TOKEN`).
     Never hardcode tokens in files under this repository.
3. **Execution Conventions**:
   - Ensure all generated documentation is clean and well-formatted.
   - Preserve existing system contracts and highlight high-risk integration touchpoints
     using markdown alerts (`> [!WARNING]`, `> [!IMPORTANT]`).
   - Frontmatter for all newly authored notes:
     ```yaml
     ---
     author: System Architect Agent
     created: YYYY-MM-DD
     type: architecture | risk-analysis | specification | task
     ---
     ```
4. **Tool Utilization**:
   - For file viewing and editing inside `local_documentation/`, use the standard
     Read/Edit/Write tools.
   - For Git/GitHub/GitLab operations, invoke the `git_mcp_server` tools (`git_status`,
     `git_log`, `git_diff`, `git_branch_list`, `git_commit_info`, `github_api`,
     `gitlab_api`).

## Standards & Conformance

Configuration and agent behavior in this workspace conform to **two** aligned standards:

1. **Anthropic Claude Code conventions** — `CLAUDE.md` as the Claude entry point,
   file-based memory, and MCP for tool/data integration.
2. **Linux Foundation — Agentic AI Foundation (AAIF)** open standards (announced
   Dec 2025). We follow its anchor projects that apply to this workspace:
   - **AGENTS.md** — the vendor-neutral, canonical instruction file. It is the single
     source of truth; `CLAUDE.md` and `GEMINI.md` are vendor-specific views that defer
     to it. Keep shared rules in `AGENTS.md`, not duplicated per vendor.
   - **MCP (Model Context Protocol)** — the standard for connecting agents to tools and
     data. New tool integrations here are exposed via MCP (see
     [`mcp_config.json`](mcp_config.json)), not ad-hoc scripts, wherever practical.

**Precedence:** `AGENTS.md` (open standard) → this `CLAUDE.md` (vendor delta) → chat
instructions from the operator. Any rule added here that is not Claude-specific should
instead be added to `AGENTS.md` so every agent inherits it.

## Agent Workflows

- **Integration risk analysis** — trace cross-system dependencies between repositories
  (`nasiya-api`, `file-bridge`, `autopay`, `hermes`, `broker`); document payload schemas,
  breaking-change hazards, and sync/async boundary risks.
- **Solution & architecture design** — draft Architecture Decision Records (ADRs); break
  monolithic changes into modular, system-by-system tasks.
- **Git & remote sync** — inspect remote commits, Merge Requests (GitLab), Pull Requests
  (GitHub), and pipeline statuses via the Git MCP server.
