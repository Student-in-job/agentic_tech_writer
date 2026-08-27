---
name: doc-watch
description: Check whether project documents under docs/ have drifted from the code they describe, by comparing each doc's last_verified_commit against the repository's current HEAD. Use when asked to check documentation freshness, find stale docs, or review what changed in a repo since the docs were written.
---

# doc-watch — detect documentation drift

Keep `docs/` honest: flag documents whose source code has moved ahead of them.

## Procedure

1. For each document in [`docs/`](../../../docs/), read its frontmatter `repo` and
   `last_verified_commit`.
2. Via the **git MCP** (`git_log` / `github_api` / `gitlab_api`), get the repo's current
   HEAD/default-branch commit.
3. If HEAD ≠ `last_verified_commit`, list the commits in between and classify likely
   impact: do they touch entry points, endpoints, data model, or integrations (the
   sections `code-recon` feeds)?
4. Report a **drift table**: doc, last-verified, current HEAD, # commits behind, whether
   endpoint-relevant files changed.

## Rules

- **Read-only** — inspect git, do not modify repos or auto-update docs.
- Do not silently rewrite documents. Surface the drift and let the operator decide what to
  refresh (then use `code-recon` + `doc-template` to update the affected sections).
- Never auto-publish updated docs (`AGENTS.md` §4).
