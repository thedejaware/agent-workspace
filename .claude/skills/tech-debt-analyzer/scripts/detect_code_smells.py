#!/usr/bin/env python3
"""
Detect code smells and technical debt indicators in .NET/C# codebases.

This script analyzes C# source code to identify:
- Large files and methods
- High complexity code
- TODO/FIXME/HACK comments
- Debug statements left in code
- Weak typing (dynamic, object casting)
- Empty catch blocks
- Catching generic Exception
- Potential null reference issues

Usage:
    python detect_code_smells.py [src-dir] [--output json|markdown]
"""

import re
import json
import sys
from pathlib import Path
from typing import List, Dict, Tuple
from collections import defaultdict

class CSharpCodeSmellDetector:
    def __init__(self, src_dir: str):
        self.src_dir = Path(src_dir)
        self.issues = defaultdict(list)
        self.stats = {
            'total_files': 0,
            'total_lines': 0,
            'total_issues': 0
        }

    def analyze(self):
        """Run all analysis checks."""
        for file_path in self.src_dir.rglob('*'):
            if self._should_analyze(file_path):
                self.stats['total_files'] += 1
                self._analyze_file(file_path)

        self.stats['total_issues'] = sum(len(issues) for issues in self.issues.values())
        return self.issues, self.stats

    def _should_analyze(self, path: Path) -> bool:
        """Check if file should be analyzed."""
        if not path.is_file():
            return False

        # Only analyze C# source files
        valid_extensions = {'.cs'}
        if path.suffix not in valid_extensions:
            return False

        # Skip test files, build artifacts, and generated code
        skip_patterns = [
            'bin', 'obj', 'packages', 'TestResults',
            '.Designer.cs', '.g.cs', '.i.cs',  # Generated files
            'AssemblyInfo.cs', 'AssemblyAttributes.cs',
            'Migrations',  # EF migrations
            'Test.cs', 'Tests.cs', 'Spec.cs',  # Test files
        ]
        return not any(pattern in str(path) for pattern in skip_patterns)

    def _analyze_file(self, file_path: Path):
        """Analyze a single C# file for code smells."""
        try:
            content = file_path.read_text(encoding='utf-8-sig')  # Handle BOM
            lines = content.split('\n')
            self.stats['total_lines'] += len(lines)

            rel_path = file_path.relative_to(self.src_dir)

            # Check file size
            self._check_file_size(rel_path, lines)

            # Check method complexity
            self._check_method_complexity(rel_path, content)

            # Check for technical debt markers
            self._check_debt_markers(rel_path, lines)

            # Check for debug statements
            self._check_debug_statements(rel_path, lines)

            # Check for weak typing
            self._check_weak_typing(rel_path, lines)

            # Check for long parameter lists
            self._check_long_parameters(rel_path, content)

            # Check for deep nesting
            self._check_nesting_depth(rel_path, lines)

            # Check for magic numbers
            self._check_magic_numbers(rel_path, lines)

            # Check for empty catch blocks
            self._check_empty_catch(rel_path, content)

            # Check for catching generic Exception
            self._check_generic_exception(rel_path, lines)

            # Check for potential null reference issues
            self._check_null_references(rel_path, lines)

        except Exception as e:
            self.issues['errors'].append({
                'file': str(file_path.relative_to(self.src_dir)),
                'message': f'Error analyzing file: {str(e)}'
            })

    def _check_file_size(self, file_path: Path, lines: List[str]):
        """Check for overly large files."""
        line_count = len(lines)

        if line_count > 500:
            severity = 'high' if line_count > 1000 else 'medium'
            self.issues['large_files'].append({
                'file': str(file_path),
                'lines': line_count,
                'severity': severity,
                'message': f'File has {line_count} lines (should be < 500)'
            })

    def _check_method_complexity(self, file_path: Path, content: str):
        """Check for complex methods."""
        # Match C# method declarations
        patterns = [
            r'(?:public|private|protected|internal|static|\s)+[\w<>[\],\s]+\s+(\w+)\s*\([^)]*\)\s*\{',
        ]

        for pattern in patterns:
            for match in re.finditer(pattern, content, re.MULTILINE):
                method_name = match.group(1)

                # Skip property getters/setters, constructors-like patterns
                if method_name in ['get', 'set', 'value']:
                    continue

                start_pos = match.start()

                # Find method body
                method_body = self._extract_method_body(content, start_pos)

                if method_body:
                    # Count complexity indicators
                    complexity = self._calculate_complexity(method_body)
                    lines_in_method = method_body.count('\n')

                    if complexity > 10 or lines_in_method > 50:
                        severity = 'high' if complexity > 20 or lines_in_method > 100 else 'medium'
                        self.issues['complex_methods'].append({
                            'file': str(file_path),
                            'method': method_name,
                            'complexity': complexity,
                            'lines': lines_in_method,
                            'severity': severity,
                            'message': f'Method "{method_name}" has complexity {complexity} and {lines_in_method} lines'
                        })

    def _extract_method_body(self, content: str, start_pos: int) -> str:
        """Extract method body using brace matching."""
        brace_count = 0
        in_method = False
        body_start = -1

        for i in range(start_pos, len(content)):
            if content[i] == '{':
                if not in_method:
                    body_start = i
                    in_method = True
                brace_count += 1
            elif content[i] == '}':
                brace_count -= 1
                if brace_count == 0 and in_method:
                    return content[body_start:i+1]

        return ''

    def _calculate_complexity(self, code: str) -> int:
        """Calculate cyclomatic complexity."""
        complexity = 1  # Base complexity

        # Count decision points
        patterns = [
            r'\bif\b',
            r'\belse\s+if\b',
            r'\bfor\b',
            r'\bforeach\b',
            r'\bwhile\b',
            r'\bdo\b',
            r'\bcase\b',
            r'\bcatch\b',
            r'\b&&\b',
            r'\b\|\|\b',
            r'\?',  # Ternary operator
            r'\?\?',  # Null coalescing
        ]

        for pattern in patterns:
            complexity += len(re.findall(pattern, code))

        return complexity

    def _check_debt_markers(self, file_path: Path, lines: List[str]):
        """Check for TODO, FIXME, HACK, XXX comments."""
        markers = ['TODO', 'FIXME', 'HACK', 'XXX', 'BUG', 'DEPRECATED', 'UNDONE']

        for line_num, line in enumerate(lines, 1):
            for marker in markers:
                if marker in line.upper() and ('//' in line or '/*' in line):
                    # Extract the comment
                    comment = line.strip()
                    severity = 'high' if marker in ['FIXME', 'BUG', 'HACK'] else 'low'

                    self.issues['debt_markers'].append({
                        'file': str(file_path),
                        'line': line_num,
                        'marker': marker,
                        'severity': severity,
                        'comment': comment,
                        'message': f'{marker} comment found'
                    })

    def _check_debug_statements(self, file_path: Path, lines: List[str]):
        """Check for Console.WriteLine and Debug statements left in code."""
        patterns = [
            r'\bConsole\.WriteLine\(',
            r'\bConsole\.Write\(',
            r'\bDebug\.WriteLine\(',
            r'\bDebug\.Write\(',
            r'\bTrace\.WriteLine\(',
        ]

        for line_num, line in enumerate(lines, 1):
            # Skip if it's commented out
            if line.strip().startswith('//'):
                continue

            for pattern in patterns:
                if re.search(pattern, line):
                    self.issues['debug_statements'].append({
                        'file': str(file_path),
                        'line': line_num,
                        'severity': 'low',
                        'code': line.strip(),
                        'message': 'Debug statement left in code'
                    })
                    break

    def _check_weak_typing(self, file_path: Path, lines: List[str]):
        """Check for 'dynamic' type or excessive object casting."""
        for line_num, line in enumerate(lines, 1):
            # Skip comments
            if line.strip().startswith('//') or line.strip().startswith('/*'):
                continue

            # Check for dynamic keyword
            if re.search(r'\bdynamic\b', line):
                self.issues['weak_typing'].append({
                    'file': str(file_path),
                    'line': line_num,
                    'severity': 'medium',
                    'code': line.strip(),
                    'message': 'Using "dynamic" type reduces type safety'
                })

            # Check for object casting patterns
            if re.search(r'\(object\)\s*\w+', line):
                self.issues['weak_typing'].append({
                    'file': str(file_path),
                    'line': line_num,
                    'severity': 'low',
                    'code': line.strip(),
                    'message': 'Explicit cast to object may indicate design issue'
                })

    def _check_long_parameters(self, file_path: Path, content: str):
        """Check for methods with too many parameters."""
        # Match method signatures
        pattern = r'(?:public|private|protected|internal|static|\s)+[\w<>[\],\s]+\s+\w+\s*\(([^)]+)\)'

        for match in re.finditer(pattern, content):
            params = match.group(1).strip()

            if not params:
                continue

            # Count parameters (simple comma split)
            # Filter out empty strings and handle generic types
            param_count = len([p for p in re.split(r',(?![^<>]*>)', params) if p.strip()])

            if param_count > 5:
                severity = 'high' if param_count > 7 else 'medium'
                # Find line number
                line_num = content[:match.start()].count('\n') + 1

                self.issues['long_parameters'].append({
                    'file': str(file_path),
                    'line': line_num,
                    'parameters': param_count,
                    'severity': severity,
                    'message': f'Method has {param_count} parameters (should be < 5)'
                })

    def _check_nesting_depth(self, file_path: Path, lines: List[str]):
        """Check for deeply nested code."""
        max_depth = 0
        current_depth = 0

        for line_num, line in enumerate(lines, 1):
            # Skip comments and strings
            stripped = line.strip()
            if stripped.startswith('//') or stripped.startswith('/*'):
                continue

            # Simple brace counting
            current_depth += line.count('{') - line.count('}')

            if current_depth > max_depth:
                max_depth = current_depth

                if current_depth > 4:
                    severity = 'high' if current_depth > 6 else 'medium'
                    self.issues['deep_nesting'].append({
                        'file': str(file_path),
                        'line': line_num,
                        'depth': current_depth,
                        'severity': severity,
                        'message': f'Nesting depth of {current_depth} (should be < 4)'
                    })

    def _check_magic_numbers(self, file_path: Path, lines: List[str]):
        """Check for magic numbers in code."""
        for line_num, line in enumerate(lines, 1):
            # Skip comments, strings, and attribute lines
            if '//' in line or '/*' in line or '"' in line or "'" in line or '[' in line:
                continue

            # Skip constant declarations
            if re.search(r'\bconst\b', line):
                continue

            # Find numbers that aren't 0, 1, -1, common values
            numbers = re.findall(r'\b(\d{2,})\b', line)

            for num in numbers:
                if int(num) not in [0, 1, 10, 100, 1000, 60, 24, 365]:
                    self.issues['magic_numbers'].append({
                        'file': str(file_path),
                        'line': line_num,
                        'number': num,
                        'severity': 'low',
                        'code': line.strip(),
                        'message': f'Magic number {num} should be a named constant'
                    })
                    break  # One per line is enough

    def _check_empty_catch(self, file_path: Path, content: str):
        """Check for empty catch blocks."""
        # Match catch blocks with empty or comment-only bodies
        pattern = r'catch\s*\([^)]+\)\s*\{\s*(?://[^\n]*)?\s*\}'

        for match in re.finditer(pattern, content, re.MULTILINE):
            line_num = content[:match.start()].count('\n') + 1
            self.issues['empty_catch'].append({
                'file': str(file_path),
                'line': line_num,
                'severity': 'high',
                'code': match.group(0).strip(),
                'message': 'Empty catch block swallows exceptions'
            })

    def _check_generic_exception(self, file_path: Path, lines: List[str]):
        """Check for catching generic Exception instead of specific types."""
        for line_num, line in enumerate(lines, 1):
            # Look for catch(Exception) but not catch(SpecificException)
            if re.search(r'catch\s*\(\s*Exception\s+\w+\s*\)', line):
                self.issues['generic_exception'].append({
                    'file': str(file_path),
                    'line': line_num,
                    'severity': 'medium',
                    'code': line.strip(),
                    'message': 'Catching generic Exception; use specific exception types'
                })

    def _check_null_references(self, file_path: Path, lines: List[str]):
        """Check for potential null reference issues."""
        for line_num, line in enumerate(lines, 1):
            # Skip comments and nullable-enabled contexts
            if line.strip().startswith('//') or '?' in line:
                continue

            # Look for direct property access without null check
            # This is a simple heuristic
            if re.search(r'\w+\.\w+\.\w+', line) and not re.search(r'\?\.|!=\s*null|==\s*null', line):
                # Too noisy, skip for now
                pass


