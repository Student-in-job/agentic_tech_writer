---
# META-TEMPLATE — structure every template file follows.
# Copy to templates/<category>/<id>-template.md, fill, and register in templates/README.md.
# The block below is the frontmatter each TEMPLATE declares about itself:
template: <id>                 # kebab-case, unique (e.g. adr, nfr, api-contract)
title: <Human Title>
standard: none                 # none | C4 | TOGAF | BIAN
unit: single                   # single | multi  (multi = parent + children, e.g. per service)
backends: [confluence, gdocs, md]
category: <requirements|architecture|api|readme|user|partner|ops|release|general>
---

<!--
AUTHORING NOTES (remove when creating a real template):
- Below is the DOCUMENT skeleton the template produces. Keep headings stable so documents
  are uniform. Author it backend-agnostic (plain Markdown); the template-library skill maps
  sections to a page/file per backend.
- Every produced document starts with its OWN frontmatter (author/created/type + backend,
  space/folder, unit). Include that block at the top of the skeleton.
- For unit: multi — describe the parent (overview/index) and the per-child skeleton.
- For standard-based templates (C4/TOGAF/BIAN) — ground the section list in the real
  standard (web / context7) before writing.
-->

---
title: <Document Title>
author: System Architect Agent
owner: <team/role>             # accountable owner (mirrors CODEOWNERS)
created: YYYY-MM-DD
updated: YYYY-MM-DD
version: 0.1.0                 # per-group scheme — see AGENTS.md "Documentation Versioning".
                               # OMIT for architecture/data-model/readme/ops (version = service release).
status: draft                  # draft | review | approved | deprecated
type: <architecture | risk-analysis | specification | task | documentation>
applies_to: <service >= x.y>   # optional — the code/version this describes
depends_on: []                 # optional — e.g. [payment-api@2.x]; compat via links
backend: confluence            # confluence | gdocs | md
target: <space/parent or drive-folder or docs path>
unit: single
---

# <Document Title>

## 1. <First section>
…

## 2. <Second section>
…

<!-- multi-unit only: describe child documents -->
## Child documents (unit: multi)
- `<child-id>` — one per <module|service|microservice>: <what each child contains>.
