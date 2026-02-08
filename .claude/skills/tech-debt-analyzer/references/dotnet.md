# .NET/C# Technical Debt Reference

## Overview

This reference provides .NET/C# specific guidance for identifying, analyzing, and addressing technical debt in .NET codebases.

## Automated Analysis Tools

### Built-in .NET Tools

**Dependency Analysis:**
```bash
# Check for outdated packages
dotnet list package --outdated

# Check for vulnerable packages
dotnet list package --vulnerable

# Check for deprecated packages
dotnet list package --deprecated
```

**Code Analysis:**
```bash
# Run code analysis
dotnet build /p:RunAnalyzers=true /p:TreatWarningsAsErrors=true

# Generate code metrics
dotnet msbuild /t:Metrics
```

### Recommended Third-Party Tools (Optional)

These tools enhance analysis capabilities but are **not required**. Install them based on your needs:

**Code Quality:**
- **SonarQube/SonarLint** - Comprehensive code quality analysis
  ```bash
  # Install SonarLint extension in VS Code or Visual Studio
  # Or run SonarQube scanner for CI/CD
  ```
- **StyleCop.Analyzers** - Code style and consistency
  ```bash
  # Add to your .csproj or Directory.Build.props
  dotnet add package StyleCop.Analyzers
  ```
- **Roslynator** - Roslyn-based analyzers and refactorings
  ```bash
  dotnet add package Roslynator.Analyzers
  ```
- **SecurityCodeScan** - Security vulnerability detection
  ```bash
  dotnet add package SecurityCodeScan.VS2019
  ```

**Performance (for advanced analysis):**
- **BenchmarkDotNet** - Performance benchmarking
- **dotTrace** - Performance profiling (JetBrains, commercial)
- **dotMemory** - Memory profiling (JetBrains, commercial)

**Test Coverage:**
- **Coverlet** - Cross-platform code coverage
  ```bash
  dotnet add package coverlet.collector
  ```
- **ReportGenerator** - Coverage report visualization
  ```bash
  dotnet tool install -g dotnet-reportgenerator-globaltool
  ```

**Note**: The skill works with built-in .NET tools. These are optional enhancements for deeper analysis.

## Common .NET Code Smells

### 1. Weak Typing Issues

**Using `dynamic` keyword:**
```csharp
// Bad: Loses compile-time type safety
public dynamic ProcessData(dynamic input)
{
    return input.SomeProperty; // No IntelliSense, runtime errors
}

// Good: Use generic types or specific types
public T ProcessData<T>(T input) where T : IDataModel
{
    return input;
}
```

**Excessive `object` casting:**
```csharp
// Bad: Type safety lost
public void ProcessItems(List<object> items)
{
    foreach (var item in items)
    {
        var data = (MyData)item; // Unsafe cast
    }
}

// Good: Use generic types
public void ProcessItems<T>(List<T> items) where T : IProcessable
{
    foreach (var item in items)
    {
        item.Process();
    }
}
```

### 2. Nullable Reference Issues

**Not using nullable reference types:**
```csharp
// Bad: Nullable not enabled, potential NullReferenceException
public string GetUserName(User user)
{
    return user.Name; // What if user is null?
}

// Good: Enable nullable reference types
#nullable enable
public string GetUserName(User? user)
{
    return user?.Name ?? "Unknown";
}
```

### 3. Improper Exception Handling

**Empty catch blocks:**
```csharp
// Bad: Swallows exceptions
try
{
    ProcessData();
}
catch (Exception)
{
    // Silent failure
}

// Good: Handle or log exceptions
try
{
    ProcessData();
}
catch (Exception ex)
{
    _logger.LogError(ex, "Failed to process data");
    throw; // Re-throw if can't handle
}
```

**Catching generic Exception:**
```csharp
// Bad: Catches everything including system exceptions
try
{
    ProcessData();
}
catch (Exception ex)
{
    return false;
}

// Good: Catch specific exceptions
try
{
    ProcessData();
}
catch (ValidationException ex)
{
    _logger.LogWarning(ex, "Validation failed");
    return false;
}
catch (DataAccessException ex)
{
    _logger.LogError(ex, "Database error");
    throw;
}
```

