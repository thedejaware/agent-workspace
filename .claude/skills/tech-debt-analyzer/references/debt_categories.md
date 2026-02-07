# Technical Debt Categories and Assessment

## Overview

Technical debt represents shortcuts, workarounds, or suboptimal solutions that reduce long-term code quality and maintainability. This reference provides a comprehensive framework for identifying, categorizing, and assessing technical debt.

## Debt Categories

### 1. Code Quality Debt

Code that works but is difficult to understand, maintain, or extend.

#### Indicators

**Code Smells:**
- Large files (>500 lines)
- Long functions (>50 lines)
- High cyclomatic complexity (>10)
- Deep nesting (>4 levels)
- Long parameter lists (>5 parameters)
- Duplicate code
- Magic numbers
- Unclear naming

**Examples:**
```csharp
// Bad: Complex method with multiple responsibilities
public AccessResult ProcessUserData(dynamic data)
{
    if (data != null && data.user != null)
    {
        var user = data.user;
        if (user.age > 18 && user.status == "active")
        {
            if (user.permissions != null)
            {
                foreach (var perm in user.permissions)
                {
                    if (perm.type == "admin")
                    {
                        // Deep nesting, unclear logic
                        if (perm.scope == "full")
                        {
                            return new AccessResult { Access = "granted", Level = "admin" };
                        }
                    }
                }
            }
        }
    }
    return new AccessResult { Access = "denied" };
}
```

**Impact:**
- High maintenance cost
- Difficult to understand and modify
- Error-prone
- Slows down development

**Priority:** Medium to High (depending on frequency of changes)

---

### 2. Architectural Debt

Structural issues in how code is organized and components interact.

#### Indicators

**Tight Coupling:**
- Components directly depend on implementation details
- Difficult to test in isolation
- Changes cascade across modules

**Poor Separation of Concerns:**
- Business logic mixed with UI code
- Data access mixed with business logic
- Multiple responsibilities in single module

**Missing Abstractions:**
- No clear interfaces or contracts
- Direct dependencies on concrete implementations
- Difficulty swapping implementations

**Examples:**
```csharp
// Bad: Service tightly coupled to infrastructure implementation
public class UserService
{
    private readonly HttpClient _httpClient = new HttpClient();

    public async Task<User> GetUserAsync(int userId)
    {
        // Direct HttpClient usage - tightly coupled to HTTP
        var response = await _httpClient.GetStringAsync(
            $"https://api.example.com/users/{userId}");

        // JSON parsing mixed with business logic
        var user = JsonConvert.DeserializeObject<User>(response);

        // Data transformation in service layer
        user.DisplayName = $"{user.FirstName} {user.LastName}".ToUpper();

        // Direct database access mixed in
        using (var db = new ApplicationDbContext())
        {
            db.UserLogs.Add(new UserLog { UserId = userId, Action = "Fetched" });
            await db.SaveChangesAsync();
        }

        return user;
    }
}

// Good: Proper separation of concerns
public class UserService
{
    private readonly IUserRepository _userRepository;
    private readonly IUserLogger _userLogger;

    public UserService(IUserRepository userRepository, IUserLogger userLogger)
    {
        _userRepository = userRepository;
        _userLogger = userLogger;
    }

    public async Task<User> GetUserAsync(int userId)
    {
        var user = await _userRepository.GetByIdAsync(userId);
        await _userLogger.LogUserAccessAsync(userId);
        return user;
    }
}
```

**Impact:**
- Difficult to modify or extend
- Hard to test
- Rigid architecture
- Prevents reuse

**Priority:** High (affects long-term maintainability)

---

### 3. Test Debt

Insufficient or inadequate test coverage.

#### Indicators

- Missing tests for critical functionality
- Low code coverage (<80%)
- No integration or E2E tests
- Fragile tests that break frequently
- Tests coupled to implementation details
- Slow test suite

**Test Coverage Gaps:**
- Untested edge cases
- Missing error handling tests
- No security tests
- No performance tests

**Examples:**
```csharp
// Bad: Test coupled to implementation
[Fact]
public void UserService_ShouldHaveInternalCache()
{
    var service = new UserService();

    // Testing internal implementation details
    Assert.NotNull(service.InternalCache);
    Assert.Equal("https://api.example.com", service.ApiClient.BaseUrl);
}

// Missing: Actual behavior tests
// - Does it fetch users correctly?
// - Does it handle errors?
// - Does it cache properly?

// Good: Test behavior, not implementation
[Fact]
public async Task GetUserAsync_WithValidId_ReturnsUser()
{
    // Arrange
    var mockRepository = new Mock<IUserRepository>();
    mockRepository.Setup(r => r.GetByIdAsync(123))
        .ReturnsAsync(new User { Id = 123, Name = "John Doe" });
    var service = new UserService(mockRepository.Object);

    // Act
    var result = await service.GetUserAsync(123);

    // Assert
    Assert.NotNull(result);
    Assert.Equal("John Doe", result.Name);
}
```

