# JavaScript Technical Debt Reference

## Overview

This reference provides JavaScript-specific guidance for identifying, analyzing, and addressing technical debt in JavaScript codebases.

## Automated Analysis Tools

### Built-in npm Tools

**Dependency Analysis:**
```bash
# Check for security vulnerabilities
npm audit

# Check for outdated packages
npm outdated

# Fix vulnerabilities automatically
npm audit fix

# Check for unused dependencies
npx depcheck

# Check for available updates
npx npm-check-updates
```

### Recommended Third-Party Tools (Optional)

These tools enhance analysis capabilities but are **not required**. Install based on your project needs:

**Code Quality (Highly Recommended):**
- **ESLint** - Linting and code quality
  ```bash
  npm install --save-dev eslint
  npx eslint --init
  ```
- **Prettier** - Code formatting
  ```bash
  npm install --save-dev prettier
  ```

**Alternative Linters (Choose one):**
- **JSHint** - Alternative linter
- **StandardJS** - Opinionated code style (zero config)

**Complexity Analysis (Optional):**
- **complexity-report** - Cyclomatic complexity analysis
- **plato** - JavaScript source code visualization
- **es6-plato** - ES6+ compatible Plato

**Security (npm audit is built-in, others optional):**
- **npm audit** - Built-in security checking (always available)
- **Snyk** - Advanced dependency security scanning
- **RetireJS** - Detect vulnerable JavaScript libraries

**Test Coverage:**
- **Istanbul/nyc** - Code coverage
- **Jest** - Testing framework with built-in coverage
- **Codecov** - Coverage visualization (SaaS)

**Note**: The skill works with built-in npm tools (`npm audit`, `npm outdated`). These are optional enhancements.

## Common JavaScript Code Smells

### 1. Callback Hell

```javascript
// Bad: Deeply nested callbacks
function getUserData(userId, callback) {
    getUser(userId, function(user) {
        getProfile(user.id, function(profile) {
            getPosts(profile.id, function(posts) {
                getComments(posts[0].id, function(comments) {
                    callback({ user, profile, posts, comments });
                });
            });
        });
    });
}

// Good: Use Promises
function getUserData(userId) {
    return getUser(userId)
        .then(user => getProfile(user.id))
        .then(profile => getPosts(profile.id))
        .then(posts => getComments(posts[0].id))
        .then(comments => ({ user, profile, posts, comments }));
}

// Better: Use async/await
async function getUserData(userId) {
    const user = await getUser(userId);
    const profile = await getProfile(user.id);
    const posts = await getPosts(profile.id);
    const comments = await getComments(posts[0].id);
    return { user, profile, posts, comments };
}
```

### 2. Var Usage Instead of Let/Const

```javascript
// Bad: Using var (function-scoped, hoisting issues)
for (var i = 0; i < 5; i++) {
    setTimeout(function() {
        console.log(i); // Always prints 5!
    }, 100);
}

// Good: Use let (block-scoped)
for (let i = 0; i < 5; i++) {
    setTimeout(function() {
        console.log(i); // Prints 0, 1, 2, 3, 4
    }, 100);
}

// Best: Use const for values that don't change
const MAX_RETRIES = 3;
const users = ['Alice', 'Bob', 'Charlie'];
```

### 3. Loose Equality (==) Instead of Strict (===)

```javascript
// Bad: Loose equality causes unexpected coercion
if (value == null) { } // Matches both null and undefined
if (0 == false) { }     // true
if ('' == false) { }    // true
if ('0' == 0) { }       // true

// Good: Use strict equality
if (value === null) { }
if (value === 0) { }
if (value === false) { }
```

### 4. Not Handling Promises Properly

```javascript
// Bad: Unhandled promise rejection
function fetchData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => console.log(data));
    // No error handling!
}

// Good: Handle errors
function fetchData() {
    fetch('/api/data')
        .then(response => response.json())
        .then(data => console.log(data))
        .catch(error => console.error('Failed to fetch:', error));
}

// Better: Use async/await with try/catch
async function fetchData() {
    try {
        const response = await fetch('/api/data');
        const data = await response.json();
        console.log(data);
    } catch (error) {
        console.error('Failed to fetch:', error);
    }
}
```