### 4. EF Core N+1 Query Problems

```csharp
// Bad: N+1 query problem
public async Task<List<User>> GetUsersWithPostsAsync()
{
    var users = await _context.Users.ToListAsync();

    foreach (var user in users) // Separate query for each user!
    {
        user.Posts = await _context.Posts
            .Where(p => p.UserId == user.Id)
            .ToListAsync();
    }

    return users;
}

// Good: Eager loading with Include
public async Task<List<User>> GetUsersWithPostsAsync()
{
    return await _context.Users
        .Include(u => u.Posts)
        .ToListAsync();
}

// Better: Projection for specific fields
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

### 5. Improper Async/Await Usage

```csharp
// Bad: Blocking on async code
public User GetUser(int id)
{
    return _userService.GetUserAsync(id).Result; // Deadlock risk!
}

// Bad: Unnecessary async/await
public async Task<int> GetCountAsync()
{
    return await Task.FromResult(5); // Just return 5!
}

// Good: Async all the way
public async Task<User> GetUserAsync(int id)
{
    return await _userService.GetUserAsync(id);
}

// Good: No async needed here
public int GetCount()
{
    return 5;
}
```

### 6. Improper Disposal

```csharp
// Bad: Resource not disposed
public void ProcessFile(string path)
{
    var stream = File.OpenRead(path);
    // Process stream...
    // stream never disposed!
}

// Good: Using statement ensures disposal
public void ProcessFile(string path)
{
    using (var stream = File.OpenRead(path))
    {
        // Process stream...
    } // Automatically disposed
}

// Better: Using declaration (C# 8+)
public void ProcessFile(string path)
{
    using var stream = File.OpenRead(path);
    // Process stream...
    // Automatically disposed at end of scope
}
```

## Dependency Debt Patterns

### Deprecated NuGet Packages

Common packages to migrate away from:

| Deprecated Package | Recommended Alternative | Reason |
|-------------------|------------------------|---------|
| `System.Data.SqlClient` | `Microsoft.Data.SqlClient` | Official replacement, actively maintained |
| `Newtonsoft.Json` | `System.Text.Json` | Built-in, better performance, smaller size |
| `Microsoft.AspNet.*` | `Microsoft.AspNetCore.*` | ASP.NET Core is the modern framework |
| `log4net` | `Microsoft.Extensions.Logging` + `Serilog`/`NLog` | Better integration with .NET ecosystem |
| `AutoMapper` | `Mapperly` | Source generator, compile-time, better performance |

### Framework Targeting Issues

**Out of Support:**
- .NET Framework 4.5-4.6.1: Out of support
- .NET Core 2.x, 3.x: Out of support
- .NET 5: Out of support (May 2022)
- .NET 6: Out of support (November 2024)
- .NET 7: Out of support (May 2024)

**Current Recommendations:**
- .NET 8: LTS (Long Term Support) until November 2026
- .NET 9: STS (Standard Term Support) until May 2026

**Migration Path:**
```xml
<!-- Current: Outdated -->
<TargetFramework>net6.0</TargetFramework>

<!-- Recommended: Upgrade to LTS -->
<TargetFramework>net8.0</TargetFramework>
```

## Configuration Best Practices

### Enable Code Analysis

**Directory.Build.props** (applies to all projects in solution):
```xml
<Project>
  <PropertyGroup>
    <!-- Enable all .NET analyzers -->
    <EnableNETAnalyzers>true</EnableNETAnalyzers>
    <AnalysisLevel>latest</AnalysisLevel>

    <!-- Treat warnings as errors -->
    <TreatWarningsAsErrors>true</TreatWarningsAsErrors>

    <!-- Enable nullable reference types -->
    <Nullable>enable</Nullable>

    <!-- Language version -->
    <LangVersion>latest</LangVersion>
  </PropertyGroup>

  <!-- Add analyzers -->
  <ItemGroup>
    <PackageReference Include="StyleCop.Analyzers" Version="1.2.0-beta.556">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
    </PackageReference>
    <PackageReference Include="SonarAnalyzer.CSharp" Version="9.16.0.82469">
      <PrivateAssets>all</PrivateAssets>
      <IncludeAssets>runtime; build; native; contentfiles; analyzers</IncludeAssets>
    </PackageReference>
  </ItemGroup>
