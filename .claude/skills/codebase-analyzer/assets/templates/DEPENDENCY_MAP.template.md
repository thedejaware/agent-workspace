# Dependency Map: [Project Name]

## Internal Module Dependencies

### Module Overview

```
[ASCII diagram showing module relationships]

┌──────────┐     ┌──────────┐     ┌──────────┐
│  Module A │────▶│ Module B │────▶│ Module C │
└──────────┘     └──────────┘     └──────────┘
      │                                 ▲
      └─────────────────────────────────┘
```

### Module Dependency Table

| Module | Depends On | Depended On By | Role |
|--------|-----------|----------------|------|
| `[module/path]` | [List of modules it imports from] | [List of modules that import from it] | [Core / Support / Peripheral] |
| `[module/path]` | [List of modules it imports from] | [List of modules that import from it] | [Core / Support / Peripheral] |
| `[module/path]` | [List of modules it imports from] | [List of modules that import from it] | [Core / Support / Peripheral] |

### Dependency Layers

```
Layer 1 (Entry Points)
  └─▶ [controllers / routes / commands / pages]

Layer 2 (Business Logic)
  └─▶ [services / use cases / handlers]

Layer 3 (Data Access)
  └─▶ [repositories / data stores / API clients]

Layer 4 (Domain)
  └─▶ [models / entities / types / interfaces]

Layer 5 (Shared Utilities)
  └─▶ [utils / helpers / constants / config]
```

**Dependency rules observed:**
- [e.g., "Layer N only imports from layers N+1 and below"]
- [e.g., "Models have no dependencies on other internal modules"]
- [e.g., "Services can depend on other services and repositories"]

### Most-Imported Modules (Central Abstractions)

These modules are imported by the most other modules, making them the structural backbone:

| Rank | Module | Imported By (count) | What It Provides |
|------|--------|-------------------|-----------------|
| 1 | `[path]` | [N] modules | [Description] |
| 2 | `[path]` | [N] modules | [Description] |
| 3 | `[path]` | [N] modules | [Description] |

### Circular Dependencies

[List any circular dependencies found, or state "None detected"]

- `[module A]` <-> `[module B]` via [explanation of the cycle]

## External Dependencies

### Core Dependencies

These are fundamental to the project and would require significant effort to replace:

| Package | Version | Purpose | Category |
|---------|---------|---------|----------|
| `[package-name]` | [version] | [What it's used for] | Framework |
| `[package-name]` | [version] | [What it's used for] | Data layer |
| `[package-name]` | [version] | [What it's used for] | Communication |

### Supporting Dependencies

These provide useful functionality but could be replaced with alternatives:

| Package | Version | Purpose | Alternative Options |
|---------|---------|---------|-------------------|
| `[package-name]` | [version] | [What it's used for] | [Other libraries that could replace it] |
| `[package-name]` | [version] | [What it's used for] | [Other libraries that could replace it] |

### Dev Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| `[package-name]` | [version] | [Testing / Linting / Building / etc.] |
| `[package-name]` | [version] | [Testing / Linting / Building / etc.] |

## External System Integrations

### Integration Map

```
                    ┌─────────────────────┐
                    │   [Project Name]    │
                    └─────────┬───────────┘
                              │
         ┌────────────────────┼────────────────────┐
         │                    │                    │
         ▼                    ▼                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│  Database   │     │ External API│     │   Cache     │
│  [Type]     │     │  [Name]     │     │  [Type]     │
└─────────────┘     └─────────────┘     └─────────────┘
```

### Integration Details

#### [Database / Service Name]

- **Type:** [SQL database / NoSQL / Message queue / API / etc.]
- **Technology:** [PostgreSQL / Redis / RabbitMQ / etc.]
- **Connection configured in:** `[path/to/config]`
- **Client/driver used:** `[package name]`
- **Used by modules:** `[list of internal modules that access this]`
- **Purpose:** [What data is stored/retrieved, what operations are performed]

#### [Database / Service Name]

- **Type:** [SQL database / NoSQL / Message queue / API / etc.]
- **Technology:** [PostgreSQL / Redis / RabbitMQ / etc.]
- **Connection configured in:** `[path/to/config]`
- **Client/driver used:** `[package name]`
- **Used by modules:** `[list of internal modules that access this]`
- **Purpose:** [What data is stored/retrieved, what operations are performed]

## Dependency Health

### Observations

- **Outdated packages:** [List any significantly outdated dependencies]
- **Deprecated packages:** [List any deprecated dependencies]
- **Security advisories:** [Note any known vulnerabilities]
- **Unused dependencies:** [List any dependencies that appear unused]
- **Missing from manifest:** [Any imports that don't match declared dependencies]

### Dependency Update Risk

| Package | Current | Latest | Breaking Changes Expected | Risk Level |
|---------|---------|--------|--------------------------|------------|
| `[package]` | [current] | [latest] | [Yes/No - brief description] | [Low/Medium/High] |