**Impact:**
- Fear of refactoring
- Bugs slip into production
- Regression issues
- Slow development velocity

**Priority:** High for critical paths, Medium for others

---

### 4. Documentation Debt

Missing or outdated documentation.

#### Indicators

- No README or setup instructions
- Missing API documentation
- Outdated architecture diagrams
- No inline comments for complex logic
- Missing decision records (ADRs)
- No changelog

**Examples:**
```csharp
// Bad: Complex logic with no explanation
public decimal CalculatePrice(List<Item> items, User user, Promo promo)
{
    return items.Sum(item =>
        item.Price * (1 - (user.Tier == "gold" ? 0.15m :
        user.Tier == "silver" ? 0.10m : 0m)) *
        (promo?.Code == "SAVE20" ? 0.8m : 1m)) *
        (user.Country == "US" ? 1.07m : 1m);
}

// Good: Documented logic
/// <summary>
/// Calculate final price with tier discounts and tax
/// </summary>
/// <remarks>
/// Applies discounts and taxes in the following order:
/// 1. Tier discount (Gold: 15%, Silver: 10%, Bronze: 0%)
/// 2. Promo code discount (SAVE20: 20% off)
/// 3. Sales tax (US: 7%, Other: 0%)
/// </remarks>
/// <param name="items">List of items to calculate price for</param>
/// <param name="user">User with tier and country information</param>
/// <param name="promo">Optional promotional code</param>
/// <returns>Final price including all discounts and taxes</returns>
public decimal CalculatePrice(List<Item> items, User user, Promo promo)
{
    var subtotal = CalculateSubtotal(items);
    var tierDiscount = GetTierDiscount(user.Tier);
    var promoDiscount = GetPromoDiscount(promo);
    var tax = GetSalesTax(user.Country);

    return subtotal * (1 - tierDiscount) * (1 - promoDiscount) * (1 + tax);
}
```

**Impact:**
- Onboarding takes longer
- Knowledge loss when developers leave
- Duplicate work
- Poor decision making

**Priority:** Medium (varies by project)

---

### 5. Dependency Debt

Issues with third-party libraries and packages.

#### Indicators

- Outdated dependencies
- Deprecated packages
- Security vulnerabilities
- Unused dependencies
- Version conflicts
- Duplicate functionality

**Examples:**
```xml
<!-- Bad: Outdated and deprecated packages -->
<ItemGroup>
  <PackageReference Include="Newtonsoft.Json" Version="12.0.3" />
  <!-- Consider System.Text.Json (built-in) -->

  <PackageReference Include="System.Data.SqlClient" Version="4.8.2" />
  <!-- Deprecated - use Microsoft.Data.SqlClient -->

  <PackageReference Include="NLog" Version="4.7.0" />
  <!-- AND -->
  <PackageReference Include="Serilog" Version="2.10.0" />
  <!-- Duplicate logging functionality -->

  <PackageReference Include="AutoMapper" Version="10.0.0" />
  <!-- Consider Mapperly (source generator, better performance) -->
</ItemGroup>

<!-- Good: Modern packages -->
<ItemGroup>
  <PackageReference Include="Microsoft.Data.SqlClient" Version="5.1.0" />
  <PackageReference Include="Serilog" Version="3.1.1" />
  <PackageReference Include="Mapperly" Version="3.3.0" />
</ItemGroup>
```

**Impact:**
- Security vulnerabilities
- Missing features and bug fixes
- Larger bundle sizes
- Maintenance burden

**Priority:** High for security issues, Medium for others

---

### 6. Performance Debt

Code that works but performs poorly.

#### Indicators

- N+1 query problems
- Missing database indexes
- Inefficient algorithms
- Memory leaks
- Large bundle sizes
- Slow API responses
- Unnecessary re-renders

**Examples:**
```csharp
// Bad: N+1 query problem
public async Task<List<User>> GetUsersWithPostsAsync()
{
    var users = await _context.Users.ToListAsync();

    // Separate query for each user!
    foreach (var user in users)
    {
        user.Posts = await _context.Posts
            .Where(p => p.UserId == user.Id)
            .ToListAsync();
    }

    return users;
}

// Good: Single query with eager loading
public async Task<List<User>> GetUsersWithPostsAsync()
{
    return await _context.Users
        .Include(u => u.Posts)
        .ToListAsync();
}

// Also Good: Use projection if you only need specific fields
public async Task<List<UserWithPostsDto>> GetUsersWithPostCountAsync()
{
    return await _context.Users
        .Select(u => new UserWithPostsDto
        {
            UserId = u.Id,
            UserName = u.Name,
            PostCount = u.Posts.Count
        })
        .ToListAsync();
}
```

