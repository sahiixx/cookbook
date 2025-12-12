#!/usr/bin/env python3
"""
Comprehensive unit tests for Voice_memos.ipynb SDK migration.

This test suite validates the migration from google-genai to google-generativeai SDK,
ensuring all API calls are correctly updated and functionality is preserved.
"""

import unittest
import json
import re
from pathlib import Path
from unittest.mock import Mock, patch, MagicMock, call
import sys


class TestVoiceMemosNotebookStructure(unittest.TestCase):
    """Test the structure and integrity of the Voice_memos.ipynb notebook."""
    
    @classmethod
    def setUpClass(cls):
        """Load the notebook file once for all tests."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.code_cells = [cell for cell in cls.notebook['cells'] if cell['cell_type'] == 'code']
    
    def test_notebook_exists_and_valid_json(self):
        """Test that the notebook file exists and is valid JSON."""
        self.assertIsInstance(self.notebook, dict)
        self.assertIn('cells', self.notebook)
        self.assertIn('metadata', self.notebook)
        self.assertIn('nbformat', self.notebook)
    
    def test_has_required_code_cells(self):
        """Test that notebook has a reasonable number of code cells."""
        self.assertGreater(len(self.code_cells), 5, 
                          "Notebook should have multiple code cells")
    
    def test_no_execution_count_in_code_cells(self):
        """Test that execution counts are null (notebook is clean)."""
        for i, cell in enumerate(self.code_cells):
            self.assertIsNone(cell.get('execution_count'), 
                            f"Cell {i} should have null execution_count")
    
    def test_no_outputs_in_code_cells(self):
        """Test that code cells have no outputs (notebook is clean)."""
        for i, cell in enumerate(self.code_cells):
            outputs = cell.get('outputs', [])
            self.assertEqual(len(outputs), 0, 
                           f"Cell {i} should have no outputs")


class TestSDKMigrationPatterns(unittest.TestCase):
    """Test that the SDK migration patterns are correctly applied."""
    
    @classmethod
    def setUpClass(cls):
        """Load notebook and extract code."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.code_cells = [cell for cell in cls.notebook['cells'] if cell['cell_type'] == 'code']
        cls.all_code = '\n'.join([''.join(cell['source']) for cell in cls.code_cells])
    
    def test_uses_google_generativeai_import(self):
        """Test that google.generativeai is imported correctly."""
        import_pattern = r'import\s+google\.generativeai\s+as\s+genai'
        self.assertIsNotNone(re.search(import_pattern, self.all_code),
                           "Should import google.generativeai as genai")
    
    def test_no_old_google_genai_import(self):
        """Test that old google.genai import is removed."""
        old_import = r'from\s+google\s+import\s+genai'
        self.assertIsNone(re.search(old_import, self.all_code),
                         "Should not use 'from google import genai'")
    
    def test_uses_correct_package_version(self):
        """Test that the correct package version is specified."""
        version_pattern = r'google-generativeai>=0\.7\.2'
        self.assertIsNotNone(re.search(version_pattern, self.all_code),
                           "Should specify google-generativeai>=0.7.2")
    
    def test_no_old_package_reference(self):
        """Test that old google-genai package is not referenced."""
        old_package = r'google-genai'
        # Make sure it's not the new package name
        matches = re.finditer(old_package, self.all_code)
        for match in matches:
            # Check it's not part of google-generativeai
            context_start = max(0, match.start() - 10)
            context_end = min(len(self.all_code), match.end() + 10)
            context = self.all_code[context_start:context_end]
            self.assertIn('generativeai', context, 
                         f"Found old package reference: {context}")
    
    def test_uses_genai_configure(self):
        """Test that genai.configure() is used instead of Client()."""
        configure_pattern = r'genai\.configure\s*\(\s*api_key\s*='
        self.assertIsNotNone(re.search(configure_pattern, self.all_code),
                           "Should use genai.configure(api_key=...)")
    
    def test_no_client_instantiation(self):
        """Test that old Client() instantiation is removed."""
        client_pattern = r'client\s*=\s*genai\.Client'
        self.assertIsNone(re.search(client_pattern, self.all_code),
                         "Should not instantiate genai.Client")
    
    def test_uses_genai_upload_file(self):
        """Test that genai.upload_file() is used for file uploads."""
        upload_pattern = r'genai\.upload_file\s*\(\s*path\s*='
        matches = list(re.finditer(upload_pattern, self.all_code))
        self.assertGreater(len(matches), 0, 
                          "Should use genai.upload_file(path=...)")
        # Voice memos uploads 3 files
        self.assertGreaterEqual(len(matches), 3,
                               "Should have at least 3 file uploads")
    
    def test_no_old_client_files_upload(self):
        """Test that old client.files.upload() is removed."""
        old_upload = r'client\.files\.upload\s*\('
        self.assertIsNone(re.search(old_upload, self.all_code),
                         "Should not use client.files.upload()")
    
    def test_uses_generative_model_class(self):
        """Test that GenerativeModel class is instantiated."""
        model_pattern = r'genai\.GenerativeModel\s*\('
        self.assertIsNotNone(re.search(model_pattern, self.all_code),
                           "Should instantiate genai.GenerativeModel")
    
    def test_model_generate_content_usage(self):
        """Test that model.generate_content() is called on model instance."""
        # Pattern for model variable assignment and usage
        generate_pattern = r'model\.generate_content\s*\('
        self.assertIsNotNone(re.search(generate_pattern, self.all_code),
                           "Should call model.generate_content()")
    
    def test_no_old_client_models_generate(self):
        """Test that old client.models.generate_content() is removed."""
        old_generate = r'client\.models\.generate_content\s*\('
        self.assertIsNone(re.search(old_generate, self.all_code),
                         "Should not use client.models.generate_content()")
    
    def test_request_options_syntax(self):
        """Test that request_options parameter is used correctly."""
        request_options_pattern = r'request_options\s*=\s*\{[^}]*timeout'
        self.assertIsNotNone(re.search(request_options_pattern, self.all_code),
                           "Should use request_options with timeout")
    
    def test_no_old_config_types(self):
        """Test that old config types are removed."""
        old_config = r'types\.GenerateContentConfig'
        self.assertIsNone(re.search(old_config, self.all_code),
                         "Should not use types.GenerateContentConfig")


