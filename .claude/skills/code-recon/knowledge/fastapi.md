# Knowledge base — FastAPI (Python)

**Identify:** `fastapi` in `pyproject.toml`/`requirements.txt`; an `app = FastAPI(...)`
instance; often `uvicorn`/`gunicorn` in run config. Version = `fastapi` pin.

## Entry points

### HTTP routes
- Root app: `app = FastAPI()` then `@app.get/post/put/delete/patch("/...")`.
- Modular: `router = APIRouter(prefix="/...")` + `@router.<method>`; wired with
  `app.include_router(router, prefix=..., dependencies=...)`.
- Path/query/body via typed params + Pydantic models; `response_model=` documents output.
- **Grep:** `FastAPI\(`, `APIRouter\(`, `@app\.(get|post|put|delete|patch|websocket)`,
  `@router\.`, `include_router`.

### Lifecycle / background
- `lifespan=` async context manager (modern) or `@app.on_event("startup"|"shutdown")`.
- `BackgroundTasks` params; external task queues (Celery `@shared_task`/`@app.task`,
  ARQ, Dramatiq) if present.
- WebSockets: `@app.websocket("/ws")`.
- **Grep:** `on_event`, `lifespan`, `BackgroundTasks`, `@shared_task`, `websocket`.

## Auth & dependencies
- Auth via dependencies: `Depends(...)`, `OAuth2PasswordBearer`, `APIKeyHeader`,
  `HTTPBearer`. Router/route `dependencies=[Depends(...)]` gate access.
- **Grep:** `Depends(`, `OAuth2PasswordBearer`, `APIKeyHeader`, `Security(`.
- Map the dependency chain to the `Auth` column — dependencies are the middleware analog.

## Data access
- ORM: SQLAlchemy (`declarative_base`, `Mapped[...]`) or SQLModel or Tortoise/Beanie
  (Mongo). Migrations: Alembic (`alembic/versions`).
- Pydantic **schemas** (request/response) vs ORM **models** — keep them distinct in §10.

## Config & integrations
- Settings via `pydantic-settings` `BaseSettings` (env-driven). Outbound HTTP: `httpx`,
  `requests`. Message brokers via Celery/aio-pika config.

## Gotchas
- Route order matters: first match wins; static paths must precede `/{param}` catch-alls.
- `include_router` stacks prefixes → real path = app prefix + router prefix + route path.
- Dependencies can be declared at app, router, or route level — check all three for auth.
- `response_model` may hide/rename fields vs the internal model.
