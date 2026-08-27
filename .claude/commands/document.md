---
description: Produce/update a project's technical documentation from the canonical template
argument-hint: <project or repo>
---

Act as the **tech-writer** agent to document: `$ARGUMENTS`

Drive the full flow:
1. Establish business context & requirements (template §1–3); ask me when they are not
   derivable from code.
2. Use the **code-recon** skill to map stack, entry points, endpoints, algorithms.
3. Use the **diagram-builder** skill for the mandatory diagrams (Context/C4, Block, BPMN,
   Sequence, Flow/State).
4. Use the **doc-template** skill to assemble the document into `drafts/` following the
   canonical section order.

Read-only against code repos; draft in `drafts/`. Do NOT publish anywhere.
