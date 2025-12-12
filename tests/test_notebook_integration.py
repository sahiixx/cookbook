"""
Integration tests for notebook validation and processing.

This test suite validates that notebooks can be properly loaded,
parsed, and that their code cells follow expected patterns.
"""

import json
import re
import unittest
from pathlib import Path
from typing import Dict, List, Any


class NotebookValidator:
    """Helper class for validating Jupyter notebooks."""

    def __init__(self, notebook_path: Path):
        """Initialize validator with notebook path."""
        self.notebook_path = notebook_path
        with open(notebook_path, 'r', encoding='utf-8') as f:
            self.notebook = json.load(f)

    def get_code_cells(self) -> List[Dict[str, Any]]:
        """Get all code cells from notebook."""
        return [cell for cell in self.notebook['cells'] if cell['cell_type'] == 'code']

    def get_markdown_cells(self) -> List[Dict[str, Any]]:
        """Get all markdown cells from notebook."""
        return [cell for cell in self.notebook['cells'] if cell['cell_type'] == 'markdown']

    def get_all_code(self) -> str:
        """Get concatenated code from all code cells."""
        return '\n'.join([''.join(cell['source']) for cell in self.get_code_cells()])

    def get_all_markdown(self) -> str:
        """Get concatenated text from all markdown cells."""
        return '\n'.join([''.join(cell['source']) for cell in self.get_markdown_cells()])

    def find_imports(self) -> List[str]:
        """Find all import statements in the notebook."""
        code = self.get_all_code()
        import_pattern = r'^(?:from\s+[\w.]+\s+import\s+.+|import\s+[\w.]+(?:\s+as\s+\w+)?)'
        return re.findall(import_pattern, code, re.MULTILINE)

    def find_function_calls(self, function_name: str) -> List[str]:
        """Find all calls to a specific function."""
        code = self.get_all_code()
        pattern = rf'{re.escape(function_name)}\s*\([^)]*\)'
        return re.findall(pattern, code)

    def has_pattern(self, pattern: str) -> bool:
        """Check if a pattern exists in the notebook code."""
        code = self.get_all_code()
        return bool(re.search(pattern, code))


class TestVoiceMemosIntegration(unittest.TestCase):
    """Integration tests for Voice_memos.ipynb."""

    @classmethod
    def setUpClass(cls):
        """Set up notebook validator."""
        notebook_path = Path(__file__).parent.parent / "examples" / "Voice_memos.ipynb"
        cls.validator = NotebookValidator(notebook_path)

    def test_can_load_notebook(self):
        """Test that notebook can be loaded as JSON."""
        self.assertIsInstance(self.validator.notebook, dict)
        self.assertIn('cells', self.validator.notebook)

    def test_has_code_and_markdown_cells(self):
        """Test that notebook has both code and markdown cells."""
        code_cells = self.validator.get_code_cells()
        markdown_cells = self.validator.get_markdown_cells()
        
        self.assertGreater(len(code_cells), 0, "Notebook should have code cells")
        self.assertGreater(len(markdown_cells), 0, "Notebook should have markdown cells")

    def test_imports_are_correct(self):
        """Test that imports follow new API patterns."""
        imports = self.validator.find_imports()
        imports_str = '\n'.join(imports)
        
        # Should have google.generativeai import
        self.assertIn('google.generativeai', imports_str)
        
        # Should NOT have deprecated imports
        self.assertNotIn('from google import genai', imports_str)

    def test_api_calls_follow_new_pattern(self):
        """Test that API calls follow new library patterns."""
        # Should use genai.upload_file
        upload_calls = self.validator.find_function_calls('genai.upload_file')
        self.assertGreater(len(upload_calls), 0, "Should have genai.upload_file calls")
        
        # Should use genai.configure
        self.assertTrue(
            self.validator.has_pattern(r'genai\.configure\s*\('),
            "Should have genai.configure() call"
        )
        
        # Should use GenerativeModel
        self.assertTrue(
            self.validator.has_pattern(r'genai\.GenerativeModel\s*\('),
            "Should have genai.GenerativeModel() initialization"
        )

    def test_no_deprecated_patterns(self):
        """Test that deprecated patterns are not present."""
        deprecated_patterns = [
            r'client\s*=\s*genai\.Client',
            r'client\.files\.upload',
            r'client\.models\.generate_content',
            r'from google\.genai import types',
        ]
        
        for pattern in deprecated_patterns:
            self.assertFalse(
                self.validator.has_pattern(pattern),
                f"Deprecated pattern found: {pattern}"
            )

    def test_file_upload_workflow(self):
        """Test that file upload workflow is complete."""
        code = self.validator.get_all_code()
        
        # Should have file name definitions
        self.assertIn('audio_file_name', code)
        self.assertIn('blog_file_name', code)
        
        # Should upload files
        self.assertIn('genai.upload_file', code)
        
        # Should use uploaded files in generation
        self.assertIn('audio_file', code)
        self.assertIn('blog_file', code)

    def test_content_generation_workflow(self):
        """Test that content generation workflow is present."""
        code = self.validator.get_all_code()
        
        # Should have prompt
        self.assertIn('prompt', code)
        
        # Should call generate_content
        self.assertIn('generate_content', code)
        
        # Should access response
        self.assertIn('response', code)

    def test_dependencies_installation(self):
        """Test that required dependencies are installed."""
        code = self.validator.get_all_code()
        
        # Should install google-generativeai
        self.assertIn('google-generativeai', code)
        
        # Should install system dependencies
        self.assertIn('poppler-utils', code)

    def test_external_resources_download(self):
        """Test that external resources are downloaded."""
        code = self.validator.get_all_code()
        
        # Should have wget commands
        self.assertIn('wget', code)
        self.assertIn('storage.googleapis.com', code)


