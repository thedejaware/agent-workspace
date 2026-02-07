# Clean Architecture: Comprehensive Summary

**Based on "Clean Architecture: A Craftsman's Guide to Software Structure and Design" by Robert C. Martin (Uncle Bob), 2018**

---

## Part I: Introduction — Why Architecture Matters

### Chapter 1: What Is Design and Architecture?

There is **no difference** between design and architecture. Low-level details and high-level structure are all part of the same whole — a continuous fabric of decisions from the highest to the lowest levels.

**The Goal of Software Architecture:**

> *The goal of software architecture is to minimize the human resources required to build and maintain the required system.*

The measure of design quality is the **effort required to meet the needs of the customer**. If effort stays low throughout the system's lifetime, the design is good. If effort grows with each release, the design is bad.

**The Signature of a Mess:** When systems are thrown together in a hurry, productivity declines asymptotically toward zero. Cost per line of code skyrockets. The bigger lie is that making messes makes you go fast in the short term — **making messes is always slower than staying clean**, no matter the time scale.

> *The only way to go fast, is to go well.*

### Chapter 2: A Tale of Two Values

Every software system provides two values: **behavior** (what it does) and **architecture** (how easy it is to change).

- **Behavior** is urgent but not always important.
- **Architecture** is important but never urgent.

Using Eisenhower's Matrix, architecture occupies the top two priority positions. The mistake is elevating urgent-but-unimportant behavior over important-but-not-urgent architecture.

**It is the responsibility of the software development team to assert the importance of architecture over the urgency of features.** If architecture comes last, the system becomes ever more costly to develop.

---

## Part II: Programming Paradigms

### Three Paradigms

Each paradigm **removes** capabilities from the programmer — they tell us what *not* to do:

1. **Structured Programming** (Dijkstra, 1968): Imposes discipline on **direct transfer of control**. Removes `goto`. Enables functional decomposition and testability through falsifiable units.

2. **Object-Oriented Programming** (Dahl & Nygaard, 1966): Imposes discipline on **indirect transfer of control**. The power of OO is **polymorphism** — giving architects absolute control over the direction of all source code dependencies. This enables **dependency inversion**: the database and UI depend on business rules, not the other way around. This gives us **independent deployability** and **independent developability**.

3. **Functional Programming** (Church, 1936): Imposes discipline on **variable assignment**. Variables do not vary. Immutability eliminates race conditions, deadlock conditions, and concurrent update problems. Architects should push as much processing as possible into immutable components.

**Architectural relevance:**
- We use **polymorphism** to cross architectural boundaries
- We use **functional programming** to impose discipline on data access
- We use **structured programming** as the algorithmic foundation of our modules

---

## Part III: SOLID Design Principles

The SOLID principles tell us how to arrange functions and data structures into classes (coupled groupings), and how those classes should be interconnected. They create mid-level software structures that **tolerate change**, are **easy to understand**, and are **the basis of reusable components**.

### SRP: The Single Responsibility Principle

> *A module should be responsible to one, and only one, actor.*

