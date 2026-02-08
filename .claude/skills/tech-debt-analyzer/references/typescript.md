# TypeScript Technical Debt Reference

## Overview

This reference provides TypeScript-specific guidance for identifying, analyzing, and addressing technical debt in TypeScript codebases.

## Automated Analysis Tools

### Built-in Tools

**Type Checking:**
```bash
# Type check without emitting files
tsc --noEmit

# Type check with strict mode
tsc --noEmit --strict

# Watch mode
tsc --noEmit --watch
```

**Dependency Analysis:**
```bash
# Check for security vulnerabilities
npm audit

# Check for outdated packages
npm outdated

# Check for unused dependencies
npx depcheck

# Check type coverage
npx type-coverage
```

### Recommended Third-Party Tools (Optional)

These tools enhance analysis capabilities but are **not required**. Install based on your project needs:

**Code Quality (Highly Recommended):**
- **ESLint + @typescript-eslint** - Linting for TypeScript
  ```bash
  npm install --save-dev eslint @typescript-eslint/parser @typescript-eslint/eslint-plugin
  ```
- **Prettier** - Code formatting
  ```bash
  npm install --save-dev prettier
  ```

**TypeScript-Specific Analysis (Optional):**
- **ts-prune** - Find unused exports
  ```bash
  npx ts-prune
  ```
- **dpdm** - Detect circular dependencies
  ```bash
  npx dpdm src/index.ts
  ```

**Type Safety Measurement (Optional):**
- **type-coverage** - Measure type coverage
  ```bash
  npx type-coverage
  ```
- **tsd** - Test TypeScript type definitions
- **ts-expect-error** - Test error cases

**Security (npm audit is built-in, others optional):**
- **npm audit** - Security vulnerability scanning (always available)
- **Snyk** - Advanced security scanning
- **socket.dev** - Supply chain security

**Test Coverage:**
- **Jest** - Testing with TypeScript support
- **Vitest** - Fast unit test framework
- **nyc/Istanbul** - Code coverage

**Note**: The skill works with built-in TypeScript compiler (`tsc --noEmit`) and npm tools. These are optional enhancements.

## Common TypeScript Code Smells

### 1. Using `any` Type

```typescript
// Bad: Loses all type safety
function processData(data: any): any {
    return data.value.toString(); // No type checking!
}

// Good: Use proper types
interface DataModel {
    value: number;
}

function processData(data: DataModel): string {
    return data.value.toString();
}

// Better: Use generics for flexible types
function processData<T extends { value: number }>(data: T): string {
    return data.value.toString();
}

// If you really don't know the type, use unknown
function processData(data: unknown): string {
    if (typeof data === 'object' && data !== null && 'value' in data) {
        return String((data as { value: unknown }).value);
    }
    throw new Error('Invalid data');
}
```

### 2. Type Assertions Without Validation

```typescript
// Bad: Unsafe type assertion
function getUser(id: string): User {
    const response = fetch(`/api/users/${id}`);
    return response as User; // No validation!
}

// Good: Validate before asserting
function isUser(obj: unknown): obj is User {
    return (
        typeof obj === 'object' &&
        obj !== null &&
        'id' in obj &&
        'name' in obj &&
        typeof obj.id === 'string' &&
        typeof obj.name === 'string'
    );
}

async function getUser(id: string): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    const data = await response.json();

    if (!isUser(data)) {
        throw new Error('Invalid user data');
    }

    return data;
}

// Better: Use a validation library
import { z } from 'zod';

const UserSchema = z.object({
    id: z.string(),
    name: z.string(),
    email: z.string().email()
});

type User = z.infer<typeof UserSchema>;

async function getUser(id: string): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    const data = await response.json();
    return UserSchema.parse(data); // Validates and throws if invalid
}
```

### 3. Non-null Assertions Without Checks

