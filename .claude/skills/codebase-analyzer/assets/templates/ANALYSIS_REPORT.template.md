# Codebase Analysis: [Project Name]

## Project Overview

**What it does:** [1-2 sentence plain-English summary of the project's purpose and value]

**Project type:** [Web app / API service / CLI tool / Library / Mobile app / etc.]

**Repository:** [URL or path]

## Tech Stack

| Layer | Technology | Version | Notes |
|-------|-----------|---------|-------|
| Language | [Language] | [Version] | [Key details] |
| Framework | [Framework] | [Version] | [Key details] |
| Database | [Database] | [Version] | [How accessed - ORM, driver, etc.] |
| Testing | [Framework] | [Version] | [Unit, integration, e2e] |
| Build | [Tool] | [Version] | [Key details] |
| Deployment | [Platform] | - | [Key details] |

## Architecture Summary

### Architectural Style

[Describe the high-level architecture: monolith, microservices, modular monolith, serverless, etc.]

[Describe the organizational approach: layered, feature-based, domain-driven, etc.]

### System Diagram

```
[ASCII diagram showing high-level components and their relationships]

┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│ Component A │─────▶│ Component B │─────▶│ Component C │
└─────────────┘      └─────────────┘      └─────────────┘
```

### Directory Structure

```
project-root/
├── [dir]/                  # [Purpose]
│   ├── [subdir]/          # [Purpose]
│   └── [subdir]/          # [Purpose]
├── [dir]/                  # [Purpose]
├── [config-file]           # [Purpose]
└── [config-file]           # [Purpose]
```

## Key File Map

The most important files in this codebase and what they do:

| File | Purpose | Why It Matters |
|------|---------|---------------|
| `[path/to/file]` | [What this file does] | [Why a developer should know about it] |
| `[path/to/file]` | [What this file does] | [Why a developer should know about it] |
| `[path/to/file]` | [What this file does] | [Why a developer should know about it] |
| `[path/to/file]` | [What this file does] | [Why a developer should know about it] |
| `[path/to/file]` | [What this file does] | [Why a developer should know about it] |

## Core Abstractions

### Domain Model

[Describe the main entities/types and how they relate to each other]

```
[Entity A] ──1:N──▶ [Entity B]
    │                    │
    │                    ▼
    └──────1:1──▶ [Entity C]
```

### Key Types and Interfaces

**[Type/Interface Name]** -- `[path/to/definition]`
[What it represents and why it's important]

**[Type/Interface Name]** -- `[path/to/definition]`
[What it represents and why it's important]

**[Type/Interface Name]** -- `[path/to/definition]`
[What it represents and why it's important]

### Key Functions and Methods

**[Function Name]** -- `[path/to/file:line]`
[What it does and when it's called]

**[Function Name]** -- `[path/to/file:line]`
[What it does and when it's called]

## Data Flow

### Primary Use Case: [Name of the main use case]

```
[Step-by-step flow with file references]

User Action
    │
    ▼
[1] path/to/entry.ext         ── [What happens here]
    │
    ▼
[2] path/to/validation.ext    ── [What happens here]
    │
    ▼
[3] path/to/service.ext       ── [What happens here]
    │
    ▼
[4] path/to/repository.ext    ── [What happens here]
    │
    ▼
[5] Database / External API    ── [What happens here]
    │
    ▼
Response returned to user
```

**Detailed walkthrough:**

1. **[Step name]** (`path/to/file.ext`)
   - [What happens in this step]
   - [Key functions called]

2. **[Step name]** (`path/to/file.ext`)
   - [What happens in this step]
   - [Key functions called]

3. **[Step name]** (`path/to/file.ext`)
   - [What happens in this step]
   - [Key functions called]

### Error Handling Flow

[How errors propagate through the system]

- **Validation errors:** [How handled, where caught]
- **Business logic errors:** [How handled, where caught]
- **External service failures:** [How handled, fallback behavior]
- **Unexpected errors:** [Global error handler location and behavior]

## External Integrations

### Databases

| Database | Type | Access Method | Schema Location |
|----------|------|--------------|-----------------|
| [Name] | [SQL/NoSQL/etc.] | [ORM/Driver/etc.] | `[path/to/schema]` |

### External APIs

| Service | Purpose | Client Location | Auth Method |
|---------|---------|----------------|-------------|
| [Service] | [What it's used for] | `[path/to/client]` | [API key/OAuth/etc.] |

### Other Integrations

- **Message queue:** [Technology, where configured, what events are published/consumed]
- **Cache:** [Technology, where configured, what's cached]
- **File storage:** [Technology, where configured, what's stored]
- **Email/notifications:** [Technology, where configured, what triggers them]

## Build and Deploy

### Build Process

```bash
# Development
[dev-command]

# Production build
[build-command]

# Run tests
[test-command]
```

### CI/CD Pipeline

[Describe the CI/CD setup: what runs on PR, what runs on merge, deployment process]

### Environments

| Environment | Purpose | Configuration |
|------------|---------|---------------|
| Development | [Purpose] | `[config file or env vars]` |
| Staging | [Purpose] | `[config file or env vars]` |
| Production | [Purpose] | `[config file or env vars]` |

## Conventions and Patterns

### Naming Conventions

| Element | Convention | Example |
|---------|-----------|---------|
| Files | [kebab-case/camelCase/etc.] | `[example]` |
| Functions | [camelCase/snake_case/etc.] | `[example]` |
| Classes/Types | [PascalCase/etc.] | `[example]` |
| Constants | [UPPER_SNAKE/etc.] | `[example]` |
| Database tables | [snake_case/etc.] | `[example]` |

### Design Patterns Used

- **[Pattern name]:** [Where and how it's used]
- **[Pattern name]:** [Where and how it's used]
- **[Pattern name]:** [Where and how it's used]

### Testing Approach

- **Test framework:** [Name]
- **Test organization:** [Colocated / separate directory / both]
- **Test types:** [Unit / integration / e2e -- which are present]
- **Mocking strategy:** [How external dependencies are mocked]
- **Test data:** [Fixtures, factories, inline data]

### Error Handling Pattern

[Describe the standard error handling approach used throughout the codebase]

### Logging Pattern

[Describe the logging approach: library used, log levels, structured logging, where logs go]

## Potential Areas of Concern

[Flag any notable issues, risks, or areas that deserve attention]

- **[Concern]:** [Description and where it's observed]
- **[Concern]:** [Description and where it's observed]
- **[Concern]:** [Description and where it's observed]

## Navigation Guide for New Developers

**To understand the domain model, start with:**
- `[path/to/models]`

**To understand the API surface, start with:**
- `[path/to/routes]`

**To understand business logic, start with:**
- `[path/to/services]`

**To understand how things are tested, start with:**
- `[path/to/tests]`

**To understand build and deployment, start with:**
- `[path/to/config]`
