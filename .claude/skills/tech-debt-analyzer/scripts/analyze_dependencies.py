#!/usr/bin/env python3
"""
Analyze .NET project dependencies for technical debt indicators.

This script examines .csproj files to identify:
- Outdated dependencies
- Deprecated NuGet packages
- Framework targeting issues
- Duplicate functionality
- Version constraint problems

Usage:
    python analyze_dependencies.py [*.csproj-path]
"""

import xml.etree.ElementTree as ET
import json
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, List

class DotNetDependencyAnalyzer:
    def __init__(self, csproj_path: str):
        self.csproj_path = Path(csproj_path)
        self.issues = {
            'outdated': [],
            'framework_issues': [],
            'duplicate_functionality': [],
            'warnings': [],
            'configuration': []
        }

    def analyze(self):
        """Analyze .csproj file for dependency issues."""
        if not self.csproj_path.exists():
            print(f"Error: {self.csproj_path} not found")
            return None

        try:
            tree = ET.parse(self.csproj_path)
            root = tree.getroot()

            # Extract project information
            project_info = self._extract_project_info(root)

            # Get package references
            package_refs = self._get_package_references(root)

            # Analyze framework targeting
            self._check_framework_target(root)

            # Check for nullable reference types
            self._check_nullable_configuration(root)

            # Check for code analysis settings
            self._check_code_analysis(root)

            # Check for deprecated packages
            self._check_deprecated_packages(package_refs)

            # Check for duplicate functionality
            self._check_duplicate_functionality(package_refs)

            # Check for version constraints
            self._check_version_constraints(package_refs)

            return {
                'project_name': project_info['name'],
                'target_framework': project_info['target_framework'],
                'sdk_style': project_info['sdk_style'],
                'total_package_references': len(package_refs),
                'issues': self.issues,
                'summary': self._generate_summary()
            }

        except ET.ParseError as e:
            print(f"Error parsing .csproj file: {e}")
            return None
        except Exception as e:
            print(f"Unexpected error: {e}")
            return None

    def _extract_project_info(self, root: ET.Element) -> Dict:
        """Extract basic project information."""
        info = {
            'name': self.csproj_path.stem,
            'target_framework': 'unknown',
            'sdk_style': 'Sdk' in root.attrib
        }

        # Find TargetFramework or TargetFrameworks
        for prop_group in root.findall('.//PropertyGroup'):
            tf = prop_group.find('TargetFramework')
            if tf is not None and tf.text:
                info['target_framework'] = tf.text
                break

            tfs = prop_group.find('TargetFrameworks')
            if tfs is not None and tfs.text:
                info['target_framework'] = tfs.text.split(';')[0]  # Take first
                break

        return info

    def _get_package_references(self, root: ET.Element) -> List[Dict]:
        """Extract all PackageReference elements."""
        packages = []

        for item_group in root.findall('.//ItemGroup'):
            for pkg_ref in item_group.findall('PackageReference'):
                include = pkg_ref.get('Include')
                version = pkg_ref.get('Version')

                # Version might be in a child element
                if not version:
                    version_elem = pkg_ref.find('Version')
                    if version_elem is not None:
                        version = version_elem.text

                if include:
                    packages.append({
                        'name': include,
                        'version': version or 'unspecified'
                    })

        return packages

    def _check_framework_target(self, root: ET.Element):
        """Check for outdated framework targets."""
        outdated_frameworks = {
            'net45': '.NET Framework 4.5 is out of support - upgrade to .NET 6/7/8',
            'net451': '.NET Framework 4.5.1 is out of support - upgrade to .NET 6/7/8',
            'net452': '.NET Framework 4.5.2 is out of support - upgrade to .NET 6/7/8',
            'net46': '.NET Framework 4.6 is out of support - upgrade to .NET 6/7/8',
            'net461': '.NET Framework 4.6.1 is out of support - upgrade to .NET 6/7/8',
            'net462': '.NET Framework 4.6.2 is approaching end of support - plan upgrade to .NET 6/7/8',
            'net47': '.NET Framework 4.7 is older - consider upgrading to .NET 6/7/8',
            'net471': '.NET Framework 4.7.1 is older - consider upgrading to .NET 6/7/8',
            'net472': '.NET Framework 4.7.2 - consider upgrading to .NET 6/7/8',
            'net48': '.NET Framework 4.8 - consider migrating to .NET 6/7/8 for long-term support',
            'netcoreapp2.0': '.NET Core 2.0 is out of support - upgrade to .NET 6/7/8',
            'netcoreapp2.1': '.NET Core 2.1 is out of support - upgrade to .NET 6/7/8',
            'netcoreapp2.2': '.NET Core 2.2 is out of support - upgrade to .NET 6/7/8',
            'netcoreapp3.0': '.NET Core 3.0 is out of support - upgrade to .NET 6/7/8',
            'netcoreapp3.1': '.NET Core 3.1 is out of support (Dec 2022) - upgrade to .NET 6/7/8',
            'net5.0': '.NET 5 is out of support (May 2022) - upgrade to .NET 6/7/8',
            'net6.0': '.NET 6 will be out of support in Nov 2024 - plan upgrade to .NET 8 LTS',
            'net7.0': '.NET 7 is out of support (May 2024) - upgrade to .NET 8',
        }

        for prop_group in root.findall('.//PropertyGroup'):
            tf = prop_group.find('TargetFramework')
            if tf is not None and tf.text:
                fw = tf.text.lower()
                if fw in outdated_frameworks:
                    severity = 'high' if 'out of support' in outdated_frameworks[fw] else 'medium'
                    self.issues['framework_issues'].append({
                        'framework': tf.text,
                        'severity': severity,
                        'message': outdated_frameworks[fw]
                    })

            # Check for multi-targeting
            tfs = prop_group.find('TargetFrameworks')
            if tfs is not None and tfs.text:
                frameworks = tfs.text.split(';')
                for fw in frameworks:
                    fw = fw.strip().lower()
                    if fw in outdated_frameworks:
                        severity = 'medium'  # Lower severity for multi-target
                        self.issues['framework_issues'].append({
                            'framework': fw,
                            'severity': severity,
                            'message': f'Multi-targeting includes {fw}: {outdated_frameworks[fw]}'
                        })

    def _check_nullable_configuration(self, root: ET.Element):
        """Check if nullable reference types are enabled."""
        nullable_found = False

        for prop_group in root.findall('.//PropertyGroup'):
            nullable = prop_group.find('Nullable')
            if nullable is not None and nullable.text:
                nullable_found = True
                if nullable.text.lower() not in ['enable', 'annotations', 'warnings']:
                    self.issues['configuration'].append({
                        'setting': 'Nullable',
                        'value': nullable.text,
                        'severity': 'low',
                        'message': f'Nullable is set to "{nullable.text}" - consider "enable" for better null safety'
                    })

        if not nullable_found:
            self.issues['configuration'].append({
                'setting': 'Nullable',
                'value': 'not set',
                'severity': 'medium',
                'message': 'Nullable reference types not enabled - add <Nullable>enable</Nullable> for better null safety'
            })

    def _check_code_analysis(self, root: ET.Element):
        """Check if code analysis is enabled."""
        analysis_settings = {
            'EnableNETAnalyzers': False,
            'TreatWarningsAsErrors': False,
            'AnalysisLevel': None
        }

        for prop_group in root.findall('.//PropertyGroup'):
            for setting in analysis_settings:
                elem = prop_group.find(setting)
                if elem is not None and elem.text:
                    if setting in ['EnableNETAnalyzers', 'TreatWarningsAsErrors']:
                        analysis_settings[setting] = elem.text.lower() == 'true'
                    else:
                        analysis_settings[setting] = elem.text

        if not analysis_settings['EnableNETAnalyzers']:
            self.issues['configuration'].append({
                'setting': 'EnableNETAnalyzers',
                'value': 'false or not set',
                'severity': 'medium',
                'message': 'Code analysis not enabled - add <EnableNETAnalyzers>true</EnableNETAnalyzers>'
            })

        if not analysis_settings['TreatWarningsAsErrors']:
            self.issues['configuration'].append({
                'setting': 'TreatWarningsAsErrors',
                'value': 'false or not set',
                'severity': 'low',
                'message': 'Warnings not treated as errors - consider enabling for stricter code quality'
            })

    def _check_deprecated_packages(self, packages: List[Dict]):
        """Check for known deprecated NuGet packages."""
        deprecated = {
            'Microsoft.AspNet.Mvc': 'Use Microsoft.AspNetCore.Mvc for ASP.NET Core',
            'Microsoft.AspNet.WebApi': 'Use Microsoft.AspNetCore.Mvc for ASP.NET Core',
            'System.Data.SqlClient': 'Deprecated - use Microsoft.Data.SqlClient instead',
            'Microsoft.EntityFrameworkCore.Tools.DotNet': 'Use dotnet ef global tool instead',
            'Newtonsoft.Json': 'Consider migrating to System.Text.Json (built-in, better performance)',
            'NLog': 'Consider Microsoft.Extensions.Logging with NLog.Extensions.Logging',
            'log4net': 'Consider Microsoft.Extensions.Logging abstractions',
            'AutoMapper': 'Consider Mapperly (source generator, better performance)',
            'Moq': 'Consider NSubstitute or FakeItEasy for cleaner syntax',
            'xunit.runner.visualstudio': 'Often unnecessary in modern .NET projects',
        }

        for pkg in packages:
            pkg_name = pkg['name']
            if pkg_name in deprecated:
                # Newtonsoft.Json is common, mark as medium; others as high
                severity = 'medium' if pkg_name == 'Newtonsoft.Json' else 'medium'

                self.issues['outdated'].append({
                    'package': pkg_name,
                    'version': pkg['version'],
                    'severity': severity,
                    'message': deprecated[pkg_name]
                })

    def _check_duplicate_functionality(self, packages: List[Dict]):
        """Check for packages that provide duplicate functionality."""
        pkg_names = [p['name'] for p in packages]

        # Common duplications in .NET
        duplication_groups = [
            {
                'packages': ['Newtonsoft.Json', 'System.Text.Json'],
                'functionality': 'JSON Serialization'
            },
            {
                'packages': ['NLog', 'Serilog', 'log4net', 'Microsoft.Extensions.Logging'],
                'functionality': 'Logging'
            },
            {
                'packages': ['AutoMapper', 'Mapperly', 'AgileMapper'],
                'functionality': 'Object Mapping'
            },
            {
                'packages': ['Moq', 'NSubstitute', 'FakeItEasy'],
                'functionality': 'Mocking Framework'
            },
            {
                'packages': ['xUnit', 'NUnit', 'MSTest'],
                'functionality': 'Test Framework'
            },
            {
                'packages': ['FluentValidation', 'DataAnnotations'],
                'functionality': 'Validation'
            },
            {
                'packages': ['Dapper', 'Entity Framework Core', 'NHibernate'],
                'functionality': 'Data Access'
            },
        ]

        for group in duplication_groups:
            found = [pkg for pkg in group['packages'] if pkg in pkg_names]
            if len(found) > 1:
                self.issues['duplicate_functionality'].append({
                    'packages': found,
                    'functionality': group['functionality'],
                    'severity': 'medium',
                    'message': f'Multiple packages for {group["functionality"]}: {", ".join(found)}'
                })

    def _check_version_constraints(self, packages: List[Dict]):
        """Check for version constraint issues."""
        for pkg in packages:
            version = pkg['version']

            # Check for wildcard versions
            if '*' in version:
                self.issues['warnings'].append({
                    'package': pkg['name'],
                    'version': version,
                    'severity': 'high',
                    'message': f'Wildcard version constraint can cause unexpected breaking changes'
                })

            # Check for unspecified versions
            if version == 'unspecified' or not version:
                self.issues['warnings'].append({
                    'package': pkg['name'],
                    'version': 'not specified',
                    'severity': 'medium',
                    'message': 'Version not specified - use explicit versioning'
                })

    def _generate_summary(self) -> Dict:
        """Generate summary statistics."""
        total_issues = sum(len(issues) for issues in self.issues.values())

        severity_count = {'high': 0, 'medium': 0, 'low': 0}
        for category in self.issues.values():
            for issue in category:
                if 'severity' in issue:
                    severity_count[issue['severity']] += 1

        return {
            'total_issues': total_issues,
            'by_severity': severity_count,
            'by_category': {k: len(v) for k, v in self.issues.items()}
        }


