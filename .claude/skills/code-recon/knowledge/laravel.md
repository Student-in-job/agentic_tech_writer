# Knowledge base — Laravel (PHP)

**Identify:** `composer.json` has `laravel/framework`; `artisan` file at root; `app/`,
`routes/`, `bootstrap/app.php`. Version = `laravel/framework` constraint in `composer.json`.

## Entry points

### HTTP routes
- `routes/api.php` (prefix `/api`, stateless), `routes/web.php` (session/CSRF),
  `routes/channels.php` (broadcast), `routes/console.php` (closures).
- Definitions: `Route::get|post|put|patch|delete(...)`, `Route::apiResource(...)`,
  `Route::resource(...)`, `Route::group([...], ...)`, `Route::prefix(...)->group(...)`.
- Controllers: `app/Http/Controllers/**`. Method = handler. Also invokable controllers
  (`__invoke`). Laravel 11+ may use route attributes.
- **Grep:** `Route::`, `apiResource`, `class \w+ extends Controller`, `function __invoke`.

### Console / scheduled
- Commands: `app/Console/Commands/**` — `protected $signature = '...'`.
- Scheduler: `app/Console/Kernel.php` `schedule()` (or `routes/console.php` in L11+).
- **Grep:** `protected \$signature`, `->command(`, `->cron(`, `->daily(`.

### Async / events
- Queued jobs: `app/Jobs/**` `implements ShouldQueue` — entry = `handle()`.
- Listeners: `app/Listeners/**`; events `app/Events/**`.
- Broadcasting: events `implements ShouldBroadcast`.
- **Grep:** `ShouldQueue`, `ShouldBroadcast`, `dispatch(`, `class \w+ implements`.

## Auth & middleware
- Middleware in route groups (`->middleware('auth:sanctum')`, `auth:api`).
- Guards/providers in `config/auth.php`; Sanctum/Passport tokens; policies in `app/Policies`.
- Map each route's middleware stack to the `Auth` column of the endpoint table.

## Data access
- Eloquent models `app/Models/**`; migrations `database/migrations/**` (schema/§10).
- Relationships = methods returning `hasMany/belongsTo/...`.

## Config & integrations
- `.env` + `config/**`. External HTTP via `Http::` (Guzzle). Queues/Redis in `config/queue.php`.

## Gotchas
- Route model binding hides lookups (`/users/{user}` auto-resolves).
- Middleware aliases live in `Kernel.php` (or `bootstrap/app.php` in L11+).
- FormRequest classes (`app/Http/Requests`) carry validation + authorization — read them.
- API version prefixes often set in a route group, not per-route.
