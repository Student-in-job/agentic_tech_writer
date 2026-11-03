---
template: runbook
title: Runbook & Monitoring
standard: none
unit: single
backends: [confluence, gdocs, md]
category: ops
---

---
title: <Service> — Runbook
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
# version: n/a — as-code; current main branch is authoritative (AGENTS.md)
status: draft                # draft | review | approved | deprecated
type: documentation
applies_to: <service >= x.y>
depends_on: []                # optional
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: single
---

# <Service> — Runbook

## 1. Service summary
What it does, criticality/tier, owning team, on-call contact.

## 2. Architecture at a glance
Key components, dependencies (upstream/downstream), datastores. Link [[C4 architecture]].

## 3. Run & deploy
How to start/stop/restart, deploy, roll back. Environments and their URLs.

## 4. Configuration
Env vars / config keys (names only, no secrets), feature flags.

## 5. Observability
Where to look: dashboards, logs (query examples), metrics, key SLIs/SLOs, alerts.

## 6. Health & readiness
Health endpoints, expected responses, what "healthy" means.

## 7. Common incidents & responses
| Symptom | Likely cause | Diagnosis | Action |
|---------|--------------|-----------|--------|

## 8. Escalation
When and to whom to escalate; severity definitions.

## 9. Maintenance
Backups/restore, routine jobs, capacity/scaling actions.
