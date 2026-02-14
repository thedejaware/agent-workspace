# Pattern Recognition

This reference provides guidance on identifying architectural patterns, design patterns, framework-specific patterns, and anti-patterns from code structure.

## Architectural Patterns

### Monolith

**How to recognize:**
- Single deployable unit
- One main entry point
- Shared database
- All code in one repository with no service boundaries
- Single build and deploy process

**Directory structure signature:**
```
project/
├── src/
│   ├── controllers/     # or routes/
│   ├── services/
│   ├── models/
│   ├── middleware/
│   └── utils/
├── tests/
└── package.json         # single manifest
```

**Strengths:** Simple deployment, easy local development, straightforward debugging.
**Watch for:** Growing complexity, long build times, difficulty scaling individual components.

### Modular Monolith

**How to recognize:**
- Single deployable unit, but code organized by business domain
- Each module has its own models, services, and controllers
- Modules communicate through well-defined interfaces
- May have a shared kernel for cross-cutting concerns

**Directory structure signature:**
```
project/
├── src/
│   ├── modules/
│   │   ├── users/
│   │   │   ├── controllers/
│   │   │   ├── services/
│   │   │   ├── models/
│   │   │   └── index.ts      # public API for this module
│   │   ├── orders/
│   │   │   ├── controllers/
│   │   │   ├── services/
│   │   │   ├── models/
│   │   │   └── index.ts
│   │   └── shared/            # shared kernel
│   └── app.ts
```

**Strengths:** Clear boundaries, easier to split into services later, organized by business domain.
**Watch for:** Cross-module imports that bypass the public interface.

### Microservices

**How to recognize:**
- Multiple independently deployable services
- Each service has its own database or data store
- Services communicate via HTTP, gRPC, or message queues
- Separate repositories or monorepo with distinct services
- Docker compose or Kubernetes configuration defining service topology

**Directory structure signature:**
```
project/
├── services/
│   ├── user-service/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   └── package.json
│   ├── order-service/
│   │   ├── src/
│   │   ├── Dockerfile
│   │   └── package.json
│   └── notification-service/
├── shared/                    # shared libraries/types
├── docker-compose.yml
└── kubernetes/                # or terraform/
```

**Strengths:** Independent scaling, technology flexibility, team autonomy.
**Watch for:** Distributed system complexity, data consistency challenges, service-to-service communication overhead.

### Event-Driven Architecture

**How to recognize:**
- Event emitters and handlers throughout the code
- Message queue configuration (RabbitMQ, Kafka, SQS, NATS)
- Event classes/types defined separately from handlers
- Async processing for operations that don't need immediate response
- Commands and events as first-class concepts

**Code signature:**
```javascript
// Event definitions
class OrderPlaced extends DomainEvent { ... }
class PaymentProcessed extends DomainEvent { ... }

// Event handlers
@EventHandler(OrderPlaced)
class SendOrderConfirmation { ... }

// Event publishing
eventBus.publish(new OrderPlaced(order));
```

**Strengths:** Loose coupling, scalability, natural audit trail.
**Watch for:** Eventual consistency complexity, event ordering issues, difficulty tracing full request lifecycle.

### Layered Architecture

**How to recognize:**
- Clear horizontal layers with strict dependency direction
- Presentation -> Business Logic -> Data Access -> Database
- Each layer only calls the layer directly below it

**Code signature:**
```
Controller (receives HTTP request)
  → Service (applies business rules)
    → Repository (accesses database)
      → Database
```

**Strengths:** Clear separation of concerns, easy to understand.
**Watch for:** Tendency to pass data through multiple layers unchanged, can feel over-engineered for simple operations.

### Hexagonal / Ports and Adapters

**How to recognize:**
- Domain logic at the center with no external dependencies
- "Ports" (interfaces) defined by the domain
- "Adapters" that implement ports for specific technologies
- Clear separation between domain code and infrastructure code