### 5. Modifying Parameters/Arguments

```javascript
// Bad: Mutating parameters
function addItem(array, item) {
    array.push(item); // Mutates original array
    return array;
}

// Good: Return new array
function addItem(array, item) {
    return [...array, item];
}

// Bad: Modifying object parameters
function updateUser(user, updates) {
    user.name = updates.name; // Mutates original object
    return user;
}

// Good: Return new object
function updateUser(user, updates) {
    return { ...user, ...updates };
}
```

### 6. Global Variables

```javascript
// Bad: Global variables
var userData = null;
var config = {};

function initApp() {
    userData = fetchUserData();
    config = loadConfig();
}

// Good: Module pattern or ES6 modules
// user-service.js
let userData = null;

export function initUserData() {
    userData = fetchUserData();
}

export function getUserData() {
    return userData;
}
```

### 7. Not Using Array Methods

```javascript
// Bad: Manual loops
const numbers = [1, 2, 3, 4, 5];
const doubled = [];
for (let i = 0; i < numbers.length; i++) {
    doubled.push(numbers[i] * 2);
}

// Good: Use array methods
const doubled = numbers.map(n => n * 2);

// Bad: Finding items manually
let user = null;
for (let i = 0; i < users.length; i++) {
    if (users[i].id === targetId) {
        user = users[i];
        break;
    }
}

// Good: Use find()
const user = users.find(u => u.id === targetId);
```

### 8. Not Using Template Literals

```javascript
// Bad: String concatenation
const greeting = 'Hello, ' + user.name + '! You have ' +
                 user.messages + ' new messages.';

// Good: Template literals
const greeting = `Hello, ${user.name}! You have ${user.messages} new messages.`;

// Bad: Multiline strings with concatenation
const html = '<div>' +
             '  <h1>' + title + '</h1>' +
             '  <p>' + content + '</p>' +
             '</div>';

// Good: Template literals
const html = `
  <div>
    <h1>${title}</h1>
    <p>${content}</p>
  </div>
`;
```

## Dependency Debt Patterns

### Deprecated npm Packages

Common packages to migrate away from:

| Deprecated Package | Recommended Alternative | Reason |
|-------------------|------------------------|---------|
| `request` | `axios`, `node-fetch`, or native `fetch` | Deprecated, no longer maintained |
| `moment` | `date-fns`, `dayjs`, or native `Intl` | Large bundle size, maintenance mode |
| `node-uuid` | `uuid` | Official package renamed |
| `gulp` | `npm scripts`, `webpack`, or `vite` | Modern build tools more capable |
| `bower` | `npm` or `yarn` | Deprecated package manager |

### Large Bundle Sizes

**Identify large dependencies:**
```bash
# Analyze bundle size
npx webpack-bundle-analyzer

# Check package size before installing
npx package-phobia <package-name>

# Alternative lightweight packages
npm install date-fns      # Instead of moment (6x smaller)
npm install lodash-es     # Tree-shakeable lodash
npm install preact        # Lightweight React alternative (3KB)
```

### Multiple Versions of Same Package

```bash
# Check for duplicate packages
npm ls <package-name>

# Deduplicate packages
npm dedupe

# Or use yarn
yarn dedupe
```

## Configuration Best Practices

### ESLint Configuration

**.eslintrc.json:**
```json
{
  "env": {
    "browser": true,
    "es2021": true,
    "node": true
  },
  "extends": [
    "eslint:recommended"
  ],
  "parserOptions": {
    "ecmaVersion": 2021,
    "sourceType": "module"
  },
  "rules": {
    "no-var": "error",
    "prefer-const": "error",
    "prefer-arrow-callback": "warn",
    "no-console": "warn",
    "eqeqeq": ["error", "always"],
    "complexity": ["error", 10],
    "max-lines": ["error", 500],
    "max-params": ["error", 5],
    "max-depth": ["error", 4],
    "no-unused-vars": "error",
    "no-magic-numbers": ["warn", { "ignore": [0, 1, -1] }]
  }
}
```

