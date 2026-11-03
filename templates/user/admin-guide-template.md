---
template: admin-guide
title: Administrator Guide
standard: none
unit: single
backends: [confluence, gdocs, md]
category: user
---

---
title: <Product> — Administrator Guide
author: System Architect Agent
owner: <team/role>            # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0                # tied to product release; folder per major /docs/vN (AGENTS.md)
status: draft                # draft | review | approved | deprecated
type: documentation
applies_to: <product >= x>    # product major this guide documents
depends_on: []                # optional
backend: confluence
target: <space/parent or drive-folder or docs path>
unit: single
---

# <Product> — Administrator Guide

> Audience: **administrators** (people with elevated rights / an admin panel). Use only if
> the system has administration. For running the service in prod, see [[Runbook]] and
> [[Deployment & infrastructure]].

## 1. Admin overview
What admins can do, how to reach the admin area, prerequisites.

## 2. Initial setup / configuration
First-time configuration steps, with screenshots where there is a UI.

## 3. Roles & permissions
| Role | Can do | Cannot do | Assigned to |
|------|--------|-----------|-------------|

How roles are assigned/revoked; default roles.

## 4. User & access management
Create/disable users, reset access, audit who did what.

## 5. System settings
Configurable options, feature flags, integrations toggles (names, not secrets).

## 6. Monitoring & housekeeping (admin-visible)
Admin dashboards, usage/limits, routine admin tasks.

## 7. Troubleshooting (admin)
| Symptom | Likely cause | Admin action | Escalate to |
|---------|--------------|--------------|-------------|