**Directory structure signature:**
```
project/
├── src/
│   ├── domain/              # core business logic (no imports from outside)
│   │   ├── models/
│   │   ├── services/
│   │   └── ports/           # interfaces for external interactions
│   ├── adapters/            # implementations of ports
│   │   ├── persistence/     # database adapters
│   │   ├── http/            # HTTP controllers
│   │   └── messaging/       # queue adapters
│   └── config/              # wiring adapters to ports
```

**Strengths:** Testable domain logic, technology-agnostic core, easy to swap implementations.
**Watch for:** Over-abstraction for simple projects, many small files.

### Serverless / Function-as-a-Service

**How to recognize:**
- Individual function files mapped to specific events or HTTP endpoints
- Cloud provider configuration (AWS SAM, Serverless Framework, Vercel config)
- No persistent server process
- Cold start considerations in the code

**Directory structure signature:**
```
project/
├── functions/
│   ├── createUser.ts
│   ├── processOrder.ts
│   └── sendNotification.ts
├── serverless.yml           # or template.yaml, vercel.json
└── shared/                  # shared utilities between functions
```

## Design Patterns in Code

### Repository Pattern

**How to recognize:**
- Classes or modules named `*Repository`, `*Repo`, `*Store`, `*DAO`
- Encapsulate all data access logic behind an interface
- Return domain objects, not raw database rows

**Code signature:**
```typescript
interface UserRepository {
  findById(id: string): Promise<User>;
  findByEmail(email: string): Promise<User | null>;
  save(user: User): Promise<User>;
  delete(id: string): Promise<void>;
}

class PostgresUserRepository implements UserRepository {
  // database-specific implementation
}
```

### Service Layer Pattern

**How to recognize:**
- Classes or modules named `*Service`, `*UseCase`, `*Handler`
- Orchestrate business logic by coordinating multiple repositories or other services
- No direct database access -- delegate to repositories
- Transaction management

**Code signature:**
```python
class OrderService:
    def __init__(self, order_repo, product_repo, payment_service):
        self.order_repo = order_repo
        self.product_repo = product_repo
        self.payment_service = payment_service

    def place_order(self, cart, payment_info):
        # orchestrate multiple steps
        products = self.product_repo.find_by_ids(cart.product_ids)
        order = Order.create(products, cart.quantities)
        payment = self.payment_service.charge(payment_info, order.total)
        order.confirm(payment.id)
        self.order_repo.save(order)
        return order
```

### Dependency Injection

**How to recognize:**
- Constructor parameters for dependencies (not created internally)
- DI containers or modules (NestJS modules, Spring beans, .NET service registrations)
- Interfaces/abstractions used as parameter types
- Factory functions that wire dependencies together

**Code signature:**
```csharp
// Registration
builder.Services.AddScoped<IUserRepository, PostgresUserRepository>();
builder.Services.AddScoped<IUserService, UserService>();

// Usage (injected via constructor)
public class UserService : IUserService
{
    private readonly IUserRepository _repo;
    public UserService(IUserRepository repo) => _repo = repo;
}
```

### Middleware / Pipeline Pattern

**How to recognize:**
- Functions that receive a request, do something, and call `next()`
- Ordered chain of processing steps
- Cross-cutting concerns like auth, logging, error handling

**Code signature:**
```javascript
// Express middleware
app.use(requestLogger);
app.use(authenticate);
app.use(rateLimiter);
app.use('/api', apiRouter);
app.use(errorHandler);
```

### Observer / Event Emitter Pattern

**How to recognize:**
- `EventEmitter`, `Subject`, `Observable` usage
- `on()`, `emit()`, `subscribe()`, `publish()` method calls
- Decoupled communication between components

**Code signature:**
```typescript
class OrderEvents extends EventEmitter {}

// Publisher
orderEvents.emit('order:placed', order);

// Subscribers (possibly in different files)
orderEvents.on('order:placed', sendConfirmationEmail);
orderEvents.on('order:placed', updateInventory);
orderEvents.on('order:placed', notifyWarehouse);
```

### Strategy Pattern

**How to recognize:**
- Interface with multiple implementations
- Implementation selected at runtime based on conditions
- Common in payment processing, notification sending, data export

