# Knowledge base — Quarkus (Java/Kotlin)

**Identify:** `pom.xml`/`build.gradle` with `io.quarkus` deps; `application.properties` or
`application.yaml` under `src/main/resources`. Version = `quarkus.platform.version` /
`io.quarkus:quarkus-bom`.

## Entry points

### REST (JAX-RS / RESTEasy Reactive)
- Resource classes with `@Path("/...")` at class + method level.
- Methods: `@GET @POST @PUT @DELETE @PATCH`, plus `@Produces/@Consumes`.
- Path params `@PathParam`, query `@QueryParam`, body = method param.
- **Grep:** `@Path`, `@GET|@POST|@PUT|@DELETE|@PATCH`, `@Produces`.

### Messaging (SmallRye Reactive Messaging / Kafka)
- `@Incoming("channel")` (consumer), `@Outgoing("channel")` (producer).
- Channel → connector mapping in `application.properties` (`mp.messaging.incoming.*`).
- **Grep:** `@Incoming`, `@Outgoing`, `@Channel`, `mp.messaging.`.

### Scheduled / lifecycle
- `@Scheduled(cron=...|every=...)`.
- Startup: `@Observes StartupEvent`; `@Startup` beans; `void onStart(@Observes ...)`.
- **Grep:** `@Scheduled`, `StartupEvent`, `@Startup`.

### gRPC (if present)
- `@GrpcService`; proto in `src/main/proto`.

## Auth & security
- `@RolesAllowed`, `@Authenticated`, `@PermitAll`, `@DenyAll` (MicroProfile JWT / OIDC).
- OIDC/JWT config in `application.properties` (`quarkus.oidc.*`). Map to `Auth` column.

## Data access
- Panache: entities extend `PanacheEntity`/`PanacheEntityBase`, or `PanacheRepository`.
- JPA `@Entity`; schema also in Flyway/Liquibase migrations (`src/main/resources/db`).

## Config & integrations
- `application.properties`/`.yaml`; profiles `%dev`, `%prod`. REST clients:
  `@RegisterRestClient` interfaces (`org.eclipse.microprofile.rest.client`).
- **Grep:** `@RegisterRestClient` for outbound integrations.

## Gotchas
- Reactive vs blocking: `Uni<T>`/`Multi<T>` return types (Mutiny) change flow semantics.
- Build-time config: many things fixed at build (`@ConfigProperty`, build steps).
- Constructor injection via `@Inject`; CDI beans (`@ApplicationScoped`) are the services.
- Kotlin projects: same annotations, different file layout.