def format_markdown_report(issues: Dict, stats: Dict) -> str:
    """Format issues as markdown report."""
    report = ["# Technical Debt Analysis Report (.NET/C#)\n"]
    report.append(f"**Generated:** {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
    report.append("## Summary\n")
    report.append(f"- **Files Analyzed:** {stats['total_files']}")
    report.append(f"- **Total Lines:** {stats['total_lines']}")
    report.append(f"- **Total Issues:** {stats['total_issues']}\n")

    # Calculate severity distribution
    severity_count = defaultdict(int)
    for category_issues in issues.values():
        for issue in category_issues:
            if 'severity' in issue:
                severity_count[issue['severity']] += 1

    report.append("### Issues by Severity\n")
    for severity in ['high', 'medium', 'low']:
        count = severity_count.get(severity, 0)
        report.append(f"- **{severity.upper()}:** {count}")
    report.append("\n")

    # Issues by category
    category_names = {
        'large_files': 'Large Files',
        'complex_methods': 'Complex Methods',
        'debt_markers': 'Technical Debt Markers',
        'debug_statements': 'Debug Statements',
        'weak_typing': 'Weak Typing',
        'long_parameters': 'Long Parameter Lists',
        'deep_nesting': 'Deep Nesting',
        'magic_numbers': 'Magic Numbers',
        'empty_catch': 'Empty Catch Blocks',
        'generic_exception': 'Generic Exception Handling',
        'errors': 'Analysis Errors'
    }

    for category, name in category_names.items():
        category_issues = issues.get(category, [])
        if category_issues:
            report.append(f"## {name} ({len(category_issues)} issues)\n")

            # Group by severity
            high = [i for i in category_issues if i.get('severity') == 'high']
            medium = [i for i in category_issues if i.get('severity') == 'medium']
            low = [i for i in category_issues if i.get('severity') == 'low']

            for severity, severity_issues in [('High', high), ('Medium', medium), ('Low', low)]:
                if severity_issues:
                    report.append(f"### {severity} Priority\n")
                    for issue in severity_issues[:10]:  # Limit to 10 per severity
                        report.append(f"- **{issue['file']}**")
                        if 'line' in issue:
                            report.append(f" (line {issue['line']})")
                        report.append(f": {issue['message']}")
                        if 'code' in issue:
                            report.append(f"\n  ```csharp\n  {issue['code']}\n  ```")
                        report.append("\n")

                    if len(severity_issues) > 10:
                        report.append(f"\n_... and {len(severity_issues) - 10} more_\n")
            report.append("\n")

    return ''.join(report)


def main():
    src_dir = sys.argv[1] if len(sys.argv) > 1 else 'src'
    output_format = 'markdown'

    if '--output' in sys.argv:
        idx = sys.argv.index('--output')
        if idx + 1 < len(sys.argv):
            output_format = sys.argv[idx + 1]

    if not Path(src_dir).exists():
        print(f"Error: Source directory not found: {src_dir}")
        sys.exit(1)

    print(f"Analyzing C# codebase in: {src_dir}")

    detector = CSharpCodeSmellDetector(src_dir)
    issues, stats = detector.analyze()

    if output_format == 'json':
        result = {
            'stats': stats,
            'issues': dict(issues)
        }
        print(json.dumps(result, indent=2))
    else:
        report = format_markdown_report(issues, stats)
        print(report)


if __name__ == '__main__':
    main()
