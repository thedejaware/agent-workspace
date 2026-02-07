---
name: arch-review
description: >
  Comprehensive architecture and code quality review. Analyzes code structure,
  detects violations of Clean Architecture principles, identifies Domain-Driven
  Design anti-patterns, and spots code smells. Use when reviewing code architecture,
  assessing design quality, checking for architectural boundaries, or when user asks
  to "review architecture", "check code quality", "find code smells", "analyze design",
  "check clean architecture", "review domain model", or "find DDD issues".
allowed-tools: Read, Grep, Glob, Bash(git log *), Bash(git diff *)
---

# Architecture & Code Quality Review

This skill provides comprehensive architectural analysis based on Clean Architecture principles and Domain-Driven Design patterns. It helps identify structural issues, architectural violations, and code smells while providing actionable recommendations for improvement.

## Architecture Principles

This review is based on established architectural principles documented in:
- [Clean Architecture patterns](references/clean-architecture.md) - Uncle Bob's Clean Architecture principles
- [Domain-Driven Design practices](references/domain-driven-design.md) - DDD patterns and tactical design

Review these documents for detailed explanations of the principles checked in this analysis.

## When This Skill Applies

Automatically activates when the user:
- Asks to review code architecture or design quality
- Mentions Clean Architecture or DDD principles
- Requests code smell detection
- Wants to check architectural boundaries
- Asks about code structure or organization
- Requests design pattern validation
- Wants to assess domain model quality

## Process

Follow these steps systematically for architectural review:

### 1. Project Structure Analysis

**Objective:** Understand the overall organization and identify architectural patterns.