</Project>
```

### EditorConfig for Consistent Style

**.editorconfig:**
```ini
root = true

[*.cs]
# Indentation
indent_style = space
indent_size = 4

# New line preferences
end_of_line = crlf
insert_final_newline = true

# Code style rules
dotnet_style_qualification_for_field = false:suggestion
dotnet_style_qualification_for_property = false:suggestion
dotnet_style_predefined_type_for_locals_parameters_members = true:warning

# Naming conventions
dotnet_naming_rule.interfaces_should_be_prefixed_with_i.severity = warning
dotnet_naming_rule.interfaces_should_be_prefixed_with_i.symbols = interface
dotnet_naming_rule.interfaces_should_be_prefixed_with_i.style = begins_with_i

# Null checking
dotnet_style_prefer_is_null_check_over_reference_equality_method = true:warning
```

## Architectural Debt Patterns

### Dependency Injection Anti-patterns

**Service Locator Pattern (Anti-pattern):**
```csharp
// Bad: Service Locator hides dependencies
public class OrderService
{
    public void ProcessOrder(Order order)
    {
        var repo = ServiceLocator.Get<IOrderRepository>();
        var logger = ServiceLocator.Get<ILogger>();
        // Hidden dependencies!
    }
}

// Good: Constructor Injection makes dependencies explicit
public class OrderService
{
    private readonly IOrderRepository _repository;
    private readonly ILogger<OrderService> _logger;

    public OrderService(IOrderRepository repository, ILogger<OrderService> logger)
    {
        _repository = repository;
        _logger = logger;
    }

    public void ProcessOrder(Order order)
    {
        // Dependencies are clear
    }
}
```

### Static Classes for State (Anti-pattern)

```csharp
// Bad: Static state is global, hard to test
public static class UserContext
{
    public static User CurrentUser { get; set; }
    public static List<Role> Roles { get; set; } = new();
}

// Good: Use instance-based services
public interface IUserContext
{
    User CurrentUser { get; }
    IReadOnlyList<Role> Roles { get; }
}

public class HttpUserContext : IUserContext
{
    private readonly IHttpContextAccessor _httpContextAccessor;

    public HttpUserContext(IHttpContextAccessor httpContextAccessor)
    {
        _httpContextAccessor = httpContextAccessor;
    }

    public User CurrentUser => GetCurrentUser();
    public IReadOnlyList<Role> Roles => GetRoles();

    private User GetCurrentUser() { /* ... */ }
    private IReadOnlyList<Role> GetRoles() { /* ... */ }
}
```

## Testing Debt

### Missing Test Patterns

**Unit Tests:**
```csharp
// Use xUnit, NUnit, or MSTest
// Use mocking frameworks: Moq, NSubstitute, FakeItEasy

[Fact]
public async Task GetUserAsync_WithValidId_ReturnsUser()
{
    // Arrange
    var mockRepo = new Mock<IUserRepository>();
    mockRepo.Setup(r => r.GetByIdAsync(123))
        .ReturnsAsync(new User { Id = 123, Name = "John" });
    var service = new UserService(mockRepo.Object);

    // Act
    var result = await service.GetUserAsync(123);

    // Assert
    Assert.NotNull(result);
    Assert.Equal("John", result.Name);
}
```

**Integration Tests:**
```csharp
// Use WebApplicationFactory for ASP.NET Core
public class UsersControllerTests : IClassFixture<WebApplicationFactory<Program>>
{
    private readonly WebApplicationFactory<Program> _factory;

    public UsersControllerTests(WebApplicationFactory<Program> factory)
    {
        _factory = factory;
    }

