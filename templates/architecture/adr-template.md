---
template: adr
title: Architecture Decision Record
standard: none
unit: single
backends: [confluence, gdocs, md]
category: architecture
---

---
title: "ADR-<NNN>: <short decision title>"
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
# version: n/a — ADRs are immutable & numbered; supersede instead of editing (AGENTS.md)
status: proposed             # proposed | accepted | deprecated | superseded
superseded_by:               # e.g. ADR-0012, set when this record is replaced
type: architecture
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: single
---

# ADR-<NNN>: <short decision title>

- **Status:** Proposed | Accepted | Superseded by [[ADR-XXX]] | Deprecated
- **Date:** YYYY-MM-DD
- **Deciders:** …
- **Related:** [[FR]] / [[NFR]] / [[C4 architecture]]

## Context
The forces at play: problem, constraints, requirements (link FR/NFR), and what makes this
decision necessary now. Facts, not opinions.

## Decision
The change we are making, stated in one clear sentence, then the specifics.

## Options considered
| Option | Pros | Cons |
|--------|------|------|
| A (chosen) | … | … |
| B | … | … |

## Consequences
- **Positive:** …
- **Negative / trade-offs:** …
- **Follow-ups / risks:** … (link tasks)

## Compliance
How the decision aligns with the relevant standard(s) (C4/TOGAF/BIAN) or why it deviates.
