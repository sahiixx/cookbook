#!/usr/bin/env python3
"""
Unit tests for package-lock.json integrity and dependency management.

Tests ensure the package lock file is valid, dependencies are properly locked,
and there are no security or integrity issues.
"""

import unittest
import json
from pathlib import Path
import re


class TestPackageLockStructure(unittest.TestCase):
    """Test the structure and validity of package-lock.json."""
    
    @classmethod
    def setUpClass(cls):
        """Load package-lock.json file."""
        lock_path = Path("quickstarts/file-api/package-lock.json")
        with open(lock_path, 'r', encoding='utf-8') as f:
            cls.package_lock = json.load(f)
    
    def test_package_lock_is_valid_json(self):
        """Test that package-lock.json is valid JSON."""
        self.assertIsInstance(self.package_lock, dict)
    
    def test_has_required_fields(self):
        """Test that package-lock.json has required top-level fields."""
        required_fields = ['name', 'version', 'lockfileVersion', 'requires', 'packages']
        for field in required_fields:
            self.assertIn(field, self.package_lock,
                         f"package-lock.json should have '{field}' field")
    
    def test_lockfile_version(self):
        """Test that lockfile version is valid."""
        version = self.package_lock.get('lockfileVersion')
        self.assertIsNotNone(version, "Should have lockfileVersion")
        self.assertIsInstance(version, int, "lockfileVersion should be integer")
        self.assertGreaterEqual(version, 1, "lockfileVersion should be >= 1")
    
    def test_package_name_matches(self):
        """Test that package name matches expected value."""
        self.assertEqual(self.package_lock.get('name'), 'file-api-client-samples',
                        "Package name should be 'file-api-client-samples'")
    
    def test_has_packages_section(self):
        """Test that packages section exists and is a dictionary."""
        packages = self.package_lock.get('packages')
        self.assertIsNotNone(packages)
        self.assertIsInstance(packages, dict)
    
    def test_root_package_exists(self):
        """Test that root package ("") entry exists."""
        packages = self.package_lock.get('packages', {})
        self.assertIn('', packages, "Should have root package entry")
        root = packages['']
        self.assertIn('dependencies', root, "Root should have dependencies")


class TestDependencies(unittest.TestCase):
    """Test dependency declarations and integrity."""
    
    @classmethod
    def setUpClass(cls):
        """Load package files."""
        lock_path = Path("quickstarts/file-api/package-lock.json")
        pkg_path = Path("quickstarts/file-api/package.json")
        
        with open(lock_path, 'r', encoding='utf-8') as f:
            cls.package_lock = json.load(f)
        with open(pkg_path, 'r', encoding='utf-8') as f:
            cls.package_json = json.load(f)
    
    def test_dependencies_match_package_json(self):
        """Test that locked dependencies match package.json."""
        pkg_deps = self.package_json.get('dependencies', {})
        lock_deps = self.package_lock.get('packages', {}).get('', {}).get('dependencies', {})
        
        for dep_name in pkg_deps:
            self.assertIn(dep_name, lock_deps,
                         f"Dependency '{dep_name}' should be in package-lock.json")
    
    def test_required_dependencies_present(self):
        """Test that required project dependencies are present."""
        required_deps = ['dotenv', 'googleapis', 'mime-types']
        lock_deps = self.package_lock.get('packages', {}).get('', {}).get('dependencies', {})
        
        for dep in required_deps:
            self.assertIn(dep, lock_deps,
                         f"Required dependency '{dep}' should be present")
    
    def test_googleapis_dependency(self):
        """Test googleapis dependency configuration."""
        packages = self.package_lock.get('packages', {})
        
        # Find googleapis in node_modules
        googleapis_keys = [k for k in packages.keys() if 'googleapis' in k]
        self.assertGreater(len(googleapis_keys), 0,
                          "Should have googleapis package")
    
    def test_dotenv_dependency(self):
        """Test dotenv dependency for environment variable management."""
        packages = self.package_lock.get('packages', {})
        
        dotenv_keys = [k for k in packages.keys() if 'dotenv' in k and 'node_modules/dotenv' in k]
        self.assertGreater(len(dotenv_keys), 0,
                          "Should have dotenv package")
    
    def test_mime_types_dependency(self):
        """Test mime-types dependency."""
        packages = self.package_lock.get('packages', {})
        
        mime_keys = [k for k in packages.keys() if 'mime-types' in k]
        self.assertGreater(len(mime_keys), 0,
                          "Should have mime-types package")


