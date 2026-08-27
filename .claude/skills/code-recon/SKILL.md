---
name: code-recon
description: Analyze a code repository (Laravel, Quarkus, Spring, FastAPI, or Vue.js) to detect its stack, entry points, and HTTP/async endpoints, then describe how it works and its key algorithms. Use when documenting a project, mapping endpoints, or answering "what are the entry points / how does this service work" for a repo.
---

# code-recon — repository technical analysis

Produce the raw technical facts that feed section 5–9 of
[`templates/project-doc-template.md`](../../../templates/project-doc-template.md):
components, **entry points & endpoints**, key scenarios, and algorithms.

## Ground rules

- **Read-only.** Never modify the target repository (see `AGENTS.md` Operating Principles).
- Anchor every finding to `file:line`. No claim without a source location.
- If the stack is ambiguous or mixed, say so and analyze each part.

## Procedure

### Step 0 — README-first hint (fast, non-authoritative)
Read the repository's `README*` (and any `docs/`, `CONTRIBUTING.md`) to form a first guess:
which **language + framework**, what the service **does** (domain), how it is **run**.
Extract candidate stack keywords (e.g. "Laravel", "Quarkus", "FastAPI", "Vue 3").
> Treat the README as a hint only — it can be stale or wrong. Never finalize the stack on
> the README alone; confirm in Step 1.

### Step 1 — Confirm the stack from manifests (authoritative)
Verify the guess against dependency manifests; the manifest wins on conflict:
- `composer.json` (+ `laravel/framework`) → **Laravel**
- `pom.xml` / `build.gradle` with `io.quarkus` → **Quarkus**; with `spring-boot` → **Spring**
- `pyproject.toml` / `requirements.txt` with `fastapi` → **FastAPI**
- `package.json` with `vue` → **Vue.js** (frontend)

Record the framework **version** from the manifest — conventions differ across major versions.

### Step 2 — Load the framework knowledge-base
Load only the KB for the confirmed stack (progressive disclosure — do not read the others):

| Stack | Knowledge-base |
|-------|----------------|
| Laravel | [`knowledge/laravel.md`](knowledge/laravel.md) |
| Quarkus | [`knowledge/quarkus.md`](knowledge/quarkus.md) |
| Spring | [`knowledge/spring.md`](knowledge/spring.md) |
| FastAPI | [`knowledge/fastapi.md`](knowledge/fastapi.md) |
| Vue.js | [`knowledge/vue.md`](knowledge/vue.md) |

The KB holds the detailed entry-point markers, routing/auth conventions, async/scheduling
patterns, and common gotchas for that framework. If the detected **version** or a library
is unfamiliar, fetch current docs via the **context7 MCP** (resolve the library, then query
the specific topic) before relying on assumptions.

> **New stack not covered?** If no KB matches the detected framework, don't guess from
> memory — use the **[`kb-author`](../kb-author/SKILL.md)** skill to research it (README +
> context7) and add `knowledge/<stack>.md` from the template, then continue. See
> [`knowledge/README.md`](knowledge/README.md).

### Step 3 — Enumerate & trace
Using the KB's markers, Grep the repo for entry points. For each: trace entry → handler →
service → data access to describe the flow. Identify key algorithms, state machines,
retries, schedulers.

### Step 4 — Emit
Return an endpoint table (matching template §6) plus notes for §7–9.

## Output shape

Detected **stack + version + confidence**; the endpoint table (template §6 columns); a
short per-endpoint flow note; a list of key algorithms with `file:line`; integrations
observed. Flag anything uncertain rather than guessing.
