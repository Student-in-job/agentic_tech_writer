---
description: Check docs/ for drift against the code they describe (last_verified_commit vs HEAD)
argument-hint: [document or repo, optional — default all]
---

Use the **doc-watch** skill to check documentation drift: `$ARGUMENTS`

For each relevant document in `docs/`, compare its frontmatter `last_verified_commit`
against the repo's current HEAD via the git MCP. Report a drift table (doc, last-verified,
current HEAD, commits behind, whether endpoint-relevant files changed). Read-only — do not
rewrite or publish anything; just surface the drift.