**Actions:**
- Examine directory structure and naming conventions
- Identify layer organization (domain, application, infrastructure, UI)
- Check if structure "screams" the domain (tells what the app does, not what it's built with)
- Map framework/technology locations
- Identify cross-cutting concerns

**Key Questions:**
- Does the top-level structure reveal business concerns or technical frameworks?
- Are architectural boundaries clear from folder organization?
- Is there separation between domain logic and infrastructure?
- Are related components grouped by feature/domain vs technical layer?

### 2. Dependency Analysis

**Objective:** Map component dependencies and verify proper dependency direction.

**Actions:**
- Analyze import/require/using statements
- Create dependency graph (at least conceptually)
- Identify dependency direction between layers
- Check for circular dependencies
- Verify the Dependency Rule (dependencies point inward)

**Tools:**
```bash
# Find imports/dependencies
grep -r "import\|require\|using" --include="*.{js,ts,java,cs,py,go}" [path]

# Check for potential circular dependencies
git log --all --format=%H | while read hash; do
  git ls-tree -r --name-only $hash [path]
done | sort | uniq -c
```

**The Dependency Rule:**
> Source code dependencies must point only inward, toward higher-level policies. Nothing in an inner circle can know anything about something in an outer circle.

**Red Flags:**
- Domain entities importing infrastructure classes
- Use cases depending on UI frameworks
- Business logic importing database libraries
- Inner layers depending on outer layers

### 3. Layer Boundary Verification

**Objective:** Ensure architectural layers are properly isolated and boundaries are respected.

**Clean Architecture Layers (innermost to outermost):**
1. **Entities** - Enterprise business rules
2. **Use Cases** - Application business rules
3. **Interface Adapters** - Controllers, presenters, gateways
4. **Frameworks & Drivers** - UI, database, external interfaces

**Verification Checklist:**

**Domain Layer (Entities):**
- [ ] Contains only business rules and domain logic
- [ ] Has NO dependencies on frameworks or infrastructure
- [ ] Uses plain language types (no database annotations, no UI references)
- [ ] Depends on nothing external

**Application Layer (Use Cases):**
- [ ] Orchestrates domain objects to fulfill business scenarios
- [ ] Defines interfaces for data access (repositories) without implementing them
- [ ] Independent of database, UI, and external services
- [ ] Contains input/output port definitions

**Interface Adapters:**
- [ ] Converts data between use cases and external format
- [ ] Implements repository interfaces defined in application layer
- [ ] Contains controllers, presenters, view models
- [ ] Depends inward only

**Infrastructure/Frameworks:**
- [ ] Database implementations are plugins
- [ ] Web frameworks are plugins
- [ ] External services are plugins
- [ ] Can be swapped without changing business rules

**Key Questions:**
- Can you test business logic without a database?
- Can you test business logic without the web framework?
- Can you swap databases without changing use cases?
- Can you deploy business rules independently?

### 4. Domain Model Assessment (DDD)

**Objective:** Evaluate domain model richness and DDD pattern usage.

**Anemic Domain Model Detection:**

**Red Flags:**
```
// BAD: Anemic domain model
class Order {
  getItems() { return this.items; }
  setItems(items) { this.items = items; }
  getTotal() { return this.total; }
  setTotal(total) { this.total = total; }
}

// Service does all the work
class OrderService {
  calculateTotal(order) {
    let total = 0;
    for (item of order.getItems()) {
      total += item.price * item.quantity;
    }
    order.setTotal(total);
  }
}
```

**Good Practice:**
```
// GOOD: Rich domain model
class Order {
  addItem(product, quantity) {
    this.items.push(new OrderItem(product, quantity));
    this.recalculateTotal();
  }

  recalculateTotal() {
    this.total = this.items.reduce((sum, item) =>
      sum + item.calculateSubtotal(), 0);
  }

  canBeShipped() {
    return this.items.length > 0 && this.isPaid;
  }
}
```

**DDD Pattern Checklist:**

**Entities:**
- [ ] Have unique identity that persists over time
- [ ] Contain behavior, not just getters/setters
- [ ] Enforce their own invariants
- [ ] Use value objects for attributes without identity

**Value Objects:**
- [ ] Defined by attributes, not identity
- [ ] Immutable
- [ ] Replace primitive types for domain concepts
- [ ] Examples: Money, DateRange, Address, Email

**Aggregates:**
- [ ] Have clear boundaries around clusters of entities
- [ ] One entity is the aggregate root
- [ ] External objects can only reference the root
- [ ] Invariants enforced within aggregate boundary
- [ ] Modified and persisted as a unit

**Repositories:**
- [ ] Only for aggregate roots (not for every entity)
- [ ] Provide collection-like interface
- [ ] Abstract persistence mechanism
- [ ] Return fully-formed aggregates

**Domain Services:**
- [ ] Used when operation doesn't belong to an entity
- [ ] Stateless
- [ ] Named after ubiquitous language
- [ ] Coordinate between multiple aggregates

**Ubiquitous Language:**
- [ ] Code uses domain terms from business
- [ ] Class/method names match business vocabulary
- [ ] No technical jargon polluting domain layer
- [ ] Consistent terminology across codebase

### 5. Generate Comprehensive Report

**Objective:** Provide actionable findings organized by severity and category.

**Report Structure:**

#### Executive Summary
- Overall architecture health score
- Critical issues count
- Major issues count
- Minor issues count
- Quick wins identified

#### Findings by Category

**A. Clean Architecture Violations**
- Dependency Rule violations
- Framework leakage into domain
- Database coupling in business logic
- UI concerns in use cases
- Missing architectural boundaries

**B. DDD Anti-Patterns**
- Anemic domain models
- Aggregate boundary violations
- Missing value objects
- Repository misuse
- Entity/Value Object confusion

**C. Code Smells**
- God classes
- Long methods
- Deep nesting
- Primitive obsession
- Feature envy
- Inappropriate intimacy

**D. SOLID Violations**
- Single Responsibility violations
- Open/Closed violations
- Liskov Substitution violations
- Interface Segregation violations
- Dependency Inversion violations

#### Severity Classification

**CRITICAL** - Breaks fundamental architectural principles:
- Inner layers depending on outer layers
- Business logic directly using database/frameworks
- Circular dependencies between layers
- No separation between domain and infrastructure

**MAJOR** - Significantly impacts maintainability:
- Anemic domain models
- God classes (>500 lines)
- Missing aggregate boundaries
- Repository for every entity
- Framework annotations in domain entities

**MINOR** - Should be improved but not urgent:
- Primitive obsession (could be value objects)
- Long methods (>50 lines)
- Missing ubiquitous language
- Inconsistent naming

**IMPROVEMENT** - Best practice suggestions:
- Additional abstractions for clarity
- Potential for value objects
- Opportunity for domain events
- Better organization suggestions

#### Prioritized Action Plan

1. **Quick Wins** (high impact, low effort)
2. **Critical Path** (fixes that unblock other improvements)
3. **Foundational Work** (major refactoring needed)
4. **Incremental Improvements** (ongoing quality work)

#### References for Learning

Point to specific sections in:
- `references/clean-architecture.md` - For dependency rule, layer separation
- `references/domain-driven-design.md` - For DDD patterns and examples

## Code Smell Patterns

### God Class
**Detection:**
- Class with >500 lines
- Class with >20 methods
- Class with dependencies on >10 other classes
- Class name contains "Manager", "Helper", "Util" with vague purpose

**Fix:** Split by responsibility, extract collaborators, create focused classes

### Anemic Domain Model
**Detection:**
- Entities with only getters/setters
- All behavior in service classes
- No business logic in domain objects
- Domain objects are just data carriers

**Fix:** Move behavior into domain objects, make entities enforce their own rules

### Primitive Obsession
**Detection:**
- Using strings/ints for domain concepts (email, money, date ranges)
- Validation scattered across codebase
- Same data structure repeated
- No type safety for domain concepts

**Fix:** Create value objects, encapsulate validation, provide domain-specific operations

### Feature Envy
**Detection:**
- Method uses more methods/properties of another class than its own
- Method would be better placed in another class
- Excessive getter calls to foreign objects

**Fix:** Move method to the class it envies, or extract the envied functionality

### Shotgun Surgery
**Detection:**
- Single change requires modifications across many classes
- Related functionality scattered
- Low cohesion across modules

**Fix:** Move related functionality together, increase cohesion, reduce coupling

### Inappropriate Intimacy
**Detection:**
- Classes accessing each other's private parts (via getters)
- Tight coupling between unrelated classes
- Breaking encapsulation

**Fix:** Reduce coupling, use interfaces, respect boundaries

## Example Violations & Fixes

### Example 1: Dependency Rule Violation

**❌ VIOLATION:**
```java
// Domain entity depending on infrastructure
package com.example.domain;

import javax.persistence.*;  // ❌ Domain depends on database framework
import com.example.infrastructure.EmailService;  // ❌ Domain depends on infrastructure

@Entity  // ❌ Framework annotation in domain
public class User {
    @Id
    private Long id;

    private EmailService emailService;  // ❌ Infrastructure dependency

    public void resetPassword() {
        emailService.send(...);  // ❌ Domain calling infrastructure
    }
}
```

**✅ FIX:**
```java
// Domain entity - pure business rules
package com.example.domain;

public class User {
    private UserId id;
    private Email email;

    public PasswordResetRequested resetPassword() {
        // Business rule validation
        if (!this.isActive) {
            throw new UserNotActiveException();
        }
        // Return domain event
        return new PasswordResetRequested(this.id, this.email);
    }
}

// Application layer handles infrastructure
package com.example.application;

public class ResetPasswordUseCase {
    private final UserRepository userRepository;  // Interface defined in domain
    private final EmailGateway emailGateway;      // Interface defined in domain

    public void execute(ResetPasswordCommand command) {
        User user = userRepository.findById(command.userId);
        PasswordResetRequested event = user.resetPassword();
        emailGateway.sendPasswordReset(event.getEmail(), event.getToken());
        userRepository.save(user);
    }
}

// Infrastructure implements interfaces
package com.example.infrastructure;

@Entity
class UserJpaEntity {
    // JPA annotations here
}

class JpaUserRepository implements UserRepository {
    // Converts between domain User and UserJpaEntity
}

class SmtpEmailGateway implements EmailGateway {
    // Email implementation details
}
```

### Example 2: Anemic Domain Model

**❌ VIOLATION:**
```python
# Anemic domain model - just data
class Order:
    def __init__(self):
        self.items = []
        self.status = "pending"
        self.total = 0

# Service does everything
class OrderService:
    def add_item(self, order, product, quantity):
        order.items.append({"product": product, "quantity": quantity})
        self.recalculate_total(order)

    def recalculate_total(self, order):
        order.total = sum(item["product"].price * item["quantity"]
                         for item in order.items)

    def can_checkout(self, order):
        return len(order.items) > 0 and order.total > 0
```

**✅ FIX:**
```python
# Rich domain model
class Money:
    def __init__(self, amount, currency="USD"):
        self.amount = amount
        self.currency = currency

    def add(self, other):
        if self.currency != other.currency:
            raise ValueError("Currency mismatch")
        return Money(self.amount + other.amount, self.currency)

class OrderItem:
    def __init__(self, product, quantity):
        if quantity <= 0:
            raise ValueError("Quantity must be positive")
        self._product = product
        self._quantity = quantity

    def subtotal(self):
        return Money(self._product.price.amount * self._quantity)

class Order:
    def __init__(self):
        self._items = []
        self._status = OrderStatus.PENDING

    def add_item(self, product, quantity):
        # Business rules enforced here
        if self._status != OrderStatus.PENDING:
            raise InvalidOperationError("Cannot modify submitted order")

        self._items.append(OrderItem(product, quantity))

    def total(self):
        return sum((item.subtotal() for item in self._items),
                   Money(0))

    def can_checkout(self):
        return len(self._items) > 0 and self.total().amount > 0

    def checkout(self):
        if not self.can_checkout():
            raise InvalidOperationError("Order cannot be checked out")
        self._status = OrderStatus.SUBMITTED
        return OrderSubmitted(self)  # Domain event
```

### Example 3: Missing Value Objects

**❌ VIOLATION:**
```typescript
// Primitive obsession
class Customer {
    email: string;
    phoneNumber: string;

    constructor(email: string, phone: string) {
        // Validation scattered
        if (!email.includes('@')) {
            throw new Error('Invalid email');
        }
        this.email = email;
        this.phoneNumber = phone;
    }
}

class Order {
    customerEmail: string;  // Duplicated validation logic

    constructor(email: string) {
        if (!email.includes('@')) {  // Same validation repeated
            throw new Error('Invalid email');
        }
        this.customerEmail = email;
    }
}
```

**✅ FIX:**
```typescript
// Value object encapsulates validation
class Email {
    private readonly value: string;

    constructor(email: string) {
        if (!this.isValid(email)) {
            throw new InvalidEmailError(email);
        }
        this.value = email;
    }

    private isValid(email: string): boolean {
        return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
    }

    toString(): string {
        return this.value;
    }

    equals(other: Email): boolean {
        return this.value === other.value;
    }
}

class PhoneNumber {
    private readonly value: string;

    constructor(phone: string) {
        const cleaned = phone.replace(/\D/g, '');
        if (cleaned.length < 10) {
            throw new InvalidPhoneNumberError(phone);
        }
        this.value = cleaned;
    }

    formatted(): string {
        return `(${this.value.slice(0,3)}) ${this.value.slice(3,6)}-${this.value.slice(6)}`;
    }
}

class Customer {
    private email: Email;
    private phoneNumber: PhoneNumber;

    constructor(email: Email, phone: PhoneNumber) {
        this.email = email;  // Already validated
        this.phoneNumber = phone;  // Already validated
    }
}

class Order {
    private customerEmail: Email;

    constructor(email: Email) {
        this.customerEmail = email;  // Type safety + validation
    }
}
```

## Guidelines for Context-Aware Reviews

### When to Be Strict

**Always enforce:**
- The Dependency Rule (inner layers never depend on outer)
- Domain layer independence from frameworks
- Business logic testability without external dependencies
- Aggregate boundaries in DDD contexts

**Zero tolerance for:**
- Circular dependencies
- Business logic in controllers/UI
- Database queries in use cases
- Framework coupling in domain entities

### When to Be Pragmatic

**Consider context for:**
- Small utility applications (< 1000 LOC) - full Clean Architecture may be overkill
- Prototypes and MVPs - note as "architectural debt to address"
- Legacy integration - suggest incremental improvement path
- Team experience - provide learning resources for complex patterns

**Acknowledge trade-offs:**
- Performance vs purity (note when optimization needed)
- Time constraints (mark as technical debt)
- Framework constraints (suggest workarounds)
- Team size and skills (recommend gradual adoption)

### Severity Calibration

**CRITICAL** - Reserved for fundamental violations that will cause serious pain
**MAJOR** - Significant issues that impact maintainability substantially
**MINOR** - Should be fixed but won't cause major problems
**IMPROVEMENT** - Nice-to-haves and optimizations

Don't mark everything as critical. Focus on what truly matters for the project's context.

### Providing Actionable Recommendations

**DO:**
- ✅ Show specific code examples
- ✅ Explain the "why" behind the principle
- ✅ Provide before/after comparisons
- ✅ Reference documentation sections for learning
- ✅ Suggest incremental improvement steps
- ✅ Consider the team's current situation

**DON'T:**
- ❌ Just list violations without context
- ❌ Recommend dogmatic adherence without trade-off analysis
- ❌ Overwhelm with too many changes at once
- ❌ Ignore project constraints and realities
- ❌ Use jargon without explanation

## Usage with Arguments

The skill accepts optional arguments to focus the review:

```
/arch-review [path] [focus-area]
```

**Examples:**
```bash
# Review entire project
/arch-review

# Review specific directory
/arch-review src/domain

# Focus on Clean Architecture principles
/arch-review . focus:clean-architecture

# Focus on DDD patterns
/arch-review src/ focus:ddd

# Focus on dependencies
/arch-review . focus:dependencies

# Focus on code smells
/arch-review src/ focus:smells

# Combine path and focus
/arch-review src/domain focus:ddd
```

**Focus Areas:**
- `focus:clean-architecture` - Emphasize layer separation and dependency rule
- `focus:ddd` - Emphasize domain model, aggregates, value objects
- `focus:dependencies` - Deep analysis of dependency directions and cycles
- `focus:smells` - Emphasize code smell detection
- `focus:solid` - Emphasize SOLID principle violations

## Key Architectural Principles Reference

### The Dependency Rule
> Source code dependencies must point only inward. Nothing in an inner circle can know anything about something in an outer circle.

### The Single Responsibility Principle (SRP)
> A module should have one, and only one, reason to change.

### The Open-Closed Principle (OCP)
> Software entities should be open for extension but closed for modification.

### The Liskov Substitution Principle (LSP)
> Derived classes must be substitutable for their base classes.

### The Interface Segregation Principle (ISP)
> Clients should not be forced to depend on methods they do not use.

### The Dependency Inversion Principle (DIP)
> High-level modules should not depend on low-level modules. Both should depend on abstractions.

### Domain-Driven Design Core Concepts

**Strategic Design:**
- Bounded Contexts - Explicit boundaries around models
- Ubiquitous Language - Shared vocabulary between developers and domain experts
- Context Mapping - Relationships between bounded contexts

**Tactical Design:**
- Entities - Objects with identity
- Value Objects - Objects defined by attributes
- Aggregates - Clusters with consistency boundaries
- Repositories - Collection-like interface for aggregates
- Domain Services - Operations that don't belong to entities
- Domain Events - Something significant that happened

## Output Format

Structure your review following this format:

```markdown
# Architecture Review: [Project Name]

## Executive Summary

**Overall Health:** [Excellent/Good/Fair/Poor]
- Critical Issues: [count]
- Major Issues: [count]
- Minor Issues: [count]
- Improvements Suggested: [count]

**Quick Assessment:**
[2-3 sentence summary of overall architecture state]

## Project Structure Analysis

[Analysis of directory organization and architectural patterns]

## Critical Findings

### [Issue Category]

**Severity:** CRITICAL
**Location:** `path/to/file.ext:123`
**Issue:** [Description]
**Impact:** [Why this matters]
**Recommendation:** [How to fix]

[Additional critical findings...]

## Major Findings

[Similar format for major issues...]

## Minor Findings & Improvements

[Similar format for minor issues...]

## Dependency Analysis

[Findings about dependency directions, cycles, coupling]

## Domain Model Assessment

[DDD-specific findings if applicable]

## Recommended Action Plan

### Phase 1: Critical Fixes (Do First)
1. [Action item with file references]
2. [Action item with file references]

### Phase 2: Major Improvements (Next)
1. [Action item]
2. [Action item]

### Phase 3: Incremental Quality (Ongoing)
1. [Action item]
2. [Action item]

## Learning Resources

For detailed understanding of the principles referenced:
- See `references/clean-architecture.md` sections: [specific chapters]
- See `references/domain-driven-design.md` sections: [specific topics]

## Positive Observations

[Note what's done well - balanced feedback]
```

## Notes

- This skill works across any programming language (principles are universal)
- Adjust strictness based on project context (size, maturity, domain complexity)
- Balance critique with recognition of good practices
- Provide learning opportunities through documentation references
- Focus on actionable improvements, not just problems
- Consider team experience when recommending patterns