### Prettier Configuration

**.prettierrc:**
```json
{
  "semi": true,
  "trailingComma": "es5",
  "singleQuote": true,
  "printWidth": 100,
  "tabWidth": 2,
  "arrowParens": "always"
}
```

### Package.json Scripts

```json
{
  "scripts": {
    "lint": "eslint . --ext .js,.jsx",
    "lint:fix": "eslint . --ext .js,.jsx --fix",
    "format": "prettier --write \"**/*.{js,jsx,json,md}\"",
    "test": "jest",
    "test:coverage": "jest --coverage",
    "audit": "npm audit",
    "audit:fix": "npm audit fix",
    "outdated": "npm outdated",
    "depcheck": "depcheck"
  }
}
```

## Architectural Debt Patterns

### Tight Coupling

```javascript
// Bad: Tight coupling to implementation
class OrderService {
    constructor() {
        this.db = new MySQLDatabase(); // Hard-coded dependency
        this.logger = new FileLogger(); // Hard-coded dependency
    }

    async createOrder(order) {
        await this.db.insert('orders', order);
        this.logger.log('Order created');
    }
}

// Good: Dependency injection
class OrderService {
    constructor(database, logger) {
        this.db = database;
        this.logger = logger;
    }

    async createOrder(order) {
        await this.db.insert('orders', order);
        this.logger.log('Order created');
    }
}

// Usage
const service = new OrderService(
    new MySQLDatabase(),
    new FileLogger()
);
```

### Mixing Business Logic with UI

```javascript
// Bad: Business logic in component
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);

    useEffect(() => {
        // Business logic mixed with UI
        fetch(`/api/users/${userId}`)
            .then(res => res.json())
            .then(data => {
                // Data transformation in component
                data.fullName = `${data.firstName} ${data.lastName}`;
                data.displayAge = `${data.age} years old`;
                setUser(data);
            });
    }, [userId]);

    return <div>{user?.fullName}</div>;
}

// Good: Separate business logic
// services/userService.js
export async function getUserProfile(userId) {
    const response = await fetch(`/api/users/${userId}`);
    const user = await response.json();
    return transformUserData(user);
}

function transformUserData(user) {
    return {
        ...user,
        fullName: `${user.firstName} ${user.lastName}`,
        displayAge: `${user.age} years old`
    };
}

// UserProfile.jsx
function UserProfile({ userId }) {
    const [user, setUser] = useState(null);

    useEffect(() => {
        getUserProfile(userId).then(setUser);
    }, [userId]);

    return <div>{user?.fullName}</div>;
}
```

## Testing Debt

### Missing Test Coverage

```javascript
// Example using Jest
describe('UserService', () => {
    let userService;
    let mockDb;

    beforeEach(() => {
        mockDb = {
            findById: jest.fn(),
            insert: jest.fn()
        };
        userService = new UserService(mockDb);
    });

    test('getUser returns user when found', async () => {
        const mockUser = { id: 1, name: 'Alice' };
        mockDb.findById.mockResolvedValue(mockUser);

        const result = await userService.getUser(1);

        expect(result).toEqual(mockUser);
        expect(mockDb.findById).toHaveBeenCalledWith(1);
    });

    test('getUser throws error when not found', async () => {
        mockDb.findById.mockResolvedValue(null);

        await expect(userService.getUser(1))
            .rejects
            .toThrow('User not found');
    });
});
```

## Performance Optimization

### Unnecessary Re-renders (React)

```javascript
// Bad: Creating new objects/functions on every render
function UserList({ users }) {
    return (
        <div>
            {users.map(user => (
                // New function created on every render!
                <User key={user.id} user={user} onClick={() => handleClick(user.id)} />
            ))}
        </div>
    );
}

// Good: Use useCallback
function UserList({ users }) {
    const handleClick = useCallback((userId) => {
        // Handle click
    }, []);

    return (
        <div>
            {users.map(user => (
                <User key={user.id} user={user} onClick={handleClick} />
            ))}
        </div>
    );
}
```

