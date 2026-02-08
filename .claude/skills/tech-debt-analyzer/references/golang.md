# Golang Technical Debt Reference

## Overview

This reference provides Go-specific guidance for identifying, analyzing, and addressing technical debt in Go codebases.

## Automated Analysis Tools

### Built-in Go Tools

**Code Analysis:**
```bash
# Vet examines Go source code and reports suspicious constructs
go vet ./...

# Format code
go fmt ./...
gofmt -s -w .  # Simplify code

# Run tests with coverage
go test -cover ./...
go test -coverprofile=coverage.out ./...
go tool cover -html=coverage.out

# Check for race conditions
go test -race ./...

# Build and check for errors
go build ./...
```

**Dependency Management:**
```bash
# Check for updates
go list -u -m all

# Check for vulnerabilities
govulncheck ./...

# Tidy dependencies
go mod tidy

# Verify dependencies
go mod verify

# View dependency graph
go mod graph
```

### Recommended Third-Party Tools (Optional)

These tools enhance analysis capabilities but are **not required**. Install based on your project needs:

**Code Quality (Highly Recommended):**
- **golangci-lint** - Meta-linter running multiple linters (recommended)
  ```bash
  # Install
  go install github.com/golangci/golangci-lint/cmd/golangci-lint@latest

  # Run
  golangci-lint run
  ```
- **staticcheck** - Advanced Go linter
  ```bash
  go install honnef.co/go/tools/cmd/staticcheck@latest
  ```

**Additional Linters (Optional, golangci-lint includes most):**
- **revive** - Fast, configurable linter
- **gosec** - Security-focused linter
- **errcheck** - Check for unchecked errors

**Complexity Analysis (Optional):**
- **gocyclo** - Cyclomatic complexity
- **gocognit** - Cognitive complexity
- **golines** - Line length formatter

**Test Coverage:**
- **go test -cover** - Built-in coverage (always available)
- **go-cover** - Coverage visualization
- **gocov** - Coverage testing tool
- **gotestsum** - Enhanced test output
  ```bash
  go install gotest.tools/gotestsum@latest
  ```

**Note**: The skill works with built-in Go tools (`go vet`, `go test`, `govulncheck`). These are optional enhancements.

## Common Go Code Smells

### 1. Not Handling Errors

```go
// Bad: Ignoring errors
file, _ := os.Open("config.json") // Never do this!
defer file.Close()

data, _ := io.ReadAll(file)
// If Open failed, file is nil and this will panic!

// Good: Handle errors
file, err := os.Open("config.json")
if err != nil {
    return fmt.Errorf("failed to open config: %w", err)
}
defer file.Close()

data, err := io.ReadAll(file)
if err != nil {
    return fmt.Errorf("failed to read config: %w", err)
}
```

### 2. Goroutine Leaks

```go
// Bad: Goroutine never terminates
func fetchData(url string) {
    go func() {
        resp, _ := http.Get(url)
        defer resp.Body.Close()
        // Process response...
        // This goroutine leaks if the request hangs
    }()
}

// Good: Use context with timeout
func fetchData(ctx context.Context, url string) error {
    ctx, cancel := context.WithTimeout(ctx, 5*time.Second)
    defer cancel()

    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return err
    }

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return err
    }
    defer resp.Body.Close()

    // Process response...
    return nil
}
```

### 3. Not Using defer for Cleanup

```go
// Bad: Easy to forget cleanup
func processFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return err
    }

    data, err := io.ReadAll(file)
    if err != nil {
        file.Close() // Have to remember to close
        return err
    }

    file.Close() // Have to remember to close
    return process(data)
}

// Good: Use defer
func processFile(path string) error {
    file, err := os.Open(path)
    if err != nil {
        return err
    }
    defer file.Close() // Always closes, even on error

    data, err := io.ReadAll(file)
    if err != nil {
        return err
    }

    return process(data)
}
```

### 4. Mutex Not Protected by Struct

```go
// Bad: Mutex separate from data it protects
type Counter struct {
    count int
}

var mu sync.Mutex
var counter Counter

func Increment() {
    mu.Lock()
    counter.count++ // Easy to forget the lock
    mu.Unlock()
}

// Good: Embed mutex with data
type Counter struct {
    mu    sync.Mutex
    count int
}

func (c *Counter) Increment() {
    c.mu.Lock()
    defer c.mu.Unlock()
    c.count++
}

func (c *Counter) Value() int {
    c.mu.Lock()
    defer c.mu.Unlock()
    return c.count
}
```