def format_report(analysis: Dict) -> str:
    """Format analysis results as markdown."""
    if not analysis:
        return "No analysis available"

    report = ["# .NET Dependency Analysis Report\n"]
    report.append(f"**Project:** {analysis['project_name']}")
    report.append(f"**Target Framework:** {analysis['target_framework']}")
    report.append(f"**SDK-Style Project:** {'Yes' if analysis['sdk_style'] else 'No (Legacy format)'}")
    report.append(f"**Package References:** {analysis['total_package_references']}")
    report.append(f"**Total Issues:** {analysis['summary']['total_issues']}\n")

    report.append("## Summary\n")
    for severity, count in analysis['summary']['by_severity'].items():
        if count > 0:
            report.append(f"- **{severity.upper()}:** {count}")
    report.append("\n")

    # Issues by category
    category_names = {
        'framework_issues': 'Framework Targeting Issues',
        'outdated': 'Deprecated/Outdated Packages',
        'duplicate_functionality': 'Duplicate Functionality',
        'configuration': 'Configuration Issues',
        'warnings': 'Version Constraint Warnings',
    }

    for category, name in category_names.items():
        issues = analysis['issues'].get(category, [])
        if issues:
            report.append(f"## {name} ({len(issues)})\n")

            for issue in issues:
                if 'package' in issue:
                    report.append(f"### {issue['package']} ")
                elif 'framework' in issue:
                    report.append(f"### {issue['framework']} ")
                elif 'setting' in issue:
                    report.append(f"### {issue['setting']} ")
                else:
                    report.append(f"### Issue ")

                report.append(f"[{issue.get('severity', 'info').upper()}]\n")
                report.append(f"{issue['message']}\n")

                if 'version' in issue and 'package' in issue:
                    report.append(f"- Current version: `{issue['version']}`\n")
                if 'packages' in issue:
                    report.append(f"- Affected packages: {', '.join(issue['packages'])}\n")
                if 'value' in issue:
                    report.append(f"- Current value: `{issue['value']}`\n")

                report.append("\n")

    # Recommendations
    report.append("## Recommendations\n")
    if analysis['summary']['total_issues'] > 0:
        report.append("1. Update deprecated packages to modern alternatives\n")
        report.append("2. Upgrade to latest LTS .NET version (.NET 8 as of 2024)\n")
        report.append("3. Enable nullable reference types for better null safety\n")
        report.append("4. Enable .NET code analyzers for better code quality\n")
        report.append("5. Consolidate duplicate functionality to reduce dependencies\n")
        report.append("6. Run `dotnet list package --vulnerable` to check for security vulnerabilities\n")
        report.append("7. Run `dotnet list package --outdated` to check for available updates\n")
        report.append("8. Consider using Directory.Build.props for shared settings across projects\n")
    else:
        report.append("✅ No major dependency issues detected!\n")
        report.append("\nRegular maintenance recommendations:\n")
        report.append("- Run `dotnet list package --vulnerable` monthly\n")
        report.append("- Run `dotnet list package --outdated` quarterly\n")
        report.append("- Keep dependencies up to date with security patches\n")

    return ''.join(report)


def main():
    csproj_path = sys.argv[1] if len(sys.argv) > 1 else 'Project.csproj'

    # If it's a directory, look for .csproj files
    path = Path(csproj_path)
    if path.is_dir():
        csproj_files = list(path.glob('*.csproj'))
        if not csproj_files:
            print(f"Error: No .csproj files found in {path}")
            sys.exit(1)
        csproj_path = str(csproj_files[0])
        print(f"Found .csproj: {csproj_path}\n")

    analyzer = DotNetDependencyAnalyzer(csproj_path)
    analysis = analyzer.analyze()

    if analysis:
        report = format_report(analysis)
        print(report)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
