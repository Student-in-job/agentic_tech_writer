# Knowledge base — Vue.js (TypeScript, frontend)

**Identify:** `vue` in `package.json`; `vite.config.*`/`vue.config.js`; `src/` with
`.vue` SFCs; `main.ts`/`main.js`. Version = `vue` pin (Vue 2 Options API vs Vue 3
Composition API differ). Nuxt = `nuxt` dep (file-based routing, different conventions).

## Entry points (frontend)

Vue is a UI, not a backend — "entry points" are **how the app boots, its routes/screens,
and which backend endpoints it calls**.

### Bootstrap
- `main.ts`/`main.js`: `createApp(App).use(router).use(pinia).mount('#app')`.
- **Grep:** `createApp`, `.mount(`.

### Router (screens)
- `vue-router`: `createRouter({ routes: [...] })`, usually `src/router/**`.
- Each route = `{ path, name, component, meta }`; lazy `component: () => import(...)`.
- Nav guards: `beforeEach`/`beforeEnter`, `meta.requiresAuth` → the app's auth gating.
- **Grep:** `createRouter`, `routes:`, `beforeEach`, `requiresAuth`.
- Nuxt: routes are files under `pages/` (no explicit router table).

### Views / pages / components
- `src/views/**` or `src/pages/**` = screens; `src/components/**` = reusable UI.
- State: Pinia stores `src/stores/**` (`defineStore`) or Vuex.

### Backend calls (the real integration surface)
- HTTP clients: `axios` instance (`src/api/**`, interceptors add auth headers), `fetch`,
  `useFetch`/`$fetch` (Nuxt), TanStack Query, Apollo (GraphQL).
- **List which backend endpoints the UI consumes** — this maps the frontend to its API.
- **Grep:** `axios`, `fetch\(`, `useFetch`, `\$fetch`, `baseURL`, `/api/`.

## Auth
- Token storage (localStorage/cookies), axios interceptor injecting `Authorization`,
  route guard `meta.requiresAuth`. Describe the client-side auth flow, not server checks.

## Config & integrations
- Env: `import.meta.env.VITE_*` (Vite) or `.env` (Nuxt `runtimeConfig`). API base URL is
  the key integration config.

## Gotchas
- SPA routes are client-side — they are **not** server endpoints; don't confuse them.
- The meaningful "integration contract" is the set of **backend API calls**, so pair this
  analysis with the backend repo's `code-recon` to connect UI → API.
- `.vue` SFC has `<script setup>` (Composition) — props/emits define the component contract.
- Nuxt adds server routes under `server/api/**` — those ARE real HTTP endpoints; analyze
  them like a backend.