**Impact:**
- Poor user experience
- Higher infrastructure costs
- Scalability issues
- Customer churn

**Priority:** High for user-facing features, Medium for internal tools

---

### 7. Security Debt

Security vulnerabilities and weaknesses.

#### Indicators

- Missing input validation
- No authentication/authorization
- Exposed secrets in code
- SQL injection vulnerabilities
- XSS vulnerabilities
- CSRF vulnerabilities
- Insecure dependencies

**Examples:**
```csharp
// Bad: SQL injection vulnerability
public User GetUser(string userId)
{
    var query = $"SELECT * FROM Users WHERE Id = {userId}";
    return _db.Query<User>(query).FirstOrDefault();
}

// Good: Use parameterized queries
public User GetUser(string userId)
{
    var query = "SELECT * FROM Users WHERE Id = @UserId";
    return _db.Query<User>(query, new { UserId = userId }).FirstOrDefault();
}

// Better: Use ORM
public async Task<User> GetUserAsync(int userId)
{
    return await _context.Users.FindAsync(userId);
}

// Bad: Exposed secrets in code
public class ApiClient
{
    private const string ApiKey = "sk_live_abc123xyz789";
    private const string ConnectionString = "Server=prod-db;Database=MyApp;User=admin;Password=P@ssw0rd123";
}

// Good: Use configuration and secrets management
public class ApiClient
{
    private readonly string _apiKey;
    private readonly string _connectionString;

    public ApiClient(IConfiguration configuration)
    {
        _apiKey = configuration["ApiSettings:ApiKey"];
        _connectionString = configuration.GetConnectionString("DefaultConnection");
    }
}

// Bad: No input validation
public async Task<IActionResult> CreateUser(string email, string name)
{
    var user = new User { Email = email, Name = name };
    await _context.Users.AddAsync(user);
    await _context.SaveChangesAsync();
    return Ok(user);
}

// Good: Input validation
public async Task<IActionResult> CreateUser([FromBody] CreateUserRequest request)
{
    if (!ModelState.IsValid)
        return BadRequest(ModelState);

    if (!IsValidEmail(request.Email))
        return BadRequest("Invalid email format");

    var user = new User { Email = request.Email, Name = request.Name };
    await _context.Users.AddAsync(user);
    await _context.SaveChangesAsync();
    return Ok(user);
}
```

**Impact:**
- Data breaches
- Legal liability
- Reputation damage
- Financial loss

**Priority:** Critical (immediate fix required)

---

### 8. Infrastructure/DevOps Debt

Issues with deployment, CI/CD, and infrastructure.

#### Indicators

- Manual deployment process
- No CI/CD pipeline
- Missing environment configs
- No monitoring or logging
- No backup strategy
- Hardcoded configuration
- Missing disaster recovery

**Examples:**
```csharp
// Bad: Hardcoded environment-specific values
public class AppSettings
{
    public const string ApiUrl = "https://prod-api.example.com";
    public const string DbHost = "10.0.1.52";
    public const bool CacheEnabled = true;
}

// Good: Environment-based configuration (appsettings.json)
// appsettings.json
{
  "ApiSettings": {
    "ApiUrl": "https://api.example.com",
    "Timeout": 30
  },
  "ConnectionStrings": {
    "DefaultConnection": "Server=(localdb)\\mssqllocaldb;Database=MyApp"
  },
  "Cache": {
    "Enabled": true,
    "ExpirationMinutes": 60
  }
}

// Startup.cs or Program.cs
public class Startup
{
    public void ConfigureServices(IServiceCollection services)
    {
        services.Configure<ApiSettings>(Configuration.GetSection("ApiSettings"));
        services.Configure<CacheSettings>(Configuration.GetSection("Cache"));
    }
}

// Usage with Options pattern
public class MyService
{
    private readonly ApiSettings _apiSettings;

    public MyService(IOptions<ApiSettings> apiSettings)
    {
        _apiSettings = apiSettings.Value;
    }

    public async Task<string> CallApiAsync()
    {
        using var client = new HttpClient();
        client.BaseAddress = new Uri(_apiSettings.ApiUrl);
        client.Timeout = TimeSpan.FromSeconds(_apiSettings.Timeout);
        // Use configuration values
    }
}
```

**Impact:**
- Deployment errors
- Downtime
- Difficult rollbacks
- Slow incident response

**Priority:** High (reduces operational risk)

---

### 9. Design Debt

UI/UX issues and inconsistencies.

#### Indicators

- Inconsistent styling
- No design system
- Accessibility issues
- Poor responsive design
- Inconsistent user flows
- Duplicate components

