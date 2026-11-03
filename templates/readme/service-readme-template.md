---
template: service-readme
title: Service / Repository README
standard: none
unit: single
backends: [md, confluence, gdocs]
category: readme
---

---
title: <Service / Repository>
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
# version: n/a — lives with code; = service commit/release (AGENTS.md)
status: draft                # draft | review | approved | deprecated
type: documentation
applies_to: <service >= x.y>  # the service this README belongs to
depends_on: []                # optional
backend: md
target: <repo root README.md, or space/folder when mirrored>
unit: single
---

# <Service / Repository>

> The README lives **in the repo** (backend `md` by default). Mirror to a KB only if the
> team keeps service docs there.

One-paragraph description: what this service does and where it sits in the system.
Link [[C4 architecture]].

## 1. Purpose
What it is responsible for; what it is **not**.

## 2. Tech stack
Language, framework, datastore, key libraries.

## 3. Run locally
```bash
# prerequisites, install, start
```
Ports, URLs, and how to reach it once running.

## 4. Configuration (environment variables)
| Variable | Required | Default | Description |
|----------|----------|---------|-------------|

> Names only — **never** real secret values. See [[Deployment & infrastructure]] for how
> secrets are provided per environment.

## 5. Tests
```bash
# how to run unit / integration tests
```

## 6. Dependencies
Upstream/downstream services, external APIs, message brokers, databases.

## 7. Entry points
Main entry point(s), key endpoints (link [[Integration / API Contract]]), scheduled jobs,
consumers.

## 8. Troubleshooting / links
Common local issues; links to [[Runbook]], dashboards, the service owner / on-call.