### 5. Not Using Context

```go
// Bad: No way to cancel operation
func fetchUser(id string) (*User, error) {
    resp, err := http.Get("https://api.example.com/users/" + id)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    // ...
}

// Good: Accept context
func fetchUser(ctx context.Context, id string) (*User, error) {
    req, err := http.NewRequestWithContext(
        ctx,
        "GET",
        "https://api.example.com/users/"+id,
        nil,
    )
    if err != nil {
        return nil, err
    }

    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    // ...
}
```

### 6. Not Checking Interface Compliance

```go
// Bad: No compile-time check
type MyWriter struct{}

func (w MyWriter) Write(p []byte) (n int, err error) {
    // Implementation
}

// Good: Compile-time interface check
type MyWriter struct{}

// Ensures MyWriter implements io.Writer at compile time
var _ io.Writer = (*MyWriter)(nil)

func (w *MyWriter) Write(p []byte) (n int, err error) {
    // Implementation
}
```

### 7. Returning Pointers to Loop Variables

```go
// Bad: All pointers point to the same address
var results []*Result
for _, item := range items {
    result := processItem(item)
    results = append(results, &result) // Bug!
}

// Good: Create new variable
var results []*Result
for _, item := range items {
    result := processItem(item)
    r := result // Create copy
    results = append(results, &r)
}

// Or use index
var results []*Result
for i := range items {
    result := processItem(items[i])
    results = append(results, &result)
}
```

### 8. Not Closing HTTP Response Body

```go
// Bad: Resource leak
resp, err := http.Get(url)
if err != nil {
    return err
}
body, _ := io.ReadAll(resp.Body)
// Forgot to close resp.Body!

// Good: Always defer Close
resp, err := http.Get(url)
if err != nil {
    return err
}
defer resp.Body.Close()

body, err := io.ReadAll(resp.Body)
if err != nil {
    return err
}
```

## Dependency Debt Patterns

### Outdated Dependencies

```bash
# Check for outdated modules
go list -u -m all

# Update to latest
go get -u ./...
go mod tidy

# Update specific module
go get -u github.com/gorilla/mux@latest
```

### Vulnerable Dependencies

```bash
# Check for known vulnerabilities
govulncheck ./...

# Update vulnerable dependencies
go get -u github.com/vulnerable/package@latest
go mod tidy
```

### Unused Dependencies

```bash
# Remove unused dependencies
go mod tidy

# Verify all dependencies are used
go mod why -m github.com/some/package
```

## Configuration Best Practices

### golangci-lint Configuration

**.golangci.yml:**
```yaml
run:
  timeout: 5m
  tests: true

linters:
  enable:
    - errcheck       # Check for unchecked errors
    - gocyclo        # Cyclomatic complexity
    - gofmt          # Check formatting
    - goimports      # Check imports
    - gosec          # Security issues
    - gosimple       # Simplify code
    - govet          # Vet examines Go source
    - ineffassign    # Detect ineffectual assignments
    - staticcheck    # Static analysis
    - unused         # Check for unused code
    - misspell       # Spelling mistakes
    - unconvert      # Unnecessary conversions
    - unparam        # Unused function parameters
    - dupl           # Duplicate code
    - goconst        # Repeated strings to constants
    - prealloc       # Slice preallocation

linters-settings:
  gocyclo:
    min-complexity: 10
  govet:
    check-shadowing: true
  dupl:
    threshold: 100
  errcheck:
    check-type-assertions: true
    check-blank: true

issues:
  exclude-use-default: false
  max-issues-per-linter: 0
  max-same-issues: 0
```

### Go Module Best Practices

**go.mod:**
```go
module github.com/username/project

go 1.21 // Always specify Go version

require (
    github.com/gorilla/mux v1.8.1
    github.com/lib/pq v1.10.9
)

// Use replace for local development
// replace github.com/username/library => ../library

// Use exclude for problematic versions
// exclude github.com/broken/module v1.2.3
```

## Architectural Debt Patterns

### Global State