**Code signature:**
```python
class NotificationStrategy(ABC):
    @abstractmethod
    def send(self, user, message): ...

class EmailNotification(NotificationStrategy):
    def send(self, user, message): ...

class SMSNotification(NotificationStrategy):
    def send(self, user, message): ...

class PushNotification(NotificationStrategy):
    def send(self, user, message): ...

# Selection
def get_notifier(channel: str) -> NotificationStrategy:
    strategies = {'email': EmailNotification, 'sms': SMSNotification, 'push': PushNotification}
    return strategies[channel]()
```

### Factory Pattern

**How to recognize:**
- Functions or classes named `*Factory`, `create*`, `build*`, `make*`
- Encapsulate object creation logic
- Often used with dependency injection

**Code signature:**
```typescript
function createDatabaseConnection(config: DatabaseConfig): Database {
  switch (config.type) {
    case 'postgres': return new PostgresDatabase(config);
    case 'mysql': return new MySQLDatabase(config);
    case 'sqlite': return new SQLiteDatabase(config);
    default: throw new Error(`Unsupported database: ${config.type}`);
  }
}
```

### Command / CQRS Pattern

**How to recognize:**
- Separate classes/types for commands and queries
- Write operations (commands) separated from read operations (queries)
- Command handlers and query handlers as separate concepts
- Possibly separate read and write database models

**Code signature:**
```typescript
// Commands (write operations)
class CreateUserCommand { constructor(public name: string, public email: string) {} }
class UpdateUserCommand { constructor(public id: string, public data: Partial<User>) {} }

// Queries (read operations)
class GetUserQuery { constructor(public id: string) {} }
class ListUsersQuery { constructor(public filters: UserFilters) {} }

// Separate handlers
class CreateUserHandler { execute(cmd: CreateUserCommand): Promise<User> { ... } }
class GetUserHandler { execute(query: GetUserQuery): Promise<UserView> { ... } }
```

## Framework-Specific Patterns

### React

| Pattern | Signature | Where to Look |
|---------|-----------|---------------|
| Component composition | Components rendering other components as children | JSX/TSX files |
| Custom hooks | `use*` functions extracting reusable stateful logic | `hooks/` directory |
| Context providers | `createContext` + `Provider` + `useContext` | `context/` or `providers/` |
| Render props | Components accepting functions as props | Component prop types |
| Higher-order components | Functions wrapping components: `withAuth(Component)` | `hoc/` directory or `with*` files |
| Container/presentational | Smart components (data) + dumb components (UI) | `containers/` vs `components/` |
| Compound components | Related components sharing implicit state | Component libraries |

### Express / Fastify / Koa

| Pattern | Signature | Where to Look |
|---------|-----------|---------------|
| Route grouping | `Router()` instances grouped by feature | `routes/` directory |
| Middleware chain | `app.use()` calls in specific order | `app.ts` or `middleware/` |
| Error middleware | `(err, req, res, next)` four-parameter functions | Last middleware registered |
| Request validation | `celebrate`, `zod`, `joi` schema validation | Middleware before handlers |
| Controller classes | Classes with methods mapped to routes | `controllers/` directory |

### Django

| Pattern | Signature | Where to Look |
|---------|-----------|---------------|
| MVT (Model-View-Template) | `models.py`, `views.py`, `templates/` | Each Django app |
| Class-based views | Classes extending `View`, `APIView`, `ViewSet` | `views.py` |
| Serializers | Classes extending `Serializer` (DRF) | `serializers.py` |
| Signals | `@receiver` decorators, `Signal` instances | `signals.py` |
| Custom managers | `Manager` subclasses on models | `models.py` or `managers.py` |
| Middleware | Classes with `__call__` or `process_*` methods | `MIDDLEWARE` in `settings.py` |

### Spring Boot

