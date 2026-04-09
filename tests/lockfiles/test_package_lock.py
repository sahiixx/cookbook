"""
Tests for package-lock.json file validation.
"""

import json
import pytest
from pathlib import Path


class TestPackageLockFile:
    """Test suite for package-lock.json"""
    
    @pytest.fixture
    def lockfile_path(self):
        return Path("quickstarts/file-api/package-lock.json")
    
    @pytest.fixture
    def lockfile_content(self, lockfile_path):
        with open(lockfile_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_lockfile_exists(self, lockfile_path):
        """Test that package-lock.json exists"""
        assert lockfile_path.exists(), f"Lock file not found at {lockfile_path}"
    
    def test_lockfile_is_valid_json(self, lockfile_path):
        """Test that lock file is valid JSON"""
        try:
            with open(lockfile_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Lock file is not valid JSON: {e}")
    
    def test_lockfile_has_required_fields(self, lockfile_content):
        """Test that lock file has required npm lockfile fields"""
        required_fields = ["name", "version", "lockfileVersion", "packages"]
        
        for field in required_fields:
            assert field in lockfile_content, \
                f"Lock file missing required field: {field}"
    
    def test_package_name_matches(self, lockfile_content):
        """Test that package name in lock file matches expected name"""
        name = lockfile_content.get("name")
        assert name == "file-api-client-samples", \
            f"Package name should be 'file-api-client-samples', got '{name}'"
    
    def test_uses_https_registry(self, lockfile_content):
        """Test that dependencies are resolved from HTTPS registry"""
        packages = lockfile_content.get("packages", {})
        
        for pkg_path, pkg_info in packages.items():
            resolved = pkg_info.get("resolved", "")
            if resolved and resolved.startswith("http://"):
                pytest.fail(f"Package '{pkg_path}' uses insecure HTTP registry")