```go
// Bad: Global variables
var db *sql.DB
var cache map[string]interface{}

func init() {
    db = connectDB()
    cache = make(map[string]interface{})
}

func GetUser(id string) (*User, error) {
    // Uses global db
}

// Good: Dependency injection
type UserService struct {
    db    *sql.DB
    cache Cache
}

func NewUserService(db *sql.DB, cache Cache) *UserService {
    return &UserService{
        db:    db,
        cache: cache,
    }
}

func (s *UserService) GetUser(ctx context.Context, id string) (*User, error) {
    // Uses injected dependencies
}
```

### God Objects

```go
// Bad: One struct doing everything
type UserManager struct {
    db     *sql.DB
    cache  Cache
    logger Logger
    mailer Mailer
    // ... 20 more fields
}

func (m *UserManager) CreateUser(...) error { /* ... */ }
func (m *UserManager) SendEmail(...) error { /* ... */ }
func (m *UserManager) ValidatePassword(...) bool { /* ... */ }
func (m *UserManager) LogActivity(...) error { /* ... */ }
// ... 50 more methods

// Good: Separate concerns
type UserService struct {
    repo   UserRepository
    logger Logger
}

type EmailService struct {
    mailer Mailer
    logger Logger
}

type AuthService struct {
    validator PasswordValidator
    logger    Logger
}
```

### Interface Pollution

```go
// Bad: Too many methods in interface
type UserService interface {
    CreateUser(User) error
    UpdateUser(User) error
    DeleteUser(string) error
    GetUser(string) (*User, error)
    ListUsers() ([]*User, error)
    SearchUsers(string) ([]*User, error)
    ValidateUser(User) error
    // ... 20 more methods
}

// Good: Small, focused interfaces
type UserCreator interface {
    CreateUser(ctx context.Context, user User) error
}

type UserRetriever interface {
    GetUser(ctx context.Context, id string) (*User, error)
}

type UserLister interface {
    ListUsers(ctx context.Context) ([]*User, error)
}

// Compose interfaces when needed
type UserManager interface {
    UserCreator
    UserRetriever
    UserLister
}
```

## Testing Debt

### Table-Driven Tests

```go
// Good: Table-driven tests
func TestCalculateTotal(t *testing.T) {
    tests := []struct {
        name     string
        items    []Item
        expected float64
        wantErr  bool
    }{
        {
            name:     "empty items",
            items:    []Item{},
            expected: 0,
            wantErr:  false,
        },
        {
            name: "single item",
            items: []Item{
                {Price: 10.0},
            },
            expected: 10.0,
            wantErr:  false,
        },
        {
            name: "multiple items",
            items: []Item{
                {Price: 10.0},
                {Price: 20.0},
            },
            expected: 30.0,
            wantErr:  false,
        },
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            got, err := CalculateTotal(tt.items)
            if (err != nil) != tt.wantErr {
                t.Errorf("CalculateTotal() error = %v, wantErr %v", err, tt.wantErr)
                return
            }
            if got != tt.expected {
                t.Errorf("CalculateTotal() = %v, want %v", got, tt.expected)
            }
        })
    }
}
```

### Test Helpers

```go
// Create test helpers for common setup
func setupTestDB(t *testing.T) *sql.DB {
    t.Helper()

    db, err := sql.Open("sqlite3", ":memory:")
    if err != nil {
        t.Fatalf("failed to open test db: %v", err)
    }

    t.Cleanup(func() {
        db.Close()
    })

    return db
}

func TestUserService(t *testing.T) {
    db := setupTestDB(t)
    service := NewUserService(db)
    // Test using service...
}
```

## Performance Optimization

### String Building

```go
// Bad: String concatenation in loop
func buildSQL(fields []string) string {
    sql := "SELECT "
    for i, field := range fields {
        if i > 0 {
            sql += ", " // Creates new string each iteration
        }
        sql += field
    }
    sql += " FROM users"
    return sql
}

// Good: Use strings.Builder
func buildSQL(fields []string) string {
    var b strings.Builder
    b.WriteString("SELECT ")
    for i, field := range fields {
        if i > 0 {
            b.WriteString(", ")
        }
        b.WriteString(field)
    }
    b.WriteString(" FROM users")
    return b.String()
}
```