### Memory Leaks

```javascript
// Bad: Event listener not cleaned up
function MyComponent() {
    useEffect(() => {
        window.addEventListener('resize', handleResize);
        // Missing cleanup!
    }, []);
}

// Good: Clean up in useEffect return
function MyComponent() {
    useEffect(() => {
        window.addEventListener('resize', handleResize);

        return () => {
            window.removeEventListener('resize', handleResize);
        };
    }, []);
}

// Bad: Timer not cleared
function MyComponent() {
    useEffect(() => {
        setInterval(() => {
            console.log('Tick');
        }, 1000);
    }, []);
}

// Good: Clear timer on unmount
function MyComponent() {
    useEffect(() => {
        const timer = setInterval(() => {
            console.log('Tick');
        }, 1000);

        return () => clearInterval(timer);
    }, []);
}
```

### Inefficient Array Operations

```javascript
// Bad: Nested loops (O(n²))
const commonItems = [];
for (const item1 of array1) {
    for (const item2 of array2) {
        if (item1.id === item2.id) {
            commonItems.push(item1);
        }
    }
}

// Good: Use Set (O(n))
const set2 = new Set(array2.map(item => item.id));
const commonItems = array1.filter(item => set2.has(item.id));
```

## Security Debt

### XSS Vulnerabilities

```javascript
// Bad: Directly inserting user input
function displayMessage(message) {
    document.getElementById('output').innerHTML = message; // XSS risk!
}

// Good: Use textContent or sanitize
function displayMessage(message) {
    document.getElementById('output').textContent = message;
}

// If you need HTML, use a sanitizer
import DOMPurify from 'dompurify';

function displayMessage(message) {
    const clean = DOMPurify.sanitize(message);
    document.getElementById('output').innerHTML = clean;
}
```

### Exposed Secrets

```javascript
// Bad: API keys in code
const API_KEY = 'sk_live_abc123xyz789';
const apiUrl = `https://api.example.com?key=${API_KEY}`;

// Good: Use environment variables
const API_KEY = process.env.REACT_APP_API_KEY;

// .env file (not committed to git)
// REACT_APP_API_KEY=sk_live_abc123xyz789

// .gitignore
// .env
// .env.local
```

### Insecure Direct Object References

```javascript
// Bad: Using user input directly
app.get('/api/file/:filename', (req, res) => {
    const file = fs.readFileSync(`./uploads/${req.params.filename}`);
    res.send(file);
    // Can access: /api/file/../../../etc/passwd
});

// Good: Validate and sanitize
app.get('/api/file/:filename', (req, res) => {
    const filename = path.basename(req.params.filename); // Remove path
    const fullPath = path.join('./uploads', filename);

    // Ensure path is within uploads directory
    if (!fullPath.startsWith(path.resolve('./uploads'))) {
        return res.status(403).send('Access denied');
    }

    const file = fs.readFileSync(fullPath);
    res.send(file);
});
```

## Maintenance Checklist

### Weekly
- [ ] Review TODO/FIXME comments
- [ ] Check CI/CD lint warnings
- [ ] Review bundle size changes

### Monthly
- [ ] Run `npm audit`
- [ ] Run `npm outdated`
- [ ] Check for deprecated dependencies
- [ ] Update Node.js version if needed

### Quarterly
- [ ] Full codebase lint analysis
- [ ] Major dependency updates
- [ ] Framework version updates (React, Vue, Angular)
- [ ] Bundle size optimization review

## Resources

**Official Documentation:**
- [MDN Web Docs - JavaScript](https://developer.mozilla.org/en-US/docs/Web/JavaScript)
- [Node.js Best Practices](https://github.com/goldbergyoni/nodebestpractices)
- [JavaScript Clean Code](https://github.com/ryanmcdermott/clean-code-javascript)

**Tools:**
- [ESLint](https://eslint.org/)
- [Prettier](https://prettier.io/)
- [Jest](https://jestjs.io/)
- [Webpack Bundle Analyzer](https://github.com/webpack-contrib/webpack-bundle-analyzer)