class TestMultiSpectralIntegration(unittest.TestCase):
    """Integration tests for multi_spectral_remote_sensing.ipynb."""

    @classmethod
    def setUpClass(cls):
        """Set up notebook validator."""
        notebook_path = Path(__file__).parent.parent / "examples" / "multi_spectral_remote_sensing.ipynb"
        cls.validator = NotebookValidator(notebook_path)

    def test_can_load_notebook(self):
        """Test that notebook can be loaded as JSON."""
        self.assertIsInstance(self.validator.notebook, dict)
        self.assertIn('cells', self.validator.notebook)

    def test_has_proper_structure(self):
        """Test that notebook has proper structure."""
        code_cells = self.validator.get_code_cells()
        markdown_cells = self.validator.get_markdown_cells()
        
        self.assertGreater(len(code_cells), 0)
        self.assertGreater(len(markdown_cells), 0)

    def test_content_quality(self):
        """Test that content does not have obvious typos."""
        markdown = self.validator.get_all_markdown()
        
        # Check for specific typo
        self.assertNotIn('iamges', markdown.lower(), "Should not contain typo 'iamges'")
        
        # Should contain correct spelling
        self.assertIn('images', markdown.lower(), "Should contain 'images'")

    def test_remote_sensing_content(self):
        """Test that notebook contains remote sensing content."""
        markdown = self.validator.get_all_markdown()
        
        # Should discuss remote sensing
        self.assertIn('remote sensing', markdown.lower())
        
        # Should discuss multi-spectral
        self.assertIn('multi', markdown.lower())
        self.assertIn('spectral', markdown.lower())


class TestPackageLockIntegrity(unittest.TestCase):
    """Test suite for package-lock.json integrity."""

    def test_package_lock_is_valid_json(self):
        """Test that package-lock.json is valid JSON."""
        package_lock_path = Path(__file__).parent.parent / "quickstarts" / "file-api" / "package-lock.json"
        
        try:
            with open(package_lock_path, 'r', encoding='utf-8') as f:
                package_lock = json.load(f)
            
            self.assertIsInstance(package_lock, dict)
            self.assertIn('name', package_lock)
            self.assertIn('version', package_lock)
            self.assertIn('lockfileVersion', package_lock)
        except json.JSONDecodeError as e:
            self.fail(f"package-lock.json is not valid JSON: {e}")

    def test_package_lock_has_required_fields(self):
        """Test that package-lock.json has required fields."""
        package_lock_path = Path(__file__).parent.parent / "quickstarts" / "file-api" / "package-lock.json"
        
        with open(package_lock_path, 'r', encoding='utf-8') as f:
            package_lock = json.load(f)
        
        required_fields = ['name', 'version', 'lockfileVersion', 'requires', 'packages']
        
        for field in required_fields:
            self.assertIn(field, package_lock, f"package-lock.json should have '{field}' field")

    def test_package_lock_dependencies(self):
        """Test that package-lock.json contains expected dependencies."""
        package_lock_path = Path(__file__).parent.parent / "quickstarts" / "file-api" / "package-lock.json"
        
        with open(package_lock_path, 'r', encoding='utf-8') as f:
            package_lock = json.load(f)
        
        # Check that main package has dependencies defined
        if 'packages' in package_lock and '' in package_lock['packages']:
            main_package = package_lock['packages']['']
            self.assertIn('dependencies', main_package)
            
            # Check for expected dependencies
            expected_deps = ['dotenv', 'googleapis', 'mime-types']
            dependencies = main_package['dependencies']
            
            for dep in expected_deps:
                self.assertIn(dep, dependencies, f"Should have dependency: {dep}")


if __name__ == '__main__':
    unittest.main()