    [Fact]
    public async Task GetUsers_ReturnsSuccessStatusCode()
    {
        var client = _factory.CreateClient();
        var response = await client.GetAsync("/api/users");

        response.EnsureSuccessStatusCode();
    }
}
```

## Performance Optimization

### Common Performance Issues

**StringBuilder for String Concatenation:**
```csharp
// Bad: String concatenation in loop
public string BuildReport(List<Item> items)
{
    string report = "";
    foreach (var item in items)
    {
        report += $"{item.Name}: {item.Value}\n"; // Creates new string each time
    }
    return report;
}

// Good: Use StringBuilder
public string BuildReport(List<Item> items)
{
    var sb = new StringBuilder();
    foreach (var item in items)
    {
        sb.AppendLine($"{item.Name}: {item.Value}");
    }
    return sb.ToString();
}
```

**LINQ Optimization:**
```csharp
// Bad: Multiple enumerations
public bool HasActiveUsers(IEnumerable<User> users)
{
    if (users.Any())
    {
        return users.Any(u => u.IsActive); // Enumerates again!
    }
    return false;
}

// Good: Single enumeration
public bool HasActiveUsers(IEnumerable<User> users)
{
    return users.Any(u => u.IsActive);
}

// Bad: Unnecessary ToList()
public int GetActiveUserCount(IQueryable<User> users)
{
    return users.Where(u => u.IsActive).ToList().Count(); // Loads all into memory
}

// Good: Execute query on database
public int GetActiveUserCount(IQueryable<User> users)
{
    return users.Count(u => u.IsActive); // SQL COUNT()
}
```

## Security Debt

### SQL Injection Prevention

```csharp
// Bad: String concatenation
public User GetUser(string username)
{
    var query = $"SELECT * FROM Users WHERE Username = '{username}'";
    return _db.Query<User>(query).FirstOrDefault();
}

// Good: Parameterized queries
public User GetUser(string username)
{
    var query = "SELECT * FROM Users WHERE Username = @Username";
    return _db.Query<User>(query, new { Username = username }).FirstOrDefault();
}

// Best: Use ORM (EF Core)
public async Task<User> GetUserAsync(string username)
{
    return await _context.Users.FirstOrDefaultAsync(u => u.Username == username);
}
```

### Secrets Management

```csharp
// Bad: Hardcoded secrets
public class EmailService
{
    private const string ApiKey = "sk_live_abc123xyz";
    private const string SmtpPassword = "MyP@ssw0rd";
}

// Good: Use configuration and User Secrets (development)
public class EmailService
{
    private readonly EmailSettings _settings;

    public EmailService(IOptions<EmailSettings> settings)
    {
        _settings = settings.Value;
    }
}

// appsettings.json (for non-secrets)
{
  "EmailSettings": {
    "SmtpHost": "smtp.example.com",
    "SmtpPort": 587
  }
}

// User secrets (development) or Azure Key Vault (production)
// dotnet user-secrets set "EmailSettings:ApiKey" "sk_live_abc123xyz"
```

## Maintenance Checklist

### Weekly
- [ ] Review TODO/FIXME comments
- [ ] Check CI/CD build warnings
- [ ] Review PR code quality comments

### Monthly
- [ ] Run `dotnet list package --vulnerable`
- [ ] Run `dotnet list package --outdated`
- [ ] Review and update deprecated API usage
- [ ] Check .NET SDK version for updates

### Quarterly
- [ ] Full codebase analysis with SonarQube
- [ ] Major dependency updates
- [ ] .NET version upgrade planning
- [ ] Architecture review session

## Resources

**Official Documentation:**
- [.NET Code Quality Rules](https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/quality-rules/)
- [.NET Security Best Practices](https://learn.microsoft.com/en-us/dotnet/standard/security/secure-coding-guidelines)
- [EF Core Performance](https://learn.microsoft.com/en-us/ef/core/performance/)

**Tools:**
- [Roslyn Analyzers](https://github.com/dotnet/roslyn-analyzers)
- [StyleCop Analyzers](https://github.com/DotNetAnalyzers/StyleCopAnalyzers)
- [SonarQube for .NET](https://www.sonarsource.com/products/sonarqube/)
