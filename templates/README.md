# Document template library

Templates for the analyst+tech-writer role. The **[`template-library`](../.claude/skills/template-library/SKILL.md)**
skill asks which template to use, applies it, and maintains this library.

## The document unit (storage-aware)

A *document* is one logical unit; it materializes per backend:

| Backend | Unit | Multi-unit (split) |
|---------|------|--------------------|
| Confluence | page | parent page + child pages |
| Google Docs | file | folder + files |
| Markdown | `.md` file | folder + `.md` files |

`unit: single` = one page/file. `unit: multi` = a tree (parent/overview + one child per
module / service / microservice) — e.g. the API library.

## Catalog

A documentation set *may* include these (not every project needs all), grouped by the
three lenses: **Business** (why & what) → **Technical** (how it is built) →
**Operations** (how to run it in production).

### Business — why & what
| id | Title | Standard | Unit | Backends | Path |
|----|-------|----------|------|----------|------|
| vision | Vision / One-pager | none | single | confluence, gdocs, md | [requirements/vision-template.md](requirements/vision-template.md) |
| frd | Functional Requirements (FR) | none | single | confluence, gdocs, md | [requirements/frd-template.md](requirements/frd-template.md) |
| nfr | Non-Functional Requirements (NFR) | none | single | confluence, gdocs, md | [requirements/nfr-template.md](requirements/nfr-template.md) |
| glossary | Domain Glossary | none | single | confluence, gdocs, md | [requirements/glossary-template.md](requirements/glossary-template.md) |

> A **PRD / simplified SRS** = `vision` + `frd` + `nfr` together (one or multi-page).

### Technical — how it is built
| id | Title | Standard | Unit | Backends | Path |
|----|-------|----------|------|----------|------|
| c4-architecture | C4 Architecture Description | C4 | single | confluence, gdocs, md | [architecture/c4-architecture-template.md](architecture/c4-architecture-template.md) |
| adr | Architecture Decision Record | none | single | confluence, gdocs, md | [architecture/adr-template.md](architecture/adr-template.md) |
| api-contract | Integration / API Contract (REST / async / gRPC) | none | single | confluence, gdocs, md | [api/api-contract-template.md](api/api-contract-template.md) |
| api-library | API Library (per module/service) | none | multi | confluence, gdocs, md | [api/api-library-template.md](api/api-library-template.md) |
| data-model | Data Model (ER / ownership / migrations) | none | single | confluence, gdocs, md | [architecture/data-model-template.md](architecture/data-model-template.md) |
| service-readme | Service / Repository README | none | single | md, confluence, gdocs | [readme/service-readme-template.md](readme/service-readme-template.md) |

### Operations — how to run it in production
| id | Title | Standard | Unit | Backends | Path |
|----|-------|----------|------|----------|------|
| deployment | Deployment & Infrastructure | none | single | confluence, gdocs, md | [ops/deployment-template.md](ops/deployment-template.md) |
| runbook | Runbook & Monitoring | none | single | confluence, gdocs, md | [ops/runbook-template.md](ops/runbook-template.md) |
| release-notes | Release Notes | none | single | confluence, gdocs, md | [release/release-notes-template.md](release/release-notes-template.md) |

### User-facing — audience is the user (incl. developer users)
| id | Title | Standard | Unit | Backends | Path |
|----|-------|----------|------|----------|------|
| user-guide | User Guide / Help Center | none | single | confluence, gdocs, md | [user/user-guide-template.md](user/user-guide-template.md) |
| admin-guide | Administrator Guide | none | single | confluence, gdocs, md | [user/admin-guide-template.md](user/admin-guide-template.md) |
| developer-portal | Developer Portal (public API) | none | multi | confluence, gdocs, md | [user/developer-portal-template.md](user/developer-portal-template.md) |

> `release-notes` (Operations) doubles as the user-facing **changelog**. The developer
> portal is built **on top of** the `api-contract` / `api-library` OpenAPI contracts.

### Partner / external — integrations with third parties
| id | Title | Standard | Unit | Backends | Path |
|----|-------|----------|------|----------|------|
| integration-registry | Partner Integration Registry | none | multi | confluence, gdocs, md | [partner/integration-registry-template.md](partner/integration-registry-template.md) |
| partner-spec-snapshot | Partner Spec Snapshot | none | single | confluence, gdocs, md | [partner/partner-spec-snapshot-template.md](partner/partner-spec-snapshot-template.md) |
| partner-integration | Partner Integration (our side) | none | single | confluence, gdocs, md | [partner/partner-integration-template.md](partner/partner-integration-template.md) |
| legal-register | Legal & Contractual Register (pointers) | none | single | confluence, gdocs, md | [partner/legal-register-template.md](partner/legal-register-template.md) |

> [!WARNING]
> `legal-register` holds **pointers only** — contracts / NDAs / signed SLAs live in a
> separate access-restricted store, never staged in this workspace.

### Cross-cutting
| id | Title | Standard | Unit | Backends | Path |
|----|-------|----------|------|----------|------|
| project-doc | Project Technical Documentation | none | single | confluence, gdocs, md | [project-doc-template.md](project-doc-template.md) |

**Planned (need grounding via web/context7 before authoring):**

| id | Title | Standard | Status |
|----|-------|----------|--------|
| togaf-* | TOGAF ADM artifacts (Vision, Business/Data/App/Tech Architecture) | TOGAF | to research |
| bian-service-domain | BIAN Service Domain / Landscape | BIAN | to research |

## Versioning

How authored documents are versioned is **not** one global scheme — each group has its own
(SemVer only for API contracts, immutable ADRs, release-tied user docs, snapshots for
partner docs, "as-code" for ops). The authoritative rule, the per-group table, and the
frontmatter metadata (`version` / `status` / `owner` / `updated` / `applies_to` /
`depends_on`) are in [`AGENTS.md` → Documentation Versioning](../AGENTS.md#documentation-versioning-authored-docs).

## Adding a template

Use the **template-library** skill (procedure B) or by hand:
1. Copy [`_meta-template.md`](_meta-template.md) → `templates/<category>/<id>-template.md`.
2. Fill the self-declaring frontmatter (`template`, `title`, `standard`, `unit`, `backends`).
3. For **standard-based** templates (C4/TOGAF/BIAN), verify the real artifacts via web /
   context7 first — do not invent structure.
4. Register a row in the catalog above.