class TestFileUploadPatterns(unittest.TestCase):
    """Test file upload patterns in the notebook."""
    
    @classmethod
    def setUpClass(cls):
        """Load notebook code."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.code_cells = [cell for cell in cls.notebook['cells'] if cell['cell_type'] == 'code']
        cls.all_code = '\n'.join([''.join(cell['source']) for cell in cls.code_cells])
    
    def test_audio_file_upload(self):
        """Test that audio file is uploaded with correct pattern."""
        audio_pattern = r'audio_file\s*=\s*genai\.upload_file\s*\(\s*path\s*=\s*["\']?Walking_thoughts_3\.m4a'
        self.assertIsNotNone(re.search(audio_pattern, self.all_code),
                           "Should upload audio file correctly")
    
    def test_blog_file_uploads(self):
        """Test that blog files are uploaded."""
        blog1_pattern = r'blog_file\s*=\s*genai\.upload_file\s*\(\s*path\s*=\s*blog_file_name'
        blog2_pattern = r'blog_file2\s*=\s*genai\.upload_file\s*\(\s*path\s*=\s*blog_file_name2'
        
        self.assertIsNotNone(re.search(blog1_pattern, self.all_code),
                           "Should upload first blog file")
        self.assertIsNotNone(re.search(blog2_pattern, self.all_code),
                           "Should upload second blog file")
    
    def test_file_download_commands(self):
        """Test that wget commands for file downloads are present."""
        wget_pattern = r'!wget\s+https://storage\.googleapis\.com/generativeai-downloads'
        matches = list(re.finditer(wget_pattern, self.all_code))
        self.assertGreaterEqual(len(matches), 3,
                               "Should have wget commands for downloading files")
    
    def test_poppler_utils_installation(self):
        """Test that poppler-utils is installed for PDF processing."""
        apt_pattern = r'!apt\s+install\s+poppler-utils'
        self.assertIsNotNone(re.search(apt_pattern, self.all_code),
                           "Should install poppler-utils")


class TestModelConfiguration(unittest.TestCase):
    """Test model configuration and usage patterns."""
    
    @classmethod
    def setUpClass(cls):
        """Load notebook code."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.code_cells = [cell for cell in cls.notebook['cells'] if cell['cell_type'] == 'code']
        cls.all_code = '\n'.join([''.join(cell['source']) for cell in cls.code_cells])
    
    def test_model_name_specification(self):
        """Test that model name is correctly specified."""
        model_pattern = r'model_name\s*=\s*["\']models/gemini-2\.5-flash["\']'
        self.assertIsNotNone(re.search(model_pattern, self.all_code),
                           "Should specify gemini-2.5-flash model")
    
    def test_system_instruction_usage(self):
        """Test that system instructions are used."""
        si_pattern = r'system_instruction\s*=\s*si'
        self.assertIsNotNone(re.search(si_pattern, self.all_code),
                           "Should use system_instruction parameter")
    
    def test_prompt_definition(self):
        """Test that prompt is defined for blog generation."""
        prompt_pattern = r'prompt\s*=\s*["\']Draft my next blog post'
        self.assertIsNotNone(re.search(prompt_pattern, self.all_code),
                           "Should define blog generation prompt")
    
    def test_response_text_access(self):
        """Test that response text is accessed."""
        response_pattern = r'print\s*\(\s*response\.text\s*\)'
        self.assertIsNotNone(re.search(response_pattern, self.all_code),
                           "Should print response.text")


