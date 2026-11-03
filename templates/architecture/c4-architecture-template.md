---
template: c4-architecture
title: C4 Architecture Description
standard: C4
unit: single
backends: [confluence, gdocs, md]
category: architecture
---

---
title: <System> — Architecture (C4)
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
# version: n/a — lives with code; = service commit/release (AGENTS.md)
status: draft                # draft | review | approved | deprecated
type: architecture
applies_to: <service >= x.y>  # the code/version this describes
depends_on: []                # optional
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: single
---

# <System> — Architecture (C4)

Structured on the **C4 model** (Context → Container → Component → Code). Each level zooms
in one step; include only the levels that add clarity (Code level usually optional).

## 1. Context (C4 L1)
The system as a black box: users, external systems, and their interactions.

```mermaid
C4Context
    title System Context — <System>
    Person(user, "User", "…")
    System(sys, "<System>", "…")
    System_Ext(ext, "External System", "…")
    Rel(user, sys, "Uses")
    Rel(sys, ext, "Calls", "HTTPS/JSON")
```

## 2. Containers (C4 L2)
Deployable/runnable units (apps, services, datastores, queues) and how they communicate.

```mermaid
C4Container
    title Containers — <System>
    Person(user, "User")
    Container(api, "API", "<tech>", "…")
    ContainerDb(db, "Database", "<tech>", "…")
    Rel(user, api, "Uses", "HTTPS")
    Rel(api, db, "Reads/writes", "<protocol>")
```

## 3. Components (C4 L3)
Inside a chosen container: its major components/modules and responsibilities.

```mermaid
C4Component
    title Components — <Container>
    Component(ctrl, "Controller", "…")
    Component(svc, "Service", "…")
    Rel(ctrl, svc, "Calls")
```

## 4. Code (C4 L4) — optional
Only for the most critical component: key classes/functions (or a link to the code).

## 5. Cross-cutting
Deployment/topology, security boundaries, key data flows, and decisions (link [[ADR]]).
