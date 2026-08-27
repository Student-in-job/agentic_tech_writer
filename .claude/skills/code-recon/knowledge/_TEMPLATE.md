# Knowledge base — <Framework> (<Language>)

<!--
KB TEMPLATE. Copy to knowledge/<stack>.md and fill every section.
Keep the section order — code-recon and kb-author rely on it.
Rules:
- Every entry-point kind must give concrete **Grep markers** (regex-ish, real symbols).
- Prefer authoritative signals (manifest, annotations, decorators) over prose.
- Note the framework VERSION differences where conventions changed across majors.
- If unsure of current conventions, verify via context7 MCP before writing.
Remove these comments when done.
-->

**Identify:** <manifest signal, e.g. `dep` in `pyproject.toml`/`pom.xml`/`package.json`>;
<root files/dirs that mark the framework>. Version = <where the version is read from>.

## Entry points

### HTTP routes
- <how routes/controllers are declared>.
- <path/param/body conventions>.
- **Grep:** `<marker1>`, `<marker2>`.

### Messaging / async  <!-- omit if N/A -->
- <queue/stream consumers & producers, background tasks>.
- **Grep:** `<marker>`.

### Scheduled / lifecycle  <!-- omit if N/A -->
- <cron/scheduled jobs; startup/shutdown hooks>.
- **Grep:** `<marker>`.

## Auth & security
- <how auth is applied: middleware/guards/dependencies/annotations>.
- <where config lives>. Map each entry point's guard to the `Auth` column of template §6.
- **Grep:** `<marker>`.

## Data access
- <ORM/repository pattern, entity markers, migrations location> — feeds template §10.

## Config & integrations
- <config files, env conventions>. Outbound clients / external calls markers.
- **Grep:** `<marker>` for outbound integrations.

## Gotchas
- <path-prefix stacking, route ordering, hidden global config, reactive vs blocking,
  version-specific traps — the things that make analysis wrong if missed>.
