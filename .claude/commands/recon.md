---
description: Analyze a repository — detect stack, entry points and endpoints (code-recon)
argument-hint: <repo path or name>
---

Use the **code-recon** skill to analyze the repository: `$ARGUMENTS`

Follow the skill's procedure: README-first hint → confirm the stack from manifests →
load the matching `knowledge/<stack>.md` → enumerate and trace entry points → emit the
endpoint table (template §6) plus notes for §7–9. Read-only; anchor every finding to
`file:line`. If no knowledge-base matches the detected framework, use the **kb-author**
skill first.