```typescript
// Bad: Assuming value exists
function getUserName(userId: string): string {
    const user = users.find(u => u.id === userId);
    return user!.name; // Dangerous! What if user is undefined?
}

// Good: Handle null/undefined cases
function getUserName(userId: string): string | null {
    const user = users.find(u => u.id === userId);
    return user?.name ?? null;
}

// Better: Return Result type
type Result<T, E> = { ok: true; value: T } | { ok: false; error: E };

function getUserName(userId: string): Result<string, string> {
    const user = users.find(u => u.id === userId);

    if (!user) {
        return { ok: false, error: 'User not found' };
    }

    return { ok: true, value: user.name };
}
```

### 4. Missing Return Types

```typescript
// Bad: Inferred return type can change unexpectedly
function calculateTotal(items) { // What's the return type?
    return items.reduce((sum, item) => sum + item.price, 0);
}

// Good: Explicit return type
function calculateTotal(items: Item[]): number {
    return items.reduce((sum, item) => sum + item.price, 0);
}

// This prevents accidental changes
function calculateTotal(items: Item[]): number {
    // Later someone changes it:
    // return items.reduce((sum, item) => sum + item.price, "0"); // Error!
    return items.reduce((sum, item) => sum + item.price, 0);
}
```

### 5. Implicit `any` in Generic Constraints

```typescript
// Bad: Generic without constraints
function getValue<T>(obj: T, key: string) {
    return obj[key]; // Error: Element implicitly has 'any' type
}

// Good: Proper constraints
function getValue<T extends Record<string, unknown>>(
    obj: T,
    key: keyof T
): T[keyof T] {
    return obj[key];
}

// Better: Type-safe with inference
function getValue<T, K extends keyof T>(obj: T, key: K): T[K] {
    return obj[key];
}

const user = { id: 1, name: 'Alice' };
const name = getValue(user, 'name'); // Type: string
```

### 6. Using Enums Incorrectly

```typescript
// Bad: Numeric enums can be assigned any number
enum Status {
    Active,
    Inactive,
    Pending
}

const status: Status = 999; // Valid but wrong!

// Good: Use string literal union types
type Status = 'active' | 'inactive' | 'pending';
const status: Status = 'active';
// const invalid: Status = 'invalid'; // Error!

// Or use const enum (erased at runtime)
const enum Status {
    Active = 'active',
    Inactive = 'inactive',
    Pending = 'pending'
}
```

### 7. Not Using Strict Mode

```typescript
// Bad: tsconfig.json without strict mode
{
    "compilerOptions": {
        "target": "ES2020",
        "module": "commonjs"
    }
}

// Good: Enable strict mode
{
    "compilerOptions": {
        "target": "ES2020",
        "module": "ESNext",
        "strict": true,
        "noUncheckedIndexedAccess": true,
        "noImplicitOverride": true,
        "noUnusedLocals": true,
        "noUnusedParameters": true,
        "noImplicitReturns": true,
        "noFallthroughCasesInSwitch": true
    }
}
```

### 8. Type Pollution in Global Scope

```typescript
// Bad: Polluting global namespace
declare global {
    interface Window {
        myApp: any; // Avoid this
    }
}

// Good: Use module augmentation sparingly
declare global {
    interface Window {
        myApp: {
            version: string;
            config: AppConfig;
        };
    }
}

// Better: Avoid global state, use dependency injection
class AppContext {
    constructor(public version: string, public config: AppConfig) {}
}
```

## Dependency Debt Patterns

### TypeScript-Specific Dependencies

**Type Definitions:**
```bash
# Check for missing @types packages
npx typesync

# Install type definitions
npm install --save-dev @types/node @types/react
```

**Common Migration Paths:**

| From | To | Reason |
|------|-----|---------|
| `ts-node` | `tsx` or `ts-node-dev` | Faster, better ES modules support |
| `tslint` | `eslint + @typescript-eslint` | TSLint deprecated |
| `@types/react` (v17) | `@types/react` (v18) | New JSX transform |
| `webpack` | `vite` or `esbuild` | Faster build times |

## Configuration Best Practices

### Strict TypeScript Configuration