### Slice Preallocation

```go
// Bad: Slice grows repeatedly
func processItems(input []int) []int {
    var result []int
    for _, item := range input {
        result = append(result, item*2) // May reallocate multiple times
    }
    return result
}

// Good: Preallocate capacity
func processItems(input []int) []int {
    result := make([]int, 0, len(input))
    for _, item := range input {
        result = append(result, item*2)
    }
    return result
}
```

### Avoid Unnecessary Allocations

```go
// Bad: Creates new slice on every call
func getConfig() []string {
    return []string{"opt1", "opt2", "opt3"}
}

// Good: Return existing slice
var defaultConfig = []string{"opt1", "opt2", "opt3"}

func getConfig() []string {
    return defaultConfig
}

// Or use sync.Pool for frequently allocated objects
var bufferPool = sync.Pool{
    New: func() interface{} {
        return new(bytes.Buffer)
    },
}

func processData(data []byte) ([]byte, error) {
    buf := bufferPool.Get().(*bytes.Buffer)
    defer bufferPool.Put(buf)
    buf.Reset()

    // Use buffer...
    return buf.Bytes(), nil
}
```

## Security Debt

### SQL Injection Prevention

```go
// Bad: String concatenation
func getUser(db *sql.DB, username string) (*User, error) {
    query := "SELECT * FROM users WHERE username = '" + username + "'"
    // SQL injection vulnerability!
}

// Good: Use parameterized queries
func getUser(db *sql.DB, username string) (*User, error) {
    query := "SELECT * FROM users WHERE username = ?"
    row := db.QueryRow(query, username)
    // ...
}
```

### Input Validation

```go
// Good: Validate all inputs
func CreateUser(w http.ResponseWriter, r *http.Request) {
    var input struct {
        Username string `json:"username"`
        Email    string `json:"email"`
        Age      int    `json:"age"`
    }

    if err := json.NewDecoder(r.Body).Decode(&input); err != nil {
        http.Error(w, "Invalid JSON", http.StatusBadRequest)
        return
    }

    // Validate input
    if len(input.Username) < 3 || len(input.Username) > 50 {
        http.Error(w, "Username must be 3-50 characters", http.StatusBadRequest)
        return
    }

    if !isValidEmail(input.Email) {
        http.Error(w, "Invalid email", http.StatusBadRequest)
        return
    }

    if input.Age < 0 || input.Age > 150 {
        http.Error(w, "Invalid age", http.StatusBadRequest)
        return
    }

    // Proceed with valid input...
}
```

### Secrets Management

```go
// Bad: Hardcoded secrets
const (
    APIKey    = "sk_live_abc123xyz"
    DBPassword = "MyP@ssw0rd"
)

// Good: Environment variables
func loadConfig() (*Config, error) {
    apiKey := os.Getenv("API_KEY")
    if apiKey == "" {
        return nil, errors.New("API_KEY not set")
    }

    dbPassword := os.Getenv("DB_PASSWORD")
    if dbPassword == "" {
        return nil, errors.New("DB_PASSWORD not set")
    }

    return &Config{
        APIKey:     apiKey,
        DBPassword: dbPassword,
    }, nil
}
```

## Maintenance Checklist

### Weekly
- [ ] Run `go vet ./...`
- [ ] Run `golangci-lint run`
- [ ] Check for TODO/FIXME comments

### Monthly
- [ ] Run `govulncheck ./...`
- [ ] Run `go list -u -m all` to check for updates
- [ ] Review test coverage: `go test -cover ./...`
- [ ] Check for goroutine leaks

### Quarterly
- [ ] Update Go version
- [ ] Major dependency updates
- [ ] Run `go mod tidy` and commit
- [ ] Performance profiling review
- [ ] Security audit

## Resources

**Official Documentation:**
- [Effective Go](https://go.dev/doc/effective_go)
- [Go Code Review Comments](https://github.com/golang/go/wiki/CodeReviewComments)
- [Go Security Best Practices](https://go.dev/security/best-practices)

**Tools:**
- [golangci-lint](https://golangci-lint.run/)
- [staticcheck](https://staticcheck.io/)
- [govulncheck](https://go.dev/security/vulncheck)
- [go-callvis](https://github.com/ofabry/go-callvis) - Visualize call graph
