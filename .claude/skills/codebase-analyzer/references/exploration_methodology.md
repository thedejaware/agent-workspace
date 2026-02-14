# Exploration Methodology

This reference provides deep guidance on systematically reading and understanding unfamiliar codebases.

## How to Systematically Read Unfamiliar Code

### The Concentric Circles Approach

Read code from the outside in, like concentric circles:

**Circle 1: Project boundary** (5 minutes)
- Read the README
- Scan all top-level files and directories
- Read the project manifest (package.json, Cargo.toml, etc.)
- Answer: "What is this project and what is it built with?"

**Circle 2: Structural skeleton** (10-15 minutes)
- Read entry points (main files, app initialization)
- Scan directory names and file names in each major directory
- Read configuration files (database, auth, environment)
- Answer: "How is this project organized and what are its main components?"

**Circle 3: Core abstractions** (15-20 minutes)
- Read type definitions, interfaces, and data models
- Read the main service/business logic files
- Skim test files for behavioral expectations
- Answer: "What are the core concepts and how do they relate?"

**Circle 4: Implementation details** (as needed)
- Deep-read specific files to understand algorithms, edge cases, and complex logic
- Trace specific features end-to-end
- Read tests for specific behaviors
- Answer: "How does [specific feature] actually work?"

### The 80/20 Rule for Codebases

Approximately 20% of files define 80% of a codebase's architecture. Identifying this structural skeleton quickly is the key to efficient codebase understanding.

**How to find the skeleton:**

1. **Look for files with the most imports/exports** -- These are the central nodes that everything connects through

2. **Look for files that define types used everywhere** -- Model definitions, shared interfaces, and configuration types are architectural cornerstones

3. **Look for files referenced in configuration** -- Entry points, route registrations, middleware chains, and dependency injection containers define the application's wiring

4. **Look for files that haven't changed much recently** -- Stable files are often foundational. Frequently-changing files are often feature-specific

5. **Look for files that appear in many import paths** -- If many files import from `utils/auth.ts` or `core/database.ts`, those are skeleton files

**Common skeleton file patterns:**

| File Pattern | Architectural Role |
|-------------|-------------------|
| `app.ts`, `server.ts`, `main.ts` | Application bootstrap and wiring |
| `routes.ts`, `router.ts` | Request routing and endpoint registration |
| `middleware/` files | Cross-cutting concerns (auth, logging, errors) |
| `models/`, `entities/`, `types/` | Domain model definitions |
| `config/`, `settings` | Application configuration |
| `db.ts`, `database.ts`, `connection.ts` | Data layer setup |
| `container.ts`, `providers/` | Dependency injection and service registration |

## Techniques for Tracing Execution Paths

### Request Tracing

To understand how a request flows through the system:

1. **Find the route/endpoint definition** -- Search for the URL path or HTTP method
2. **Identify the handler function** -- What function is called when this route is hit?
3. **Read the handler top to bottom** -- Note each function call it makes
4. **Follow each function call one level deep** -- Read the service functions called by the handler
5. **Note the database operations** -- What data is read, written, or modified?
6. **Follow the response construction** -- How is the response built and returned?

**Practical technique:** Create a call chain as you read:

```
POST /api/users
  → userController.create()
    → validateUserInput(body)
    → userService.createUser(data)
      → userRepository.findByEmail(email)    // check for duplicates
      → hashPassword(password)
      → userRepository.save(user)
      → emailService.sendWelcome(user)       // side effect
    → res.status(201).json(user)
```

### Event Tracing

For event-driven systems:

1. **Find event emission points** -- Search for `emit`, `publish`, `dispatch`, `send`
2. **Find event handlers** -- Search for `on`, `subscribe`, `listen`, `handle`
3. **Map event name to handlers** -- Which functions respond to each event?
4. **Trace the handler logic** -- What happens when the event fires?
5. **Look for event chains** -- Does one event handler emit additional events?

### State Tracing

For understanding state management:

1. **Find state definitions** -- Where is the initial state defined?
2. **Find state mutations** -- Where and how is state changed?
3. **Find state consumers** -- What reads the state?
4. **Map the lifecycle** -- State initialized → updated → consumed → cleaned up

## Using Git History to Understand Evolution and Intent

### Reading Commit History Strategically

Git history reveals design intent that code alone cannot:

**Recent activity patterns:**
```bash
# See which files change most frequently (indicates active development areas)
git log --since="3 months ago" --pretty=format: --name-only | sort | uniq -c | sort -rn | head -20

# See which authors work on which areas (indicates ownership/expertise)
git shortlog -sn --since="6 months ago"

# See the overall commit frequency and project health
git log --since="1 year ago" --oneline | wc -l
```

