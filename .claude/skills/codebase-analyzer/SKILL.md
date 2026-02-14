---
name: codebase-analyzer
description: This skill should be used when exploring, understanding, or analyzing an unfamiliar codebase. Use this skill when users ask you to understand how a project works, map its architecture, trace data flows, identify patterns and conventions, or build a comprehensive mental model of a codebase. The skill provides a systematic methodology for code exploration, technology-specific checklists, and structured output formats for presenting analysis findings.
---

# Codebase Analyzer

## Overview

This skill enables systematic exploration and deep understanding of unfamiliar codebases. Rather than producing documentation output, it focuses on building a comprehensive mental model of how a project works -- its architecture, patterns, data flows, conventions, and key abstractions. Use this skill when you need to quickly understand a new codebase or help a user make sense of a project they're working with.

## Systematic Exploration Methodology

Follow these phases in order. Each phase builds on the previous one to construct a layered understanding of the codebase.

### Phase 1: Project Identity

**Goal:** Determine what this project is, what it's built with, and how it's organized at the highest level.

**Steps:**

1. **Read project manifests** -- Look for configuration files that reveal the tech stack:
   - `package.json` / `package-lock.json` / `yarn.lock` / `pnpm-lock.yaml` (Node.js/JavaScript)
   - `pyproject.toml` / `setup.py` / `setup.cfg` / `requirements.txt` / `Pipfile` (Python)
   - `Cargo.toml` / `Cargo.lock` (Rust)
   - `go.mod` / `go.sum` (Go)
   - `pom.xml` / `build.gradle` / `build.gradle.kts` (Java/Kotlin)
   - `*.csproj` / `*.sln` / `Directory.Build.props` (C#/.NET)
   - `Gemfile` / `Gemfile.lock` (Ruby)
   - `Package.swift` / `*.xcodeproj` / `*.xcworkspace` (Swift/iOS)
   - `pubspec.yaml` (Dart/Flutter)
   - `composer.json` (PHP)
   - `mix.exs` (Elixir)
   - `CMakeLists.txt` / `Makefile` (C/C++)
   - `docker-compose.yml` / `Dockerfile` (containerized apps)

2. **Read the README** -- Extract project purpose, setup instructions, and high-level description

3. **Scan the top-level directory structure** -- Understand how the project is organized:
   - What directories exist at the root?
   - Are there `src/`, `lib/`, `app/`, `cmd/`, `internal/`, `pkg/` directories?
   - Is there a `tests/`, `test/`, `spec/`, `__tests__/` directory?
   - Are there config directories (`config/`, `.github/`, `scripts/`)?

4. **Check for monorepo structure** -- Look for workspace configurations:
   - `workspaces` in `package.json`
   - `pnpm-workspace.yaml`
   - `lerna.json`
   - Multiple `Cargo.toml` with a root workspace
   - Multiple `go.mod` files

5. **Identify the project type** -- Classify what you're dealing with:
   - Web application (frontend, backend, fullstack)
   - API service (REST, GraphQL, gRPC)
   - CLI tool
   - Library/SDK
   - Mobile application
   - Desktop application
   - Infrastructure/DevOps tooling
   - Data pipeline
   - Monorepo with multiple packages

**Output of this phase:** A 2-3 sentence summary stating what the project does, what it's built with, and how it's broadly organized.

### Phase 2: Entry Points

**Goal:** Find where execution begins and how the application bootstraps.

**Steps:**

1. **Locate the main entry point(s):**
   - Check `main`, `bin`, `exports` fields in `package.json`
   - Look for `main.ts`, `main.go`, `main.rs`, `Program.cs`, `App.java`, `__main__.py`
   - Check for `index.ts`, `index.js`, `app.ts`, `app.py`, `server.ts`
   - Look for framework-specific entry points (e.g., `pages/` in Next.js, `src/App.tsx` in React)

2. **Trace the initialization sequence:**
   - What happens when the app starts?
   - What configuration is loaded first?
   - What services/connections are initialized?
   - What middleware or interceptors are set up?

3. **Find routing and request handling:**
   - For web apps: route definitions, controller registrations
   - For CLIs: command/subcommand definitions
   - For libraries: public API surface (exported modules)

4. **Identify startup dependencies:**
   - Database connections
   - External service clients
   - Configuration providers
   - Authentication/authorization setup

**Output of this phase:** A list of key entry points with brief descriptions of what each one initializes.

### Phase 3: Dependency Mapping

**Goal:** Understand how internal modules relate to each other and what external systems the project depends on.

**Steps:**

1. **Map internal module dependencies:**
   - Which modules import from which other modules?
   - Are there clear layers (e.g., controllers -> services -> repositories)?
   - Are there circular dependencies?
   - What are the most-imported modules (central abstractions)?

2. **Categorize external dependencies:**
   - **Core framework** -- The main framework the project is built on
   - **Data layer** -- Database drivers, ORMs, cache clients
   - **Communication** -- HTTP clients, message queues, WebSocket libraries
   - **Authentication** -- Auth libraries, JWT, OAuth
   - **Utilities** -- Logging, validation, date handling
   - **Dev dependencies** -- Testing, linting, build tools

3. **Identify core vs peripheral dependencies:**
   - Core: Would require significant refactoring to replace
   - Peripheral: Could be swapped with minimal changes

4. **Map external system integrations:**
   - Databases (type, how accessed)
   - APIs consumed (what external services are called)
   - Message queues / event systems
   - File storage / cloud services
   - Caching layers

**Output of this phase:** Use the `assets/templates/DEPENDENCY_MAP.template.md` template to present findings.

### Phase 4: Architecture Recognition

**Goal:** Identify the architectural patterns and structural decisions that shape the codebase.

**Steps:**

1. **Identify the high-level architecture:**
   - Monolith vs microservices vs modular monolith
   - Client-server vs peer-to-peer
   - Event-driven vs request-response
   - Serverless vs traditional deployment

2. **Identify structural patterns from directory organization:**
   - **By layer** (`controllers/`, `services/`, `models/`) -- Layered architecture
   - **By feature** (`users/`, `orders/`, `payments/`) -- Domain-driven / feature-based
   - **By type** (`components/`, `hooks/`, `utils/`) -- Type-based organization (common in frontend)
   - **Mixed** -- Hybrid approaches

3. **Identify code-level patterns:**
   - Dependency injection (constructor injection, DI containers)
   - Repository pattern (data access abstraction)
   - Service layer (business logic isolation)
   - Middleware/pipeline (request processing chains)
   - Observer/event emitter (decoupled communication)
   - Factory pattern (object creation)
   - Strategy pattern (interchangeable algorithms)

4. **Identify state management approach:**
   - Server-side: sessions, database, cache
   - Client-side: Redux, Context, Zustand, signals, stores
   - Distributed: event sourcing, CQRS

**Output of this phase:** A description of the architectural style and the key patterns employed, with references to where each pattern is implemented.

For detailed pattern recognition guidance, refer to `references/pattern_recognition.md`.

### Phase 5: Data Flow Tracing

**Goal:** Understand how data moves through the system for the primary use cases.

**Steps:**

1. **Identify the primary use case** -- What is the most important thing this application does? Trace that first.

2. **Trace the request lifecycle:**
   - Where does the request enter the system?
   - What validation/transformation happens?
   - What business logic is applied?
   - Where is data persisted or retrieved?
   - How is the response constructed and returned?

3. **Map the data model:**
   - What are the core entities/types?
   - How do they relate to each other?
   - Where are they defined? (models, schemas, types, interfaces)
   - How are they validated?

4. **Trace error paths:**
   - How are errors created and propagated?
   - Is there centralized error handling?
   - What happens when external services fail?
   - How are errors communicated to users?

5. **Identify side effects:**
   - What triggers emails, notifications, webhooks?
   - What gets logged and where?
   - What analytics/metrics are collected?
   - What background jobs are enqueued?

**Output of this phase:** An annotated walkthrough of data flow for 1-2 primary use cases, with file paths at each step.

### Phase 6: Convention Discovery

**Goal:** Identify the coding conventions and patterns that a developer should follow when contributing to this codebase.

**Steps:**

1. **Naming conventions:**
   - File naming (kebab-case, camelCase, PascalCase, snake_case)
   - Variable/function naming style
   - Class/type naming style
   - Database table/column naming
   - API endpoint naming

2. **Code organization patterns:**
   - How are files structured internally? (exports at top vs bottom, ordering of methods)
   - How are tests organized relative to source code?
   - Are there barrel files (`index.ts` re-exports)?
   - How is shared code handled?

3. **Error handling approach:**
   - Exceptions vs result types vs error codes
   - Where are errors caught and handled?
   - Custom error classes or standard errors?
   - User-facing vs internal error messages

4. **Testing strategy:**
   - Test framework used
   - Test organization (colocated vs separate directory)
   - Test naming conventions
   - Mocking/stubbing approach
   - Integration vs unit test ratio

5. **Configuration approach:**
   - Environment variables vs config files vs both
   - How are secrets managed?
   - Environment-specific configuration

6. **Linting and formatting:**
   - ESLint, Prettier, Biome, rustfmt, gofmt, etc.
   - Custom rules or standard configs
   - Pre-commit hooks

**Output of this phase:** A conventions summary that would help a new contributor write code that fits the codebase style.

## Technology-Specific Exploration Checklists

When you identify the project's tech stack in Phase 1, use the appropriate checklist below to guide deeper exploration.

### Node.js / TypeScript

1. Check `package.json`: scripts, dependencies, engines, type (module vs commonjs)
2. Check `tsconfig.json` / `jsconfig.json`: paths, strict mode, target
3. Look for framework setup: Express app, Nest modules, Fastify plugins, Next.js config
4. Check for `.env` / `.env.example` files
5. Look for ORM setup: Prisma schema, TypeORM entities, Drizzle config, Sequelize models
6. Check middleware chain order (especially auth, error handling, logging)
7. Look for `scripts/` directory for build/deploy automation
8. Check for monorepo tools: turborepo, nx, lerna workspaces

### Python

1. Check `pyproject.toml` / `setup.py`: dependencies, entry points, build system
2. Look for framework setup: Django `settings.py`, Flask `app.py`, FastAPI `main.py`
3. Check for `requirements.txt` vs `poetry.lock` vs `Pipfile.lock`
4. Look for `alembic/` (database migrations), `models/`, `schemas/`
5. Check for `conftest.py` files (pytest fixtures and configuration)
6. Look for `manage.py` (Django), `celery.py` (task queues)
7. Check for type hints usage and `mypy.ini` / `py.typed`
8. Look for `__init__.py` patterns (what's exported from packages)

### Rust

1. Check `Cargo.toml`: dependencies, features, workspace configuration
2. Look for `lib.rs` vs `main.rs` (library vs binary)
3. Check `mod.rs` or module declarations for code organization
4. Look for trait definitions (core abstractions)
5. Check error handling: custom error types, `thiserror`, `anyhow`
6. Look for `build.rs` (build-time code generation)
7. Check for `unsafe` blocks and their justifications
8. Look for `tests/` directory and `#[cfg(test)]` modules

### Go

1. Check `go.mod`: module path, Go version, dependencies
2. Look for `cmd/` directory (CLI entry points)
3. Check `internal/` vs `pkg/` organization
4. Look for interface definitions (contracts between packages)
5. Check error handling patterns (custom error types, wrapping)
6. Look for `*_test.go` files for test patterns
7. Check for `Makefile` or `mage` build automation
8. Look for code generation markers (`//go:generate`)

### Java / Kotlin

1. Check `pom.xml` or `build.gradle`: dependencies, plugins, modules
2. Look for Spring Boot: `@SpringBootApplication`, `application.yml`/`application.properties`
3. Check package structure: controllers, services, repositories, entities
4. Look for dependency injection configuration
5. Check for `resources/` directory (config, templates, static files)
6. Look for migration tools: Flyway (`db/migration/`), Liquibase
7. Check for API documentation: Swagger/OpenAPI annotations
8. Look for `test/` directory structure mirroring `main/`

### .NET / C#

1. Check `*.csproj` / `*.sln` files: target framework, package references, project structure
2. Look for `Program.cs`: application startup and service registration
3. Check for `Startup.cs` or minimal API configuration (older vs newer patterns)
4. Look for `appsettings.json` / `appsettings.{Environment}.json`
5. Check directory structure: `Controllers/`, `Services/`, `Models/`, `Data/`
6. Look for Entity Framework: `DbContext`, migrations in `Migrations/`
7. Check for dependency injection registrations (`builder.Services.Add*`)
8. Look for middleware pipeline configuration (`app.Use*`)

### Ruby

1. Check `Gemfile`: dependencies and version constraints
2. Look for Rails structure: `app/`, `config/routes.rb`, `db/schema.rb`
3. Check `config/` directory for environment configuration
4. Look for `lib/` directory for shared code
5. Check migration files in `db/migrate/`
6. Look for `spec/` (RSpec) or `test/` (Minitest) directories
7. Check for background jobs: Sidekiq, Resque, DelayedJob
8. Look for `config/initializers/` for third-party setup

### Mobile (Swift / Kotlin)

1. Check project file: `*.xcodeproj` / `Package.swift` / `build.gradle`
2. Look for app entry point: `@main`, `AppDelegate`, `Application` class
3. Check for dependency managers: SPM, CocoaPods, Gradle
4. Look for architecture pattern: MVVM, MVC, VIPER, Clean Architecture
5. Check for networking layer setup
6. Look for persistence: Core Data, Room, Realm, SQLite
7. Check for dependency injection: Hilt, Dagger, Swinject
8. Look for navigation/routing setup

## Code Reading Strategies

Choose the strategy that best fits your goal:

### Top-Down Strategy

**When to use:** You need a broad understanding of the entire system.

1. Start from the main entry point
2. Read the initialization/bootstrap code
3. Follow the routing or command registration
4. Read handlers/controllers at a high level (what endpoints exist, what they do)
5. Dive into services only as needed for understanding
6. Read models/types to understand the domain

**Advantage:** Gives you the full picture quickly.
**Risk:** Can get lost in abstraction layers without understanding details.

### Bottom-Up Strategy

**When to use:** You need to understand the domain model and building blocks first.

1. Start with data models, types, and interfaces
2. Read utility functions and shared helpers
3. Read service/business logic that operates on the models
4. Read controllers/handlers that wire services together
5. Read configuration and initialization last

**Advantage:** Deep understanding of the building blocks.
**Risk:** Can take longer to see how everything connects.

### Feature-Focused Strategy

**When to use:** You need to understand one specific feature or capability.

1. Identify the user-facing entry point for the feature (UI component, API endpoint, CLI command)
2. Trace the request through the system layer by layer
3. Note every file touched along the way
4. Document the complete path from input to output
5. Note which parts are feature-specific vs shared

**Advantage:** Concrete, practical understanding of one slice of the system.
**Risk:** May miss cross-cutting concerns that affect the feature.

### Test-Driven Strategy

**When to use:** The codebase has good test coverage and you want to understand expected behavior.

1. Read test files to understand expected inputs and outputs
2. Use test names as a feature inventory
3. Read test fixtures/factories to understand data shapes
4. Follow tested code paths to understand implementation
5. Look for integration tests to understand component interaction

**Advantage:** Tests document intended behavior and edge cases.
**Risk:** Tests may not cover all paths or may be outdated.

## Key Questions Checklist

A complete codebase analysis should answer these questions. Use this checklist to verify your analysis is thorough.

### Purpose and Context
- [ ] What does this project do? (one-sentence answer)
- [ ] Who are the intended users?
- [ ] What problem does it solve?
- [ ] Is it a library, application, service, or tool?

### Architecture and Structure
- [ ] What is the high-level architecture? (monolith, microservices, etc.)
- [ ] What are the key directories and what do they contain?
- [ ] How is the code organized? (by layer, by feature, hybrid)
- [ ] What are the clear module boundaries?

### Core Abstractions
- [ ] What are the main types/classes/interfaces?
- [ ] What is the domain model?
- [ ] What are the most important functions/methods?
- [ ] What abstractions are used across the codebase?

### Data Flow
- [ ] How does a typical request flow through the system?
- [ ] Where does data enter the system?
- [ ] How is data validated and transformed?
- [ ] Where is data stored and how is it retrieved?
- [ ] How are responses constructed?

### External Dependencies
- [ ] What databases does it use?
- [ ] What external APIs does it call?
- [ ] What message queues or event systems are used?
- [ ] What third-party services are integrated?

### Testing
- [ ] What test framework is used?
- [ ] How are tests organized?
- [ ] What is the test coverage approach? (unit, integration, e2e)
- [ ] Are there test fixtures or factories?

### Build and Deploy
- [ ] What is the build system?
- [ ] Are there CI/CD pipelines?
- [ ] How is the project deployed?
- [ ] What environments exist?

### Conventions
- [ ] What naming conventions are used?
- [ ] What error handling pattern is followed?
- [ ] What logging approach is used?
- [ ] What code style/linting tools are configured?

## Analysis Output Format

Use the `assets/templates/ANALYSIS_REPORT.template.md` template for structured output. At minimum, every analysis should include:

1. **Project overview** -- 1-2 sentence summary of what the project does
2. **Tech stack** -- Languages, frameworks, key libraries
3. **Architecture summary** -- High-level architectural style and patterns
4. **Key file map** -- The 10-20 most important files and what they do
5. **Core abstractions** -- Main types, interfaces, or classes that define the domain
6. **Primary data flow** -- How data moves through the system for the main use case
7. **External integrations** -- Databases, APIs, services the project depends on
8. **Conventions** -- Naming, error handling, testing patterns to follow

## Using Templates

### Available Templates

- **ANALYSIS_REPORT.template.md** -- Comprehensive template for presenting full analysis findings, organized from overview through architecture, data flow, and conventions
- **DEPENDENCY_MAP.template.md** -- Focused template for mapping internal module relationships and external dependency inventory

### Using Templates

1. **Read the appropriate template** from `assets/templates/`
2. **Customize for the specific codebase** -- Fill in sections relevant to the project
3. **Remove irrelevant sections** -- Not every project needs every section
4. **Add project-specific sections** -- Extend the template if the codebase has unique aspects
5. **Include file paths** -- Always reference specific files using `path/to/file.ext` format

## Best Practices Reference

For detailed exploration techniques and pattern recognition guidance, refer to:

- `references/exploration_methodology.md` -- Deep guide on systematic code exploration, execution tracing, understanding codebase evolution through git history, and identifying the structural skeleton
- `references/pattern_recognition.md` -- Guide on recognizing architectural patterns, design patterns, framework-specific patterns, and anti-patterns from code structure

Load these references when:
- Analyzing a large or complex codebase with many modules
- Encountering unfamiliar architectural patterns
- Trying to understand the evolution and design intent behind code decisions
- Needing framework-specific pattern recognition guidance

## Quick Reference

**Command to analyze a codebase:**
"Analyze this codebase and help me understand how it works"

**Command to trace a feature:**
"Trace the authentication flow through this codebase from start to finish"

**Command to map dependencies:**
"Map the internal dependencies and external integrations in this project"

**Command to identify patterns:**
"What architectural and design patterns does this codebase use?"

**Command to discover conventions:**
"What coding conventions and patterns should I follow when contributing to this project?"