**tsconfig.json:**
```json
{
  "compilerOptions": {
    // Language and Environment
    "target": "ES2020",
    "lib": ["ES2020", "DOM", "DOM.Iterable"],
    "module": "ESNext",
    "moduleResolution": "bundler",
    "jsx": "react-jsx",

    // Type Checking - Enable all strict checks
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "allowUnusedLabels": false,
    "allowUnreachableCode": false,
    "noFallthroughCasesInSwitch": true,
    "noImplicitReturns": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "exactOptionalPropertyTypes": true,

    // Emit
    "declaration": true,
    "declarationMap": true,
    "sourceMap": true,
    "removeComments": true,
    "importHelpers": true,

    // Interop Constraints
    "esModuleInterop": true,
    "allowSyntheticDefaultImports": true,
    "forceConsistentCasingInFileNames": true,
    "isolatedModules": true,

    // Skip type checking of declaration files
    "skipLibCheck": true
  },
  "include": ["src/**/*"],
  "exclude": ["node_modules", "dist", "**/*.spec.ts"]
}
```

### ESLint Configuration for TypeScript

**.eslintrc.json:**
```json
{
  "parser": "@typescript-eslint/parser",
  "parserOptions": {
    "ecmaVersion": 2021,
    "sourceType": "module",
    "project": "./tsconfig.json"
  },
  "extends": [
    "eslint:recommended",
    "plugin:@typescript-eslint/recommended",
    "plugin:@typescript-eslint/recommended-requiring-type-checking"
  ],
  "plugins": ["@typescript-eslint"],
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/no-non-null-assertion": "warn",
    "@typescript-eslint/consistent-type-imports": "error",
    "@typescript-eslint/no-floating-promises": "error",
    "@typescript-eslint/await-thenable": "error",
    "complexity": ["error", 10],
    "max-lines": ["error", 500]
  }
}
```

## Architectural Debt Patterns

### Type-Unsafe Domain Models

```typescript
// Bad: Primitive obsession
interface User {
    id: string;
    email: string;
    age: number;
}

function createUser(id: string, email: string, age: number): User {
    return { id, email, age }; // No validation!
}

// Good: Use branded types and validation
type UserId = string & { readonly __brand: 'UserId' };
type Email = string & { readonly __brand: 'Email' };
type Age = number & { readonly __brand: 'Age' };

interface User {
    id: UserId;
    email: Email;
    age: Age;
}

function createUserId(value: string): UserId {
    if (!value) throw new Error('UserId cannot be empty');
    return value as UserId;
}

function createEmail(value: string): Email {
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)) {
        throw new Error('Invalid email');
    }
    return value as Email;
}

function createAge(value: number): Age {
    if (value < 0 || value > 150) {
        throw new Error('Invalid age');
    }
    return value as Age;
}

function createUser(id: string, email: string, age: number): User {
    return {
        id: createUserId(id),
        email: createEmail(email),
        age: createAge(age)
    };
}
```

### Missing Error Types

```typescript
// Bad: Throwing strings or generic errors
async function fetchUser(id: string): Promise<User> {
    const response = await fetch(`/api/users/${id}`);
    if (!response.ok) {
        throw new Error('Failed to fetch user'); // Generic error
    }
    return response.json();
}

// Good: Typed errors
class NotFoundError extends Error {
    constructor(public resource: string, public id: string) {
        super(`${resource} with id ${id} not found`);
        this.name = 'NotFoundError';
    }
}

class NetworkError extends Error {
    constructor(message: string, public statusCode: number) {
        super(message);
        this.name = 'NetworkError';
    }
}

async function fetchUser(id: string): Promise<User> {
    const response = await fetch(`/api/users/${id}`);

    if (response.status === 404) {
        throw new NotFoundError('User', id);
    }

    if (!response.ok) {
        throw new NetworkError('Failed to fetch user', response.status);
    }

    return response.json();
}

// Usage with proper error handling
try {
    const user = await fetchUser('123');
} catch (error) {
    if (error instanceof NotFoundError) {
        console.log('User not found:', error.id);
    } else if (error instanceof NetworkError) {
        console.log('Network error:', error.statusCode);
    } else {
        throw error;
    }
}
```

## Testing Debt

### Type-Safe Testing

