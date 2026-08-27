---
name: diagram-builder
description: Build the standard project diagrams as Mermaid — Context/C4, Block, BPMN (flowchart approximation), Sequence, and Flow/State. Use when a document needs a diagram, when visualizing a system's structure or a flow, or when converting code-recon findings into diagrams.
---

# diagram-builder — standard Mermaid diagrams

Turn analysis into the workspace's **mandatory diagram set**. All diagrams are Mermaid so
they render inline in Markdown, Confluence, and Notion.

## Mandatory set (and when to use each)

| Diagram | Mermaid syntax | Use for |
|---------|----------------|---------|
| **Context / C4** | `C4Context` / `C4Container` | system boundary, external actors/systems |
| **Block** | `block-beta` | internal components, layers, datastores |
| **BPMN** | `flowchart` w/ `subgraph` lanes | end-to-end business process |
| **Sequence** | `sequenceDiagram` | a request/flow across components over time |
| **Flow / State** | `flowchart` / `stateDiagram-v2` | algorithms, lifecycles, state machines |

## Rules

- **BPMN caveat:** Mermaid has no native BPMN. Either approximate with a lane-based
  `flowchart`, or embed an image exported from a BPMN tool and commit the `.bpmn` source
  beside the doc. State which one you used.
- Keep diagrams readable: split large ones rather than one giant graph.
- Label edges with the real protocol/contract (`HTTPS/JSON`, `Kafka`, `gRPC`) when known.
- Each diagram maps to its numbered section in
  [`templates/project-doc-template.md`](../../../templates/project-doc-template.md).