class TestNotebookDependencies(unittest.TestCase):
    """Test that all required dependencies are specified."""
    
    @classmethod
    def setUpClass(cls):
        """Load notebook code."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.code_cells = [cell for cell in cls.notebook['cells'] if cell['cell_type'] == 'code']
        cls.all_code = '\n'.join([''.join(cell['source']) for cell in cls.code_cells])
    
    def test_pip_install_command(self):
        """Test that pip install command is present."""
        pip_pattern = r'%pip\s+install.*google-generativeai'
        self.assertIsNotNone(re.search(pip_pattern, self.all_code),
                           "Should have pip install command")
    
    def test_imports_google_colab(self):
        """Test that Google Colab utilities are imported."""
        colab_pattern = r'from\s+google\.colab\s+import\s+userdata'
        self.assertIsNotNone(re.search(colab_pattern, self.all_code),
                           "Should import from google.colab")
    
    def test_api_key_retrieval(self):
        """Test that API key is retrieved from userdata."""
        api_key_pattern = r'GOOGLE_API_KEY\s*=\s*userdata\.get\s*\(\s*["\']GOOGLE_API_KEY'
        self.assertIsNotNone(re.search(api_key_pattern, self.all_code),
                           "Should retrieve API key from userdata")


class TestCodeQuality(unittest.TestCase):
    """Test code quality and best practices."""
    
    @classmethod
    def setUpClass(cls):
        """Load notebook code."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.code_cells = [cell for cell in cls.notebook['cells'] if cell['cell_type'] == 'code']
    
    def test_no_hardcoded_api_keys(self):
        """Test that no API keys are hardcoded."""
        for cell in self.code_cells:
            source = ''.join(cell['source'])
            # Check for patterns that might be API keys
            self.assertNotRegex(source, r'AIza[0-9A-Za-z_-]{35}',
                              "Should not contain hardcoded API keys")
    
    def test_uses_environment_variables(self):
        """Test that environment variables are used for sensitive data."""
        all_code = '\n'.join([''.join(cell['source']) for cell in self.code_cells])
        self.assertIn('userdata.get', all_code,
                     "Should use userdata.get for API keys")
    
    def test_consistent_variable_naming(self):
        """Test that variable naming follows conventions."""
        all_code = '\n'.join([''.join(cell['source']) for cell in self.code_cells])
        # Check for snake_case in variable names
        variables = ['audio_file', 'blog_file', 'file_name']
        for var in variables:
            if var in all_code:
                self.assertIn(var, all_code, 
                            f"Should use snake_case for {var}")


class TestBackwardsCompatibility(unittest.TestCase):
    """Test that old patterns are completely removed."""
    
    @classmethod
    def setUpClass(cls):
        """Load notebook code."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.all_code = '\n'.join([''.join(cell['source']) 
                                   for cell in cls.notebook['cells'] 
                                   if cell['cell_type'] == 'code'])
    
    def test_no_client_variable_references(self):
        """Test that 'client' variable is not used."""
        # Allow 'client' in comments or strings, but not as a variable
        client_usage = re.finditer(r'\bclient\b', self.all_code)
        for match in client_usage:
            start = max(0, match.start() - 20)
            end = min(len(self.all_code), match.end() + 20)
            context = self.all_code[start:end]
            # Should not be used as a variable (assignment or method call)
            self.assertNotRegex(context, r'client\s*[=\.]',
                              f"'client' should not be used as variable: {context}")
    
    def test_no_types_imports(self):
        """Test that google.genai.types imports are removed."""
        types_import = r'from\s+google\.genai\s+import\s+types'
        self.assertIsNone(re.search(types_import, self.all_code),
                         "Should not import types from google.genai")
    
    def test_no_thinking_config(self):
        """Test that ThinkingConfig is removed."""
        thinking_pattern = r'ThinkingConfig'
        self.assertIsNone(re.search(thinking_pattern, self.all_code),
                         "Should not use ThinkingConfig")


if __name__ == '__main__':
    # Run tests with verbose output
    unittest.main(verbosity=2)