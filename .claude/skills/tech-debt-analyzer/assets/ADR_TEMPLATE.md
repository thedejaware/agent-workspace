# ADR-XXX: [Short Title of Decision]

**Status:** [Proposed / Accepted / Deprecated / Superseded]

**Date:** [YYYY-MM-DD]

**Deciders:** [List of people involved in the decision]

**Technical Story:** [Description, ticket/issue URL]

---

## Context and Problem Statement

[Describe the context and problem statement, e.g., in free form using two to three sentences. You may want to articulate the problem in form of a question.]

**Key Constraints:**
- [List any constraints that limit the solution space]

**Key Requirements:**
- [List must-have requirements]

---

## Decision Drivers

[List the factors that influenced the decision, e.g.:]

- [driver 1, e.g., performance requirement]
- [driver 2, e.g., team expertise]
- [driver 3, e.g., cost constraints]
- [etc.]

---

## Considered Options

### Option 1: [Name]

**Description:**
[Brief description of this option]

**Pros:**
- [good, because...]
- [good, because...]

**Cons:**
- [bad, because...]
- [bad, because...]

**Effort:** [Estimated effort]

---

### Option 2: [Name]

**Description:**
[Brief description of this option]

**Pros:**
- [good, because...]
- [good, because...]

**Cons:**
- [bad, because...]
- [bad, because...]

**Effort:** [Estimated effort]

---

### Option 3: [Name]

[Repeat structure for each option considered]

---

## Decision Outcome

**Chosen option:** "[Option X: Name]"

**Rationale:**
[Explain why this option was chosen. What makes it the best choice given the context and decision drivers?]

---

## Consequences

### Positive Consequences

- [e.g., improvement of quality attribute satisfaction, follow-up decisions required, ...]
- [...]

### Negative Consequences

- [e.g., compromising quality attribute, follow-up decisions required, ...]
- [...]

### Technical Debt

[Any technical debt being incurred as a result of this decision? How will it be tracked?]

---

## Implementation

**Action Items:**
- [ ] [Implementation task 1]
- [ ] [Implementation task 2]
- [ ] [etc.]

**Timeline:** [Expected implementation timeline]

**Rollback Plan:** [How to revert this decision if needed]

---

## Validation

**Success Metrics:**
[How will we measure if this decision was correct?]

**Review Date:** [When should we review this decision?]

---

## References

- [Link to supporting documents]
- [Link to related ADRs]
- [Link to research/benchmarks]

---

## Notes

[Any additional notes, context, or discussion points]

---

## Example (.NET/C# Context)

```markdown
# ADR-005: Migrate from Newtonsoft.Json to System.Text.Json

**Status:** Accepted
**Date:** 2024-02-07
**Deciders:** Engineering Team
**Technical Story:** #PROJ-456

## Context and Problem Statement

The project currently uses Newtonsoft.Json for JSON serialization. System.Text.Json is now the recommended JSON library for .NET, offering better performance and being part of the framework.

**Key Constraints:**
- Must maintain API contract compatibility
- Migration must not break existing integrations
- Performance improvement is desired

**Key Requirements:**
- Serialize/deserialize complex DTOs
- Handle custom converters
- Support polymorphic deserialization

## Decision Drivers

- Performance (System.Text.Json is 2-3x faster)
- Reduced dependencies (System.Text.Json is built-in)
- Microsoft recommendation for new .NET applications
- Active development and long-term support
- Smaller memory footprint

## Considered Options

### Option 1: System.Text.Json

**Description:**
Migrate to System.Text.Json, the built-in JSON library in .NET

**Pros:**
- 2-3x better performance than Newtonsoft.Json
- Part of .NET framework (no external dependency)
- Lower memory allocation
- Active Microsoft support
- Modern API design

**Cons:**
- Less feature-rich than Newtonsoft.Json
- Some converters need rewriting
- Migration effort for existing code
- Different default behavior for property naming

**Effort:** 5 days

### Option 2: Keep Newtonsoft.Json

**Description:**
Continue using Newtonsoft.Json

**Pros:**
- No migration effort
- Team familiar with API
- Feature-rich and mature

**Cons:**
- External dependency
- Slower performance
- Larger memory footprint
- Not the recommended approach for modern .NET

**Effort:** 0 days

### Option 3: Gradual Migration

**Description:**
Run both libraries side-by-side, migrating incrementally

**Pros:**
- Lower risk
- Can test thoroughly
- Gradual team learning

**Cons:**
- Increases dependencies temporarily
- Inconsistent codebase during migration
- Higher complexity

**Effort:** 8 days

## Decision Outcome

**Chosen option:** "Option 1: System.Text.Json"

**Rationale:**
System.Text.Json offers significant performance benefits and aligns with Microsoft's recommendations for modern .NET applications. The migration effort is reasonable given the long-term benefits of reduced dependencies and improved performance.

## Consequences

### Positive Consequences

- 40% reduction in JSON serialization time (measured in benchmarks)
- Removal of Newtonsoft.Json dependency reduces package count
- Future-proof as it's Microsoft's recommended approach
- Better integration with ASP.NET Core
- Reduced memory allocations in hot paths

### Negative Consequences

- One-time migration effort (5 days estimated)
- Team needs to learn new API patterns
- Some custom converters need rewriting
- Breaking change for any code expecting Newtonsoft.Json behavior

### Technical Debt

None - this resolves existing dependency debt

## Implementation

**Action Items:**
- [x] Create System.Text.Json converters for custom types
- [x] Update DTOs with JsonPropertyName attributes
- [x] Replace JsonConvert calls with JsonSerializer
- [x] Update unit tests
- [x] Performance benchmarking
- [x] Update documentation

**Timeline:** Sprint 24 (2 weeks)

**Rollback Plan:**
Revert commits and restore Newtonsoft.Json package reference if critical issues found

## Validation

**Success Metrics:**
- All existing JSON tests pass
- Performance improvement of 30%+ measured
- No regression in functionality
- Reduced NuGet dependencies by 1

**Review Date:** 2024-05-01 (3 months post-migration)

## References

- [System.Text.Json Migration Guide](https://docs.microsoft.com/en-us/dotnet/standard/serialization/system-text-json-migrate-from-newtonsoft-how-to)
- [Performance Comparison](https://devblogs.microsoft.com/dotnet/performance-improvements-in-net-6/)
- Internal Benchmark Results: docs/benchmarks/json-serialization.md

## Notes

- ASP.NET Core 3.0+ uses System.Text.Json by default
- Some edge cases (e.g., circular references) require additional configuration
- Custom DateTime format handling differs from Newtonsoft.Json
```
