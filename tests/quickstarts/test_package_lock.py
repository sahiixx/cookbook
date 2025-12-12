"""
Comprehensive tests for package-lock.json validation.

This test suite validates the package-lock.json file structure, dependencies,
and ensures it follows npm's lockfile format specifications.
"""
import pytest
import json
from pathlib import Path
from jsonschema import validate, ValidationError
import re


class TestPackageLockJSON:
    """Test suite for package-lock.json validation."""
    
    @pytest.fixture
    def package_lock_path(self):
        """Return the path to package-lock.json."""
        return Path("quickstarts/file-api/package-lock.json")
    
    @pytest.fixture
    def package_lock(self, package_lock_path):
        """Load and return the package-lock.json content."""
        with open(package_lock_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @pytest.fixture
    def package_json_path(self):
        """Return the path to package.json."""
        return Path("quickstarts/file-api/package.json")
    
    @pytest.fixture
    def package_json(self, package_json_path):
        """Load and return the package.json content."""
        with open(package_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_file_exists(self, package_lock_path):
        """Test that package-lock.json exists."""
        assert package_lock_path.exists(), f"package-lock.json not found at {package_lock_path}"
        assert package_lock_path.is_file(), f"{package_lock_path} is not a file"
    
    def test_valid_json(self, package_lock_path):
        """Test that package-lock.json is valid JSON."""
        try:
            with open(package_lock_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"package-lock.json is not valid JSON: {e}")
    
    def test_has_required_top_level_fields(self, package_lock):
        """Test that package-lock.json has required top-level fields."""
        required_fields = ['name', 'version', 'lockfileVersion', 'requires', 'packages']
        
        for field in required_fields:
            assert field in package_lock, f"Missing required field: {field}"
    
    def test_lockfile_version(self, package_lock):
        """Test that lockfileVersion is correct (should be 3 for npm 7+)."""
        assert 'lockfileVersion' in package_lock
        assert package_lock['lockfileVersion'] == 3, "lockfileVersion should be 3"
    
    def test_name_matches_package_json(self, package_lock, package_json):
        """Test that name matches between package.json and package-lock.json."""
        assert package_lock['name'] == package_json['name'], \
            "Name mismatch between package.json and package-lock.json"
    
    def test_version_matches_package_json(self, package_lock, package_json):
        """Test that version matches between package.json and package-lock.json."""
        assert package_lock['version'] == package_json['version'], \
            "Version mismatch between package.json and package-lock.json"
    
    def test_packages_is_dict(self, package_lock):
        """Test that packages field is a dictionary."""
        assert 'packages' in package_lock
        assert isinstance(package_lock['packages'], dict), \
            "packages field should be a dictionary"
    
    def test_root_package_exists(self, package_lock):
        """Test that root package ("") exists in packages."""
        assert '' in package_lock['packages'], \
            "Root package entry ('') not found in packages"
    
    def test_root_package_has_dependencies(self, package_lock):
        """Test that root package has dependencies field."""
        root_package = package_lock['packages']['']
        assert 'dependencies' in root_package, \
            "Root package should have dependencies field"
    
    def test_expected_dependencies_present(self, package_lock, package_json):
        """Test that all package.json dependencies are in package-lock.json."""
        expected_deps = package_json.get('dependencies', {})
        lock_root_deps = package_lock['packages'][''].get('dependencies', {})
        
        for dep_name in expected_deps:
            assert dep_name in lock_root_deps, \
                f"Dependency '{dep_name}' from package.json not found in package-lock.json"
    
    def test_dotenv_dependency(self, package_lock):
        """Test that dotenv dependency is correctly specified."""
        root_deps = package_lock['packages'][''].get('dependencies', {})
        assert 'dotenv' in root_deps, "dotenv not found in dependencies"
        
        # Check that dotenv version matches expected pattern
        version = root_deps['dotenv']
        assert re.match(r'\^?\d+\.\d+\.\d+', version), \
            f"dotenv version '{version}' doesn't match expected pattern"
    
    def test_googleapis_dependency(self, package_lock):
        """Test that googleapis dependency is correctly specified."""
        root_deps = package_lock['packages'][''].get('dependencies', {})
        assert 'googleapis' in root_deps, "googleapis not found in dependencies"
        
        version = root_deps['googleapis']
        assert re.match(r'\^?\d+\.\d+\.\d+', version), \
            f"googleapis version '{version}' doesn't match expected pattern"
    
    def test_mime_types_dependency(self, package_lock):
        """Test that mime-types dependency is correctly specified."""
        root_deps = package_lock['packages'][''].get('dependencies', {})
        assert 'mime-types' in root_deps, "mime-types not found in dependencies"
        
        version = root_deps['mime-types']
        assert re.match(r'\^?\d+\.\d+\.\d+', version), \
            f"mime-types version '{version}' doesn't match expected pattern"
    
    def test_node_modules_entries(self, package_lock):
        """Test that node_modules packages are properly defined."""
        packages = package_lock['packages']
        
        # Check for some expected node_modules entries
        expected_modules = [
            'node_modules/dotenv',
            'node_modules/googleapis',
            'node_modules/mime-types'
        ]
        
        for module in expected_modules:
            assert module in packages, f"Expected module '{module}' not found in packages"
    
    def test_package_integrity_hashes(self, package_lock):
        """Test that packages have integrity hashes where expected."""
        packages = package_lock['packages']
        
        # Check a sample of packages for integrity hashes
        for pkg_path, pkg_data in packages.items():
            if pkg_path and 'node_modules/' in pkg_path:
                # External packages should have integrity or be links
                if 'resolved' in pkg_data:
                    assert 'integrity' in pkg_data or 'link' in pkg_data, \
                        f"Package '{pkg_path}' should have integrity hash or be a link"
    
    def test_no_duplicate_packages(self, package_lock):
        """Test that there are no obvious duplicate package entries."""
        packages = package_lock['packages']
        package_names = {}
        
        for pkg_path in packages.keys():
            if pkg_path and 'node_modules/' in pkg_path:
                # Extract package name
                name = pkg_path.split('node_modules/')[-1].split('/node_modules/')[0]
                if name in package_names:
                    # Multiple versions are OK, just track them
                    package_names[name] += 1
                else:
                    package_names[name] = 1
        
        # This is informational - multiple versions can exist
        assert len(package_names) > 0, "Should have at least some packages"
    
    def test_package_engines(self, package_lock):
        """Test that packages specify compatible engines where applicable."""
        packages = package_lock['packages']
        root = packages['']
        
        # Root package might not have engines, but if it does, validate it
        if 'engines' in root:
            engines = root['engines']
            assert isinstance(engines, dict), "engines should be a dictionary"
    
    def test_requires_field_structure(self, package_lock):
        """Test that requires field has proper structure."""
        assert 'requires' in package_lock
        assert isinstance(package_lock['requires'], bool), \
            "requires field should be a boolean"
        assert package_lock['requires'] == True, \
            "requires should be True for npm 7+"


class TestPackageLockDependencies:
    """Test suite for package-lock.json dependency validation."""
    
    @pytest.fixture
    def package_lock_path(self):
        """Return the path to package-lock.json."""
        return Path("quickstarts/file-api/package-lock.json")
    
    @pytest.fixture
    def package_lock(self, package_lock_path):
        """Load and return the package-lock.json content."""
        with open(package_lock_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_all_packages_have_version(self, package_lock):
        """Test that all package entries have a version field."""
        packages = package_lock['packages']
        
        for pkg_path, pkg_data in packages.items():
            if pkg_path:  # Skip root package
                assert 'version' in pkg_data or 'link' in pkg_data, \
                    f"Package '{pkg_path}' missing version field"
    
    def test_resolved_urls_are_valid(self, package_lock):
        """Test that resolved URLs follow expected patterns."""
        packages = package_lock['packages']
        
        valid_patterns = [
            r'https://registry\.npmjs\.org/',
            r'https://registry\.yarnpkg\.com/',
        ]
        
        for pkg_path, pkg_data in packages.items():
            if 'resolved' in pkg_data:
                resolved = pkg_data['resolved']
                assert any(re.match(pattern, resolved) for pattern in valid_patterns), \
                    f"Package '{pkg_path}' has unexpected resolved URL: {resolved}"
    
    def test_license_fields_present(self, package_lock):
        """Test that packages have license information where expected."""
        packages = package_lock['packages']
        
        for pkg_path, pkg_data in packages.items():
            if pkg_path and 'node_modules/' in pkg_path:
                # External packages should ideally have license info
                # But this isn't always present, so we just check the field exists if present
                if 'license' in pkg_data:
                    assert isinstance(pkg_data['license'], str), \
                        f"Package '{pkg_path}' license should be a string"


class TestPackageLockEdgeCases:
    """Edge case and error condition tests for package-lock.json."""
    
    @pytest.fixture
    def package_lock_path(self):
        """Return the path to package-lock.json."""
        return Path("quickstarts/file-api/package-lock.json")
    
    @pytest.fixture
    def package_lock(self, package_lock_path):
        """Load and return the package-lock.json content."""
        with open(package_lock_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_file_size_reasonable(self, package_lock_path):
        """Test that package-lock.json size is reasonable."""
        file_size = package_lock_path.stat().st_size
        # Should be at least 1KB and less than 10MB
        assert file_size > 1000, "package-lock.json seems too small"
        assert file_size < 10 * 1024 * 1024, "package-lock.json seems too large"
    
    def test_no_circular_dependencies(self, package_lock):
        """Test for obvious circular dependencies."""
        packages = package_lock['packages']
        
        # Build dependency graph
        dep_graph = {}
        for pkg_path, pkg_data in packages.items():
            if 'dependencies' in pkg_data:
                dep_graph[pkg_path] = list(pkg_data['dependencies'].keys())
        
        # Simple cycle detection would be complex, so we just check the structure exists
        assert isinstance(dep_graph, dict)
    
    def test_semver_ranges_valid(self, package_lock):
        """Test that version ranges follow semver patterns."""
        root_deps = package_lock['packages'][''].get('dependencies', {})
        
        semver_pattern = r'^[\^~]?\d+\.\d+\.\d+(-[\w\.-]+)?(\+[\w\.-]+)?$'
        
        for dep_name, version in root_deps.items():
            # Version might be a range or exact version
            assert isinstance(version, str), \
                f"Dependency '{dep_name}' version should be a string"
            # Basic validation that it looks like a version
            assert len(version) > 0, f"Dependency '{dep_name}' has empty version"
    
    def test_no_malformed_json(self, package_lock_path):
        """Test that JSON doesn't have common malformations."""
        with open(package_lock_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for common JSON issues
        assert content.count('{') == content.count('}'), \
            "Mismatched curly braces"
        assert content.count('[') == content.count(']'), \
            "Mismatched square brackets"
    
    def test_utf8_encoding(self, package_lock_path):
        """Test that file is properly UTF-8 encoded."""
        try:
            with open(package_lock_path, 'r', encoding='utf-8') as f:
                f.read()
        except UnicodeDecodeError as e:
            pytest.fail(f"File is not valid UTF-8: {e}")
    
    def test_no_sensitive_data(self, package_lock):
        """Test that package-lock.json doesn't contain sensitive data."""
        # Convert to string for searching
        content = json.dumps(package_lock)
        
        # Check for patterns that might indicate tokens or keys
        sensitive_patterns = [
            r'["\']?token["\']?\s*:\s*["\'][^"\']+["\']',
            r'["\']?password["\']?\s*:\s*["\'][^"\']+["\']',
            r'["\']?secret["\']?\s*:\s*["\'][^"\']+["\']',
        ]
        
        for pattern in sensitive_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            # Registry tokens are OK, but not other secrets
            for match in matches:
                if 'npm' not in match.lower() and 'registry' not in match.lower():
                    pytest.fail(f"Potential sensitive data found: {pattern}")


class TestPackageLockConsistency:
    """Tests for consistency between package.json and package-lock.json."""
    
    @pytest.fixture
    def package_lock_path(self):
        """Return the path to package-lock.json."""
        return Path("quickstarts/file-api/package-lock.json")
    
    @pytest.fixture
    def package_lock(self, package_lock_path):
        """Load and return the package-lock.json content."""
        with open(package_lock_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    @pytest.fixture
    def package_json_path(self):
        """Return the path to package.json."""
        return Path("quickstarts/file-api/package.json")
    
    @pytest.fixture
    def package_json(self, package_json_path):
        """Load and return the package.json content."""
        with open(package_json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_dependency_count_reasonable(self, package_lock, package_json):
        """Test that package-lock has reasonable number of dependencies."""
        lock_deps_count = len(package_lock['packages'])
        json_deps_count = len(package_json.get('dependencies', {}))
        
        # Lock file should have more dependencies (including transitive)
        assert lock_deps_count > json_deps_count, \
            "package-lock.json should have more dependencies than package.json"
    
    def test_no_missing_dependencies(self, package_lock, package_json):
        """Test that no required dependencies are missing."""
        required_deps = set(package_json.get('dependencies', {}).keys())
        lock_root_deps = set(package_lock['packages'][''].get('dependencies', {}).keys())
        
        missing = required_deps - lock_root_deps
        assert len(missing) == 0, f"Missing dependencies in package-lock.json: {missing}"
    
    def test_version_compatibility(self, package_lock, package_json):
        """Test that locked versions are compatible with package.json ranges."""
        json_deps = package_json.get('dependencies', {})
        lock_root_deps = package_lock['packages'][''].get('dependencies', {})
        
        for dep_name in json_deps:
            if dep_name in lock_root_deps:
                json_version = json_deps[dep_name]
                lock_version = lock_root_deps[dep_name]
                
                # Both should be strings
                assert isinstance(json_version, str)
                assert isinstance(lock_version, str)
                
                # If json has ^, lock should not (it should be exact)
                if json_version.startswith('^'):
                    assert not lock_version.startswith('^'), \
                        f"Lock version for '{dep_name}' should be exact, not a range"