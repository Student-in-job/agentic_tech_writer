---
name: doc-template
description: Produce or update a project's technical documentation using the canonical cross-project template. Use when writing project docs, filling the standard doc structure, or ensuring a document matches the portfolio template (sections, frontmatter, diagrams).
---

# doc-template — write docs against the canonical template

Assemble a project's technical documentation so it is **uniform across the portfolio**.

## Source of truth

The template is [`templates/project-doc-template.md`](../../../templates/project-doc-template.md).
Always start from it — copy it, never invent a different section order.

## Procedure

1. Copy the template into `drafts/<project>.md` (WIP) — never write straight into `docs/`.
2. Fill the **frontmatter**: `project`, `repo`, `ref` (commit analyzed), `stack`,
   `kb_target`, `last_verified_commit`.
3. Use **[`code-recon`](../code-recon/SKILL.md)** to fill §5–9 (components, endpoints,
   scenarios, algorithms) — every technical claim anchored to `file:line`.
4. Fill business sections §1–3, §11–13 from requirements + code.
5. Build the **mandatory Mermaid diagrams**: Context/C4 (§4), Block (§5), BPMN (§7,
   flowchart approximation or embedded `.bpmn`), Sequence (§8), Flow/State (§9).
6. Keep every heading. Unknown/irrelevant section → `N/A — <reason>`, never delete.
7. Update §15 changelog and `last_verified_commit`.

## Rules

- Read-only against code repos; full read/write only inside `local_documentation/`.
- Draft in `drafts/`; move to `docs/` only when the operator says it is ready.
- **Do not publish.** Sending to a KB (Confluence/Notion/GDocs) is a separate, explicit,
  operator-initiated step (`AGENTS.md` §4).
- Relative markdown links, not `file:///`.