**Understanding design decisions:**
```bash
# Find when a specific file was introduced (reveals original intent)
git log --diff-filter=A -- path/to/file.ts

# Find the full history of a specific file (reveals evolution)
git log --follow -p -- path/to/file.ts

# Find commits that mention specific terms (reveals reasoning)
git log --grep="refactor" --oneline
git log --grep="migrate" --oneline
```

**Understanding architecture changes:**
```bash
# Find large commits that likely represent architectural changes
git log --shortstat --oneline | head -50

# Find when directories were introduced
git log --diff-filter=A --summary | grep "create mode" | grep -v "test"
```

### What Git History Tells You

- **Files that change together** frequently are likely tightly coupled
- **Files that haven't changed in a long time** are either stable foundations or abandoned code
- **Large commits with many files** often indicate refactoring or architectural changes
- **Commit messages with "fix"** indicate areas that have had bugs
- **Merged branches** tell you how the team works (feature branches, release branches, etc.)

## Leveraging Tests as Living Documentation

### Reading Tests Strategically

Tests are often the most accurate documentation because they must stay in sync with the code:

**Test names as feature inventory:**
```
describe('UserService')
  it('creates a new user with valid data')
  it('rejects duplicate email addresses')
  it('hashes password before storing')
  it('sends welcome email after creation')
  it('assigns default role to new users')
```

This tells you exactly what the UserService does, including edge cases.

**Test fixtures reveal data shapes:**
```javascript
const validUser = {
  email: 'test@example.com',
  name: 'Test User',
  role: 'member',
  organizationId: 'org_123'
};
```

This tells you the expected shape of a user object and its required fields.

**Integration tests reveal component interactions:**
```python
def test_checkout_flow():
    cart = create_cart(user_id=1)
    add_item(cart, product_id=42, quantity=2)
    order = checkout(cart, payment_method='card')
    assert order.status == 'confirmed'
    assert len(order.items) == 1
    assert email_sent_to(user_id=1, template='order_confirmation')
```

This reveals the full checkout flow: cart creation, item addition, payment processing, and email notification.

**What to look for in tests:**

| Test Element | What It Reveals |
|-------------|----------------|
| `describe`/`context` blocks | Module boundaries and feature groupings |
| `it`/`test` descriptions | Expected behaviors and edge cases |
| Setup/teardown (`beforeEach`) | Dependencies and prerequisites |
| Mocks and stubs | External dependencies and boundaries |
| Assertions | Expected outputs and side effects |
| Error test cases | Failure modes and error handling |
| Test data factories | Valid data shapes and relationships |

## Understanding Configuration-Driven Behavior

### Configuration as Hidden Architecture

Many codebases derive significant behavior from configuration rather than code. Missing this layer means missing how the application actually works.

**Environment configuration:**
- `.env` / `.env.example` -- Runtime configuration
- `config/` directory -- Structured configuration
- `appsettings.json` -- .NET configuration
- `application.yml` -- Spring Boot configuration
- Feature flags (LaunchDarkly, Unleash, etc.)

**Framework configuration that defines behavior:**
- Route configuration files
- Dependency injection registrations
- Database migration files (define the data model over time)
- Build configuration that affects runtime behavior (webpack aliases, babel transforms)
- Docker compose files (define service topology)

**What to look for:**
1. What is configured vs hardcoded?
2. What changes between environments?
3. Are there feature flags that change behavior?
4. What secrets or API keys are required?
5. What external URLs or service addresses are configured?

### Configuration Hierarchy

Most applications have layered configuration:

```
Defaults (code)
  ↓ overridden by
Config files (committed)
  ↓ overridden by
Environment-specific config
  ↓ overridden by
Environment variables (runtime)
  ↓ overridden by
Command-line arguments
```

Understanding this hierarchy is essential for understanding what the application will actually do in any given environment.

## Exploration Anti-Patterns to Avoid

**Don't read every file sequentially.** This is the most common mistake. You'll get lost in details before understanding the big picture.

**Don't start with utility code.** Utilities are generic and context-free -- they won't help you understand the application's purpose.

**Don't ignore tests.** Tests are often the best documentation of what code should do and what edge cases exist.

**Don't skip configuration files.** A surprising amount of application behavior is driven by configuration, not code.

**Don't assume the README is current.** READMEs often lag behind the code. Use them as a starting point, then verify against the code.

**Don't try to understand everything at once.** Pick one feature or flow and trace it completely before broadening your scope.

**Don't ignore the git history.** It tells you why things are the way they are, not just what they are.
