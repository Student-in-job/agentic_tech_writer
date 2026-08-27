# GEMINI.md — Gemini Agentic Workspace Directives

> **Canonical source of truth:** [`AGENTS.md`](AGENTS.md).
> This file holds only Gemini-specific deltas. When anything here and `AGENTS.md`
> disagree, `AGENTS.md` wins. Shared rules (mission, workspace scoping, git/MCP usage,
> documentation standards, standards & conformance) live in `AGENTS.md` — do not
> duplicate them here.

## Gemini-specific deltas

1. **Tool utilization**:
   - For file viewing and editing inside `local_documentation/`, use Gemini's standard
     view and edit tools.
   - For Git/GitHub/GitLab operations, invoke the `git_mcp_server` tools (`git_status`,
     `git_log`, `git_diff`, `git_commit_info`, `git_branch_list`, `github_api`,
     `gitlab_api`).
2. **Alerts**:
   - Highlight high-risk integration touchpoints with markdown alerts
     (`> [!WARNING]`, `> [!IMPORTANT]`).