| Pattern | Signature | Where to Look |
|---------|-----------|---------------|
| Layered architecture | `@Controller`, `@Service`, `@Repository` | Package organization |
| Auto-configuration | `@SpringBootApplication`, `application.yml` | Main class and config |
| Bean injection | `@Autowired`, `@Bean`, constructor injection | Service constructors |
| AOP | `@Aspect`, `@Around`, `@Before` annotations | `aspect/` package |
| Profiles | `@Profile`, `application-{profile}.yml` | Config files |
| JPA repositories | Interfaces extending `JpaRepository` | `repository/` package |

### NestJS

| Pattern | Signature | Where to Look |
|---------|-----------|---------------|
| Modules | `@Module()` decorator grouping providers | `*.module.ts` files |
| Dependency injection | Constructor parameter injection | Service constructors |
| Guards | `@UseGuards()`, `CanActivate` interface | `guards/` directory |
| Interceptors | `@UseInterceptors()`, `NestInterceptor` | `interceptors/` directory |
| Pipes | `@UsePipes()`, `PipeTransform` | `pipes/` directory |
| DTOs | Classes with validation decorators | `dto/` directories |

### ASP.NET Core

| Pattern | Signature | Where to Look |
|---------|-----------|---------------|
| Minimal APIs | `app.MapGet()`, `app.MapPost()` | `Program.cs` |
| Controller-based | Classes extending `ControllerBase` | `Controllers/` directory |
| Middleware pipeline | `app.Use*()` calls | `Program.cs` |
| Service registration | `builder.Services.Add*()` | `Program.cs` or extension methods |
| Options pattern | `IOptions<T>`, `Configure<T>()` | Configuration classes |
| Entity Framework | `DbContext`, `DbSet<T>`, migrations | `Data/` or `Persistence/` directory |

## Anti-Patterns and Code Smells

### Architectural Anti-Patterns

**God class / God module:**
- One class or file that does everything
- Dozens or hundreds of methods
- Imported by nearly every other file
- Sign: A single file with 1000+ lines that keeps growing

**Circular dependencies:**
- Module A imports from Module B, which imports from Module A
- Often hidden through indirect chains (A -> B -> C -> A)
- Sign: Import errors, difficult to test in isolation

**Distributed monolith:**
- Multiple services that must be deployed together
- Services that share a database
- Tight coupling between services requiring synchronized changes
- Sign: Changing one service requires deploying several others

**Anemic domain model:**
- Entity classes with only data (getters/setters) and no behavior
- All business logic in service classes
- Models are just data transfer objects
- Sign: Service classes that manipulate entity properties directly

**Spaghetti architecture:**
- No clear layering or module boundaries
- Any file can import from any other file
- Business logic mixed with presentation and data access
- Sign: No consistent import patterns

### Code-Level Smells

**Feature envy:**
- A method that uses more features of another class than its own
- Sign: Chains of method calls on another object

**Shotgun surgery:**
- A single change requires editing many files across the codebase
- Sign: Small feature changes touch 10+ files

**Primitive obsession:**
- Using primitive types (strings, numbers) instead of domain types
- Sign: Email addresses, IDs, and money amounts as raw strings/numbers

**Long parameter lists:**
- Functions with 5+ parameters
- Sign: Often indicates the function is doing too much

**Dead code:**
- Unused functions, classes, imports, or variables
- Commented-out code blocks
- Feature flags that are always on/off
- Sign: Code coverage tools showing 0% coverage on specific areas

### How to Flag Anti-Patterns

When you identify anti-patterns, report them with:

1. **What** -- Name the pattern and where it occurs
2. **Impact** -- Why it's a problem (maintainability, performance, reliability)
3. **Evidence** -- Specific files or code that demonstrate the issue
4. **Severity** -- How urgent is it? (critical, moderate, minor)
5. **Suggested approach** -- How it could be improved (without over-prescribing)

Example:
```
Anti-pattern: Circular dependency between `users/` and `organizations/` modules
Impact: Makes both modules difficult to test independently and creates tight coupling
Evidence: users/service.ts imports from organizations/service.ts (line 5)
          organizations/service.ts imports from users/service.ts (line 8)
Severity: Moderate -- works but will make refactoring harder over time
Approach: Extract shared types to a common module, or use events for cross-module communication
```
