---
description: Build a standard Mermaid diagram (Context/C4, Block, BPMN, Sequence, Flow/State)
argument-hint: <diagram type> for <subject>
---

Use the **diagram-builder** skill to build: `$ARGUMENTS`

Produce a Mermaid diagram from the mandatory set that fits the request. For BPMN, state
whether you used a lane-based flowchart approximation or an embedded `.bpmn`. Keep it
readable; label edges with the real protocol/contract. Map it to its numbered section in
the documentation template.