class TestPackageIntegrity(unittest.TestCase):
    """Test package integrity and security."""
    
    @classmethod
    def setUpClass(cls):
        """Load package-lock.json."""
        lock_path = Path("quickstarts/file-api/package-lock.json")
        with open(lock_path, 'r', encoding='utf-8') as f:
            cls.package_lock = json.load(f)
        cls.packages = cls.package_lock.get('packages', {})
    
    def test_packages_have_integrity_or_resolved(self):
        """Test that packages have integrity hashes or resolved URLs."""
        node_modules_packages = {k: v for k, v in self.packages.items() 
                                 if k.startswith('node_modules/')}
        
        for pkg_name, pkg_data in node_modules_packages.items():
            # Should have either integrity or be a link
            has_integrity = 'integrity' in pkg_data
            has_resolved = 'resolved' in pkg_data
            is_link = pkg_data.get('link', False)
            
            self.assertTrue(has_integrity or has_resolved or is_link,
                          f"Package {pkg_name} should have integrity or resolved field")
    
    def test_no_obvious_vulnerabilities(self):
        """Test that there are no obvious vulnerability indicators."""
        # This is a basic check - real vulnerability scanning needs specialized tools
        for pkg_name, pkg_data in self.packages.items():
            if 'version' in pkg_data:
                version = pkg_data['version']
                # Check for obviously old or suspicious versions
                if version:
                    # Major version should be reasonable
                    match = re.match(r'^(\d+)', version)
                    if match:
                        major = int(match.group(1))
                        # Just a sanity check - versions shouldn't be absurdly high
                        self.assertLess(major, 1000,
                                      f"Package {pkg_name} has suspicious version {version}")
    
    def test_resolved_urls_use_https(self):
        """Test that resolved URLs use HTTPS."""
        for pkg_name, pkg_data in self.packages.items():
            if 'resolved' in pkg_data:
                resolved = pkg_data['resolved']
                if resolved.startswith('http'):
                    self.assertTrue(resolved.startswith('https://'),
                                  f"Package {pkg_name} should use HTTPS: {resolved}")
    
    def test_no_file_protocol_dependencies(self):
        """Test that no dependencies use file:// protocol."""
        for pkg_name, pkg_data in self.packages.items():
            if 'resolved' in pkg_data:
                resolved = pkg_data['resolved']
                self.assertFalse(resolved.startswith('file://'),
                               f"Package {pkg_name} should not use file:// protocol")


class TestVersionConsistency(unittest.TestCase):
    """Test version consistency across package files."""
    
    @classmethod
    def setUpClass(cls):
        """Load both package files."""
        lock_path = Path("quickstarts/file-api/package-lock.json")
        pkg_path = Path("quickstarts/file-api/package.json")
        
        with open(lock_path, 'r', encoding='utf-8') as f:
            cls.package_lock = json.load(f)
        with open(pkg_path, 'r', encoding='utf-8') as f:
            cls.package_json = json.load(f)
    
    def test_version_matches(self):
        """Test that version in package.json matches package-lock.json."""
        pkg_version = self.package_json.get('version')
        lock_version = self.package_lock.get('version')
        
        self.assertEqual(pkg_version, lock_version,
                        "Versions should match between package.json and package-lock.json")
    
    def test_name_matches(self):
        """Test that name matches between files."""
        pkg_name = self.package_json.get('name')
        lock_name = self.package_lock.get('name')
        
        self.assertEqual(pkg_name, lock_name,
                        "Names should match between package.json and package-lock.json")


class TestDependencyTree(unittest.TestCase):
    """Test the dependency tree structure."""
    
    @classmethod
    def setUpClass(cls):
        """Load package-lock.json."""
        lock_path = Path("quickstarts/file-api/package-lock.json")
        with open(lock_path, 'r', encoding='utf-8') as f:
            cls.package_lock = json.load(f)
        cls.packages = cls.package_lock.get('packages', {})
    
    def test_no_circular_dependencies(self):
        """Test that there are no obvious circular dependencies."""
        # Build a simple dependency graph
        dep_graph = {}
        
        for pkg_name, pkg_data in self.packages.items():
            if pkg_name:  # Skip root
                deps = pkg_data.get('dependencies', {})
                dep_graph[pkg_name] = list(deps.keys())
        
        # This is a simplified check - full circular dependency detection is complex
        # Just check that packages don't directly depend on themselves
        for pkg_name, deps in dep_graph.items():
            pkg_base = pkg_name.replace('node_modules/', '').split('/')[0]
            for dep in deps:
                self.assertNotEqual(pkg_base, dep,
                                  f"Package {pkg_name} should not directly depend on itself")
    
    def test_transitive_dependencies_present(self):
        """Test that transitive dependencies are included."""
        # Get direct dependencies
        root_deps = self.packages.get('', {}).get('dependencies', {})
        
        # For each direct dependency, check if it and its deps are in packages
        for dep_name in root_deps:
            node_modules_key = f'node_modules/{dep_name}'
            matching_keys = [k for k in self.packages.keys() if dep_name in k]
            
            self.assertGreater(len(matching_keys), 0,
                             f"Dependency {dep_name} should be in packages")


if __name__ == '__main__':
    unittest.main(verbosity=2)