```typescript
// Use Jest with TypeScript
import { describe, test, expect } from '@jest/globals';

describe('UserService', () => {
    test('getUser returns correct type', async () => {
        const service = new UserService(mockRepository);
        const user = await service.getUser('123');

        // TypeScript ensures correct types
        expect(user.id).toBe('123');
        expect(user.name).toBe('Alice');
        // expect(user.invalid).toBe('value'); // Type error!
    });

    test('handles errors correctly', async () => {
        const service = new UserService(mockRepository);

        await expect(service.getUser('invalid'))
            .rejects
            .toThrow(NotFoundError);
    });
});
```

### Testing Type Definitions

```typescript
// Use tsd for testing type definitions
import { expectType, expectError } from 'tsd';

// Test correct types
expectType<string>(getValue(obj, 'name'));
expectType<number>(getValue(obj, 'age'));

// Test that invalid usage causes errors
expectError(getValue(obj, 'invalid'));
expectError(getValue(obj, 123));
```

## Performance Optimization

### Avoid Type Computation Overhead

```typescript
// Bad: Complex conditional types that slow compilation
type DeepPartial<T> = T extends object
    ? { [P in keyof T]?: DeepPartial<T[P]> }
    : T;

type VeryComplexType<T> = {
    [K in keyof T]: T[K] extends Array<infer U>
        ? U extends object
            ? Array<DeepPartial<U>>
            : T[K]
        : T[K];
};

// Good: Keep types simple, use utility types
type UserUpdate = Partial<Pick<User, 'name' | 'email'>>;
```

### Tree-Shaking with TypeScript

```typescript
// Good: Use named exports for tree-shaking
export const utilityA = () => { /* ... */ };
export const utilityB = () => { /* ... */ };

// Bad: Default exports harder to tree-shake
export default {
    utilityA,
    utilityB
};
```

## Security Debt

### Type-Safe API Contracts

```typescript
// Use Zod or similar for runtime validation
import { z } from 'zod';

// Define schema
const CreateUserSchema = z.object({
    name: z.string().min(1).max(100),
    email: z.string().email(),
    age: z.number().int().min(0).max(150)
});

type CreateUserInput = z.infer<typeof CreateUserSchema>;

// Validate at API boundary
app.post('/users', async (req, res) => {
    try {
        const input = CreateUserSchema.parse(req.body);
        const user = await createUser(input);
        res.json(user);
    } catch (error) {
        if (error instanceof z.ZodError) {
            res.status(400).json({ errors: error.errors });
        } else {
            throw error;
        }
    }
});
```

### Prevent Prototype Pollution

```typescript
// Bad: Direct object creation from user input
function mergeOptions(userOptions: any) {
    const options = {};
    Object.assign(options, userOptions); // Dangerous!
    return options;
}

// Good: Use known keys only
function mergeOptions(userOptions: Partial<AppOptions>): AppOptions {
    const defaults: AppOptions = {
        theme: 'light',
        language: 'en'
    };

    return {
        theme: userOptions.theme ?? defaults.theme,
        language: userOptions.language ?? defaults.language
    };
}
```

## Maintenance Checklist

### Weekly
- [ ] Run `tsc --noEmit` to check types
- [ ] Review TODO/FIXME comments
- [ ] Check ESLint warnings

### Monthly
- [ ] Run `npx typesync` to check missing type definitions
- [ ] Run `npm audit`
- [ ] Run `npm outdated`
- [ ] Check TypeScript version for updates
- [ ] Run `npx type-coverage` to measure type safety

### Quarterly
- [ ] Update TypeScript to latest version
- [ ] Major dependency updates
- [ ] Framework updates (React, Vue, Angular)
- [ ] Review and update tsconfig.json settings

## Resources

**Official Documentation:**
- [TypeScript Handbook](https://www.typescriptlang.org/docs/handbook/intro.html)
- [TypeScript Deep Dive](https://basarat.gitbook.io/typescript/)
- [Type Challenges](https://github.com/type-challenges/type-challenges)

**Tools:**
- [@typescript-eslint](https://typescript-eslint.io/)
- [ts-prune](https://github.com/nadeesha/ts-prune)
- [type-coverage](https://github.com/plantain-00/type-coverage)
- [Zod](https://zod.dev/) - Runtime type validation