**NOT** "a module should do one thing" (that's a function-level concern). SRP means that code serving different actors (stakeholders) should be separated. Violations lead to:

- **Accidental duplication**: Shared code that different actors change for different reasons breaks unexpectedly.
- **Merge conflicts**: Multiple teams editing the same file for different reasons.

**Solutions:** Separate classes per actor (e.g., `PayCalculator`, `HourReporter`, `EmployeeSaver`), optionally unified behind a Facade.

At the component level, SRP becomes the **Common Closure Principle**. At the architectural level, it becomes the **Axis of Change** that creates Architectural Boundaries.

### OCP: The Open-Closed Principle

> *A software artifact should be open for extension but closed for modification.*

Architects separate functionality based on how, why, and when it changes, then organize it into a **hierarchy of components**. Higher-level components are **protected** from changes in lower-level components. The **Interactor** (containing business rules) is the most protected; Views are the least protected.

All component relationships should be **unidirectional**. If component A should be protected from changes in component B, then B should depend on A.

### LSP: The Liskov Substitution Principle

> *If S is a subtype of T, then objects of type T may be replaced with objects of type S without altering the correctness of the program.*

Applies beyond inheritance — to **interfaces, REST APIs, and service contracts**. Violations at the architectural level pollute systems with special-case mechanisms (e.g., `if` statements checking for specific vendors).

### ISP: The Interface Segregation Principle

> *Don't depend on things you don't use.*

Depending on modules that contain more than you need is harmful. At the architecture level: if system S depends on framework F which depends on database D, changes to unused features in D can force redeployment of S.

### DIP: The Dependency Inversion Principle

> *Source code dependencies must refer only to abstractions, not to concretions.*

Practical rules:
- Don't refer to volatile concrete classes — use abstract interfaces
- Don't derive from volatile concrete classes
- Don't override concrete functions
- Never mention the name of anything concrete and volatile

Use **Abstract Factories** to manage creation of concrete objects. The curved line separating abstract from concrete becomes the **architectural boundary**. Source code dependencies cross it pointing toward the abstract side.

---

## Part IV: Component Principles

### Component Cohesion — What Goes Inside Components

Three principles in tension:

1. **REP (Reuse/Release Equivalence Principle):** Classes grouped into a component must be releasable together and share a cohesive purpose.

2. **CCP (Common Closure Principle):** Gather classes that change for the same reasons and at the same times. Separate classes that change at different times for different reasons. *This is SRP for components.*

3. **CRP (Common Reuse Principle):** Don't force users of a component to depend on things they don't need. Classes not tightly bound should not be in the same component. *This is ISP for components.*

REP and CCP make components **larger** (inclusive). CRP makes components **smaller** (exclusive). A good architect finds the right balance for the project's current maturity. Early projects favor CCP (developability); mature projects shift toward REP/CRP (reusability).

### Component Coupling — Relationships Between Components

1. **ADP (Acyclic Dependencies Principle):** Allow no cycles in the component dependency graph. Cycles make testing, releasing, and independent development impossible. Break cycles with DIP (introduce an interface) or by extracting a new component.

2. **SDP (Stable Dependencies Principle):** Depend in the direction of stability. A component with many incoming dependencies is stable (hard to change). Volatile components should not be depended upon by stable components.

3. **SAP (Stable Abstractions Principle):** A component should be as abstract as it is stable. Stable components should be abstract so their stability does not prevent extension. Volatile components should be concrete.

**Component structure evolves** — it cannot be designed top-down before any code exists. It is a map to buildability and maintainability, not a functional decomposition.

---

## Part V: Architecture

### Chapter 15: What Is Architecture?

The architecture of a system is the **shape** given to it by those who build it — the division into components, their arrangement, and the communication pathways between them.

The purpose of architecture is to **keep options open** and to make the system **easy to understand, develop, deploy, and maintain**. Good architecture maximizes the number of decisions NOT made.

**The critical distinction:** Policy (business rules) vs. Details (IO devices, databases, frameworks, delivery mechanisms). A good architecture recognizes them as separate and ensures policy has no knowledge of details. Details can be deferred.

### Chapter 16: Independence

A good architecture supports:
- **Use cases** — The architecture should scream about what the system does
- **Operation** — Allows the system to scale
- **Development** — Allows independent team work (Conway's Law)
- **Deployment** — Immediate deployment ("Deploy-ability")

**Decoupling Modes (from lightest to heaviest):**
1. **Source level**: Separate modules in the same address space (monolith)
2. **Deployment level**: Separate deployable units (jars, DLLs, shared libraries)
3. **Service level**: Separate processes communicating over network (microservices)

> *A good architecture allows a system to be born as a monolith, deployed in a single file, but then to grow into independently deployable units, and then all the way to independent services and/or micro-services. Later, as things change, it should allow for reversing that progression.*

Don't start with services by default — it's expensive and encourages coarse-grained decoupling. Push decoupling to the point where a service *could* be formed, but leave components in the same address space as long as possible.

### Chapter 17: Boundaries — Drawing Lines

**Boundaries separate software elements and restrict knowledge.** They are drawn for the purpose of deferring decisions as long as possible.

- The GUI doesn't matter to the business rules → boundary
- The database doesn't matter to the business rules → boundary
- Frameworks don't matter to the business rules → boundary

**Plugin Architecture:** The core business rules are independent. Everything else (GUI, database, frameworks) is a plugin. Arranging systems into a plugin architecture creates firewalls across which changes cannot propagate.

**FitNesse case study:** By drawing a boundary between business rules and the database (using an interface), the team deferred the database decision for 18 months, eventually choosing flat files over MySQL. A customer later added MySQL support in a single day by implementing the interface.

### Chapter 18: Boundary Anatomy

Boundary types (from lightest to heaviest):
1. **Monolith** — Source-level decoupling, function calls. Very fast, chatty communication.
2. **Deployment components** — Dynamically linked libraries (DLLs, jars). Still function calls.
3. **Local processes** — Separate address spaces, communicate via sockets/IPC. Moderate cost.
4. **Services** — Network communication. Very slow. Avoid chattiness.

All follow the same rule: **source code dependencies point inward toward higher-level components**.

### Chapter 19: Policy and Level

**Level** = distance from inputs and outputs. The farther from IO, the higher the level. Higher-level policies change less frequently and for more important reasons. Lower-level policies change frequently for less important reasons.

Source code dependencies should be **decoupled from data flow** and **coupled to level**. Lower-level components should be plugins to higher-level components.

### Chapter 20: Business Rules

**Entities:** Objects embodying **Critical Business Rules** operating on **Critical Business Data**. They would exist even without automation. They are the highest-level, most general, most reusable code.

**Use Cases:** Application-specific business rules. They orchestrate Entities to achieve application goals. They describe input, processing, and output without mentioning UI or database.

**Hierarchy:** Entities know nothing of use cases. Use cases know about entities but not about UI/DB. Request/Response models should be independent plain data structures — never HttpRequest, Entity objects, or database rows.

### Chapter 21: Screaming Architecture

The architecture should **scream about the use cases**, not about the frameworks.

> *When you look at the top-level directory structure, it should scream "Health Care System" or "Accounting System" — not "Rails" or "Spring/Hibernate."*

- Architectures should not be supplied by frameworks
- Frameworks are tools, not architectures
- A good architecture makes framework decisions deferrable
- A testable architecture can run all use cases without frameworks, databases, or web servers in place

### Chapter 22: The Clean Architecture

The Clean Architecture integrates ideas from Hexagonal Architecture (Ports & Adapters), DCI, BCE, and others into a single actionable model.

**The Four Concentric Circles (inside to outside):**

1. **Entities** — Enterprise-wide Critical Business Rules
2. **Use Cases** — Application-specific business rules
3. **Interface Adapters** — Controllers, Presenters, Gateways (MVC lives here). Converts data between use case format and external format (DB, web)
4. **Frameworks & Drivers** — Web frameworks, databases, UI frameworks. Glue code only.

**THE DEPENDENCY RULE:**

> *Source code dependencies must point only inward, toward higher-level policies.*

- Nothing in an inner circle can know anything about an outer circle
- Data formats from outer circles must not be used by inner circles
- Data crossing boundaries must be in the form most convenient for the inner circle
- You may need more than four circles, but the Dependency Rule always applies

**Crossing boundaries:** Use the Dependency Inversion Principle. The use case calls an **output port interface** (in the inner circle); the presenter in the outer circle implements it.

**Typical Scenario (web-based Java):**
```
Web Server → Controller → [InputBoundary] → UseCaseInteractor → Entities
                                                    ↓
                                            [DataAccessInterface] → Database
                                                    ↓
                                            OutputData → [OutputBoundary] → Presenter → ViewModel → View
```

All dependencies point inward. The system is intrinsically testable. External parts (DB, web framework) can be replaced with minimum fuss.

### Chapter 23: Presenters and Humble Objects

The **Humble Object Pattern** separates hard-to-test behaviors from easy-to-test behaviors:

- **View** (humble, hard to test): Simply moves data from ViewModel into HTML/screen
- **Presenter** (testable): Formats data into strings, booleans, and flags in the ViewModel
- **Database Gateways** (humble): Simple SQL implementations behind polymorphic interfaces
- **Service Listeners** (humble): Format data to/from external services

At each architectural boundary, the Humble Object pattern appears. It vastly increases testability.

### Chapter 24: Partial Boundaries

Full boundaries are expensive. Three strategies for partial boundaries:

1. **Skip the Last Step:** Do all the design work (interfaces, data structures) but keep components in the same deployable unit.
2. **One-Dimensional Boundaries:** Use a Strategy pattern instead of full reciprocal interfaces.
3. **Facades:** A simple Facade class that delegates to service classes, without dependency inversion.

Each degrades over time if not maintained, but holds a place for a full boundary when needed.

### Chapter 25: Layers and Boundaries

Architectural boundaries exist everywhere, not just at the obvious places. Even a simple game has boundaries between business rules, language policy, data storage, and communication mechanisms.

**Over-engineering vs. under-engineering is a real tension.** You must watch for where boundaries may be needed, weigh the cost of implementing them vs. ignoring them, and add them at inflection points.

### Chapter 26: The Main Component

**Main is the dirtiest, lowest-level component.** It is the ultimate detail — the initial entry point. It creates factories, strategies, and global facilities, then hands control to high-level abstractions. Think of Main as a plugin to the application — one that sets up the initial conditions, then hands off. You could have different Main components for different configurations (Dev, Test, Production).

### Chapter 27: Services: Great and Small

**Services are not architecturally significant by themselves.** The architecture is defined by the boundaries *within* services and the dependencies that cross those boundaries — not by the physical mechanism of communication.

- Services do not inherently decouple
- Services can still be tightly coupled by shared data structures
- Internal component architecture within services should still follow the Dependency Rule
- A service might be a single component or composed of several components with architectural boundaries

### Chapter 28: The Test Boundary

**Tests are part of the system** and participate in the architecture. They follow the Dependency Rule — they are the outermost circle, depending inward on application components.

**The Fragile Tests Problem:** Tests coupled to volatile things (like GUIs) break with trivial changes, making the system rigid. The solution: create a **Testing API** that decouples tests from the application structure, allowing both to evolve independently.

Design for testability: **Don't depend on volatile things.** Business rules should be testable without the GUI, without the database, without the web server.

### Chapter 29: Clean Embedded Architecture

Embedded software principles apply universally:

1. **"First make it work. Then make it right. Then make it fast."** (Kent Beck) — Most systems only do step 1.
2. **The Hardware Abstraction Layer (HAL):** Separates software from firmware. Software above the HAL is testable off-target.
3. **The Operating System Abstraction Layer (OSAL):** Isolates software from OS dependencies.
4. **Program to interfaces and substitutability** at every layer.

The same principles apply to non-embedded code: SQL in your code = firmware. Platform dependencies spread throughout = firmware. Android API in your business logic = firmware.

---

## Part VI: Details

### Chapter 30: The Database Is a Detail

The **data model** is architecturally significant. The **database technology** (Oracle, MySQL, Mongo) is a low-level detail. The database is a utility for moving data between disk and RAM — nothing more.

Don't allow database rows/tables to leak into use cases or business rules. Knowledge of tabular structure should be restricted to the outermost circles.

### Chapter 31: The Web Is a Detail

The web is an IO device — a delivery mechanism. The oscillation between centralized and distributed computing has been going on since the 1960s. Your architecture should be ignorant of how it is delivered. You should be able to deliver it as a console app, web app, thick client, or service without undue change.

### Chapter 32: Frameworks Are Details

Frameworks are not architectures. The relationship is **asymmetric** — you commit to the framework; it commits nothing to you.

**Risks:** Frameworks violate the Dependency Rule by asking you to inherit from their base classes in your Entities. They may outgrow your needs, evolve in unhelpful directions, or be superseded.

**Solution:** Treat the framework as a detail. Keep it in the outer circle. Don't let it into your inner circles. Don't derive your Entities from framework base classes. Use the framework at arm's length.

### Chapter 33: Case Study — Video Sales

Demonstrates applying Clean Architecture to a real system: identifying actors, use cases, components, and managing dependencies so that views and presenters depend on use cases, which depend on entities. The goal is to create a **dependency structure** where changes in one area don't ripple through the entire system.

### Chapter 34: The Missing Chapter (by Simon Brown)

Four approaches to organizing code:

1. **Package by Layer:** Horizontal slicing (web, service, repository). Doesn't scream about the domain. Two layered architectures look identical from the directory structure.

2. **Package by Feature:** Vertical slicing by feature/use case. All code for "Orders" lives together. The directory structure screams about the domain.

3. **Ports and Adapters:** Inside (domain) and outside (infrastructure). Domain code has no dependencies on the outside.

4. **Package by Component:** Bundles business logic and persistence into a single coarse-grained component behind a well-defined interface. The web layer accesses functionality through the component's public interface.

**Critical insight:** Organization and encapsulation are different. A nice-looking package structure means nothing if you don't enforce the rules. In Java, making everything `public` defeats the purpose. **The devil is in the implementation details.** Use compiler-enforced access modifiers (package-private in Java, internal in C#) or architecture validation tools (ArchUnit, etc.) to maintain boundaries at the code level, not just the diagram level.

---

## Key Principles Summary

| Principle | Essence |
|---|---|
| **The Dependency Rule** | Source code dependencies point inward, toward higher-level policies |
| **SRP** | A module is responsible to one, and only one, actor |
| **OCP** | Open for extension, closed for modification — achieved through dependency hierarchy |
| **LSP** | Subtypes must be substitutable — violations pollute architecture with special cases |
| **ISP** | Don't depend on things you don't use |
| **DIP** | Depend on abstractions, not concretions |
| **REP** | The granule of reuse is the granule of release |
| **CCP** | Gather things that change together; separate things that change separately |
| **CRP** | Don't force users to depend on things they don't need |
| **ADP** | No cycles in the component dependency graph |
| **SDP** | Depend in the direction of stability |
| **SAP** | Stable components should be abstract |

## Architecture Checklist

- [ ] Business rules are independent of UI, database, and frameworks
- [ ] Use cases are the central organizing structure
- [ ] Source code dependencies point inward (toward entities and use cases)
- [ ] The database is a plugin — business rules don't know SQL or schema details
- [ ] The web/UI is a plugin — business rules don't know about HTTP, HTML, or presentation
- [ ] Frameworks are kept at arm's length — no framework base classes in entities
- [ ] The system is testable without UI, database, web server, or any external element
- [ ] Components have no dependency cycles
- [ ] Volatile components are not depended on by stable components
- [ ] Boundaries exist between things that change at different rates and for different reasons
- [ ] The directory structure screams about the domain, not the framework
- [ ] Data crossing boundaries is in simple structures (not Entity objects or DB rows)
- [ ] The Main component is the dirtiest module — it wires everything together
- [ ] The architecture allows starting as a monolith and growing to services if needed
- [ ] Access modifiers (package-private, internal) enforce boundaries, not just diagrams

## Architectural Smells (Anti-Patterns)

- **Framework-first architecture:** Top-level directory says "Rails" not "Health Care System"
- **Database-centric design:** Business rules coupled to SQL, ORM entities leaked across boundaries
- **Dependency cycles:** Component A depends on B depends on C depends on A
- **God classes:** One class responsible to multiple actors (violates SRP)
- **Premature service decomposition:** Microservices before understanding domain boundaries
- **Big Ball of Mud:** No discernible boundaries, everything depends on everything
- **Leaky abstractions:** HTTP request objects passed to use cases, DB rows returned to controllers
- **Rigid tests:** Tests coupled to UI structure or internal implementation details
- **Making messes to go fast:** "We'll clean it up later" — you won't, and messes are always slower
