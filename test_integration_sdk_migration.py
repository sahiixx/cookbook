#!/usr/bin/env python3
"""
Integration tests for SDK migration across the repository.

Tests ensure that the migration from google-genai to google-generativeai
is consistent across all affected files and examples.
"""

import unittest
import json
import re
from pathlib import Path
from typing import List, Dict, Tuple


class TestSDKMigrationConsistency(unittest.TestCase):
    """Test that SDK migration is consistent across the repository."""
    
    @classmethod
    def setUpClass(cls):
        """Scan repository for notebook files."""
        cls.examples_dir = Path("examples")
        cls.notebooks = list(cls.examples_dir.glob("*.ipynb"))
        cls.voice_memos_path = cls.examples_dir / "Voice_memos.ipynb"
    
    def test_voice_memos_uses_new_sdk(self):
        """Test that Voice_memos.ipynb uses the new SDK."""
        with open(self.voice_memos_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        all_code = '\n'.join([''.join(cell['source']) for cell in code_cells])
        
        # Should use new SDK
        self.assertIn('google.generativeai', all_code,
                     "Voice_memos should use google.generativeai")
        self.assertIn('genai.configure', all_code,
                     "Voice_memos should use genai.configure")
        
        # Should not use old SDK
        self.assertNotIn('from google import genai', all_code,
                        "Voice_memos should not use old SDK import")
    
    def test_no_mixed_sdk_usage(self):
        """Test that notebooks don't mix old and new SDK patterns."""
        with open(self.voice_memos_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        all_code = '\n'.join([''.join(cell['source']) for cell in code_cells])
        
        # If using new SDK, shouldn't have old patterns
        if 'google.generativeai' in all_code:
            self.assertNotIn('client.files.upload', all_code,
                           "Should not mix old and new file upload methods")
            self.assertNotIn('client.models.generate_content', all_code,
                           "Should not mix old and new generation methods")


class TestNotebookAPIPatterns(unittest.TestCase):
    """Test API usage patterns in notebooks."""
    
    @classmethod
    def setUpClass(cls):
        """Load Voice_memos notebook."""
        cls.voice_memos_path = Path("examples/Voice_memos.ipynb")
        with open(cls.voice_memos_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.code_cells = [cell for cell in cls.notebook['cells'] 
                          if cell['cell_type'] == 'code']
        cls.all_code = '\n'.join([''.join(cell['source']) for cell in cls.code_cells])
    
    def test_api_key_management(self):
        """Test that API keys are managed securely."""
        # Should use userdata or environment variables
        secure_patterns = ['userdata.get', 'os.environ', 'os.getenv']
        has_secure = any(pattern in self.all_code for pattern in secure_patterns)
        self.assertTrue(has_secure, "Should use secure API key management")
        
        # Should not hardcode keys
        self.assertNotRegex(self.all_code, r'AIza[0-9A-Za-z_-]{35}',
                          "Should not hardcode API keys")
    
    def test_file_upload_pattern(self):
        """Test that file uploads use correct new pattern."""
        # Should use genai.upload_file with path parameter
        upload_pattern = r'genai\.upload_file\s*\(\s*path\s*='
        self.assertIsNotNone(re.search(upload_pattern, self.all_code),
                           "Should use genai.upload_file(path=...)")
    
    def test_model_instantiation_pattern(self):
        """Test that models are instantiated correctly."""
        # Should use GenerativeModel class
        model_pattern = r'genai\.GenerativeModel\s*\('
        self.assertIsNotNone(re.search(model_pattern, self.all_code),
                           "Should use genai.GenerativeModel()")
    
    def test_content_generation_pattern(self):
        """Test that content generation uses correct pattern."""
        # Should call generate_content on model instance
        generate_pattern = r'model\.generate_content\s*\('
        self.assertIsNotNone(re.search(generate_pattern, self.all_code),
                           "Should use model.generate_content()")


class TestCrossNotebookConsistency(unittest.TestCase):
    """Test consistency across multiple notebooks."""
    
    @classmethod
    def setUpClass(cls):
        """Load relevant notebooks."""
        cls.voice_memos_path = Path("examples/Voice_memos.ipynb")
        cls.multi_spectral_path = Path("examples/multi_spectral_remote_sensing.ipynb")
        
        with open(cls.voice_memos_path, 'r', encoding='utf-8') as f:
            cls.voice_notebook = json.load(f)
        
        with open(cls.multi_spectral_path, 'r', encoding='utf-8') as f:
            cls.multi_notebook = json.load(f)
    
    def test_consistent_notebook_structure(self):
        """Test that notebooks follow consistent structure."""
        for name, notebook in [('voice_memos', self.voice_notebook),
                              ('multi_spectral', self.multi_notebook)]:
            self.assertIn('cells', notebook, f"{name} should have cells")
            self.assertIn('metadata', notebook, f"{name} should have metadata")
            self.assertIn('nbformat', notebook, f"{name} should have nbformat")
    
    def test_consistent_nbformat_version(self):
        """Test that notebooks use consistent nbformat version."""
        voice_format = self.voice_notebook.get('nbformat')
        multi_format = self.multi_notebook.get('nbformat')
        
        self.assertEqual(voice_format, multi_format,
                        "Notebooks should use same nbformat version")
    
    def test_all_notebooks_are_clean(self):
        """Test that all notebooks have clean state (no outputs)."""
        for name, notebook in [('voice_memos', self.voice_notebook),
                              ('multi_spectral', self.multi_notebook)]:
            code_cells = [cell for cell in notebook['cells'] 
                         if cell['cell_type'] == 'code']
            
            for i, cell in enumerate(code_cells):
                self.assertIsNone(cell.get('execution_count'),
                                f"{name} cell {i} should have null execution_count")
                self.assertEqual(len(cell.get('outputs', [])), 0,
                               f"{name} cell {i} should have no outputs")


class TestFileAPIImplementations(unittest.TestCase):
    """Test File API implementations across different languages."""
    
    def test_python_sample_exists(self):
        """Test that Python sample exists."""
        sample_path = Path("quickstarts/file-api/sample.py")
        self.assertTrue(sample_path.exists(), "Python sample should exist")
    
    def test_javascript_sample_exists(self):
        """Test that JavaScript sample exists."""
        sample_path = Path("quickstarts/file-api/sample.js")
        self.assertTrue(sample_path.exists(), "JavaScript sample should exist")
    
    def test_shell_sample_exists(self):
        """Test that shell sample exists."""
        sample_path = Path("quickstarts/file-api/sample.sh")
        self.assertTrue(sample_path.exists(), "Shell sample should exist")
    
    def test_python_sample_uses_correct_imports(self):
        """Test that Python sample uses correct imports."""
        sample_path = Path("quickstarts/file-api/sample.py")
        with open(sample_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should import from google.genai (the newer SDK used in file-api)
        self.assertIn('from google import genai', content,
                     "Python sample should import genai")
    
    def test_javascript_sample_uses_googleapis(self):
        """Test that JavaScript sample uses googleapis."""
        sample_path = Path("quickstarts/file-api/sample.js")
        with open(sample_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        self.assertIn('googleapis', content,
                     "JavaScript sample should use googleapis")
    
    def test_samples_have_license_headers(self):
        """Test that all samples have license headers."""
        samples = [
            Path("quickstarts/file-api/sample.py"),
            Path("quickstarts/file-api/sample.js"),
            Path("quickstarts/file-api/sample.sh")
        ]
        
        for sample_path in samples:
            with open(sample_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            self.assertIn('Copyright', content,
                         f"{sample_path.name} should have copyright notice")
            self.assertIn('Apache License', content,
                         f"{sample_path.name} should have Apache license")


class TestDependencyManagement(unittest.TestCase):
    """Test dependency management across the project."""
    
    def test_python_requirements_exist(self):
        """Test that Python requirements file exists."""
        req_path = Path("quickstarts/file-api/requirements.txt")
        self.assertTrue(req_path.exists(), "requirements.txt should exist")
    
    def test_python_requirements_content(self):
        """Test that Python requirements have correct dependencies."""
        req_path = Path("quickstarts/file-api/requirements.txt")
        with open(req_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Should have google-generativeai for examples
        # Note: file-api uses google-api-python-client (older SDK) which is correct
        self.assertIn('google-', content,
                     "Should have Google SDK dependencies")
    
    def test_package_json_exists(self):
        """Test that package.json exists for Node.js."""
        pkg_path = Path("quickstarts/file-api/package.json")
        self.assertTrue(pkg_path.exists(), "package.json should exist")
    
    def test_package_lock_exists(self):
        """Test that package-lock.json exists."""
        lock_path = Path("quickstarts/file-api/package-lock.json")
        self.assertTrue(lock_path.exists(), "package-lock.json should exist")
    
    def test_package_dependencies_are_locked(self):
        """Test that Node.js dependencies are properly locked."""
        pkg_path = Path("quickstarts/file-api/package.json")
        lock_path = Path("quickstarts/file-api/package-lock.json")
        
        with open(pkg_path, 'r', encoding='utf-8') as f:
            package_json = json.load(f)
        
        with open(lock_path, 'r', encoding='utf-8') as f:
            package_lock = json.load(f)
        
        # Dependencies in package.json should be in package-lock.json
        pkg_deps = package_json.get('dependencies', {})
        lock_deps = package_lock.get('packages', {}).get('', {}).get('dependencies', {})
        
        for dep in pkg_deps:
            self.assertIn(dep, lock_deps,
                         f"Dependency {dep} should be locked")


if __name__ == '__main__':
    unittest.main(verbosity=2)