**Examples:**
```csharp
// Bad: Inconsistent UI component usage across Blazor/Razor app
// Page1.razor
<button style="background: blue; padding: 10px">Submit</button>

// Page2.razor
<button class="btn btn-primary">Submit</button>

// Page3.razor
<MatButton Color="primary">Submit</MatButton>

// Good: Consistent design system with shared components
// Shared/Components/AppButton.razor
<button class="@GetButtonClass()" @onclick="OnClick">
    @ChildContent
</button>

@code {
    [Parameter] public ButtonVariant Variant { get; set; } = ButtonVariant.Primary;
    [Parameter] public RenderFragment ChildContent { get; set; }
    [Parameter] public EventCallback OnClick { get; set; }

    private string GetButtonClass() => Variant switch
    {
        ButtonVariant.Primary => "btn btn-primary",
        ButtonVariant.Secondary => "btn btn-secondary",
        ButtonVariant.Danger => "btn btn-danger",
        _ => "btn"
    };
}

// Usage - consistent across all pages
<AppButton Variant="ButtonVariant.Primary" OnClick="HandleSubmit">
    Submit
</AppButton>
```

**Impact:**
- Poor user experience
- Brand inconsistency
- Accessibility compliance issues
- Higher development cost

**Priority:** Medium (varies by product)

---

## Assessment Framework

### Severity Levels

**Critical:**
- Security vulnerabilities
- Production-breaking issues
- Data loss risks
- Immediate action required

**High:**
- Significant performance issues
- Architectural problems blocking features
- High-risk areas with no tests
- Action required within sprint

**Medium:**
- Code quality issues
- Missing documentation
- Outdated dependencies (non-security)
- Address in next few sprints

**Low:**
- Minor code smells
- Optimization opportunities
- Nice-to-have improvements
- Address when convenient

### Impact Assessment

**Business Impact:**
- Does it affect user experience?
- Does it block new features?
- Does it increase costs?
- Does it create risk?

**Technical Impact:**
- How difficult to fix?
- How widespread is the issue?
- How frequently is code changed?
- What's the maintenance burden?

**Urgency:**
- Is it getting worse over time?
- Will it be harder to fix later?
- Is there a deadline or trigger event?

### Prioritization Matrix

| Impact / Effort | Low Effort | Medium Effort | High Effort |
|----------------|-----------|---------------|-------------|
| High Impact    | Do First  | Do Second     | Plan & Do   |
| Medium Impact  | Do Second | Plan & Do     | Consider    |
| Low Impact     | Quick Win | Consider      | Avoid       |

---

## Measurement Metrics

### Code Quality Metrics

- **Lines of Code (LOC):** Track file/function sizes
- **Cyclomatic Complexity:** Measure code complexity
- **Code Duplication:** Percentage of duplicated code
- **Test Coverage:** Percentage of code covered by tests
- **Code Churn:** Frequency of changes to files

### Dependency Metrics

- **Outdated Dependencies:** Count of packages behind latest
- **Vulnerable Dependencies:** Count with known CVEs
- **Dependency Age:** Time since last update
- **Bundle Size:** Total size of dependencies

### Development Metrics

- **Build Time:** Time to build project
- **Test Execution Time:** Time to run test suite
- **Deployment Frequency:** How often code is deployed
- **Lead Time:** Time from commit to production
- **MTTR:** Mean time to recovery from incidents

---

## Documentation Standards

### Required Documentation

1. **README.md**
   - Project overview
   - Setup instructions
   - Development workflow
   - Testing approach

2. **Architecture Docs**
   - System architecture diagram
   - Data flow diagrams
   - Technology stack
   - Key design decisions

3. **API Documentation**
   - Endpoint descriptions
   - Request/response formats
   - Authentication
   - Error codes

4. **Code Comments**
   - Complex algorithms
   - Non-obvious business logic
   - Workarounds and their reasons
   - TODOs with context

5. **ADRs (Architecture Decision Records)**
   - Context for major decisions
   - Alternatives considered
   - Rationale for choice
   - Consequences

---

## Prevention Strategies

### Code Review Checklist

- [ ] No code smells introduced
- [ ] Tests added/updated
- [ ] Documentation updated
- [ ] No security vulnerabilities
- [ ] Performance considered
- [ ] Accessibility addressed
- [ ] No new dependencies without justification

### Automated Prevention

- **Code Analysis:** Roslyn analyzers, StyleCop, SonarAnalyzer
- **Formatting:** EditorConfig, consistent style across team
- **Testing:** Required minimum coverage (coverlet, ReportGenerator)
- **Security:** Automated vulnerability scanning (`dotnet list package --vulnerable`)
- **Performance:** BenchmarkDotNet for performance regression tests
- **Dependencies:** Automated update PRs (Dependabot for NuGet packages)

### Regular Maintenance

- Weekly: Review TODO/FIXME comments
- Monthly: Dependency updates
- Quarterly: Architecture review
- Annually: Major refactoring initiatives
