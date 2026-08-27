# Knowledge base — Spring Boot (Java/Kotlin)

**Identify:** `pom.xml`/`build.gradle` with `org.springframework.boot`; a
`@SpringBootApplication` main class; `application.properties`/`.yml`. Version =
`spring-boot-starter-parent` / `org.springframework.boot` version.

## Entry points

### REST (Spring MVC / WebFlux)
- `@RestController` (or `@Controller` + `@ResponseBody`) classes.
- Mappings: `@RequestMapping` (class base path) + `@GetMapping/@PostMapping/@PutMapping/`
  `@DeleteMapping/@PatchMapping`.
- Params: `@PathVariable`, `@RequestParam`, `@RequestBody`.
- WebFlux: same annotations but `Mono<T>`/`Flux<T>` returns; or functional `RouterFunction`.
- **Grep:** `@RestController`, `@(Get|Post|Put|Delete|Patch|Request)Mapping`, `RouterFunction`.

### Messaging
- Kafka `@KafkaListener(topics=...)`; RabbitMQ `@RabbitListener`; JMS `@JmsListener`;
  Spring Cloud Stream `@StreamListener`/functional `Consumer<T>` beans.
- **Grep:** `@KafkaListener`, `@RabbitListener`, `@JmsListener`.

### Scheduled / lifecycle
- `@Scheduled(cron=...|fixedRate=...)` (needs `@EnableScheduling`).
- Startup: `CommandLineRunner`, `ApplicationRunner`, `@EventListener(ApplicationReadyEvent)`.
- **Grep:** `@Scheduled`, `CommandLineRunner`, `ApplicationRunner`.

## Auth & security
- Spring Security: `SecurityFilterChain` bean / `WebSecurityConfigurerAdapter` (legacy);
  method security `@PreAuthorize`, `@Secured`, `@RolesAllowed`.
- JWT/OAuth2 resource server config in `application.yml` (`spring.security.oauth2.*`).
- Map filter-chain matchers + method annotations to the `Auth` column.

## Data access
- Spring Data repositories: interfaces extending `JpaRepository`/`CrudRepository`/
  `ReactiveCrudRepository`. Entities `@Entity`. Migrations: Flyway/Liquibase.
- Derived query methods (`findByEmail`) imply queries without SQL.

## Config & integrations
- `application.yml`/`.properties`, profiles (`application-prod.yml`).
- Outbound: `RestTemplate`, `WebClient`, Feign `@FeignClient` interfaces.
- **Grep:** `@FeignClient`, `WebClient`, `RestTemplate`.

## Gotchas
- Base path may be split between `@RequestMapping` on class and method — combine them.
- `server.servlet.context-path` adds a global prefix to every route.
- Global exception handling in `@ControllerAdvice` shapes error responses.
- Bean-wired services (`@Service`, `@Component`) are the domain layer.
