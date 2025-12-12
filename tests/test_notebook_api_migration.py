"""
Unit tests for validating API migration in Voice_memos.ipynb notebook.

This test suite validates that the notebook correctly uses the google-generativeai
library instead of the deprecated google-genai library.
"""

import json
import re
import unittest
from pathlib import Path


class TestVoiceMemosNotebookAPIValidation(unittest.TestCase):
    """Test suite for Voice_memos.ipynb API migration validation."""

    @classmethod
    def setUpClass(cls):
        """Load the notebook once for all tests."""
        notebook_path = Path(__file__).parent.parent / "examples" / "Voice_memos.ipynb"
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        
        cls.code_cells = [
            cell for cell in cls.notebook['cells'] 
            if cell['cell_type'] == 'code'
        ]
        
        cls.all_code = '\n'.join([
            ''.join(cell['source']) 
            for cell in cls.code_cells
        ])

    def test_notebook_structure_valid(self):
        """Test that notebook has valid JSON structure."""
        self.assertIn('cells', self.notebook)
        self.assertIn('metadata', self.notebook)
        self.assertGreater(len(self.notebook['cells']), 0)

    def test_correct_library_import(self):
        """Test that notebook imports google.generativeai correctly."""
        import_found = False
        for cell in self.code_cells:
            source = ''.join(cell['source'])
            if 'import google.generativeai as genai' in source:
                import_found = True
                break
        
        self.assertTrue(
            import_found,
            "Notebook should import 'google.generativeai as genai'"
        )

    def test_no_deprecated_google_genai_import(self):
        """Test that deprecated google.genai import is not present."""
        deprecated_patterns = [
            r'from google import genai',
            r'import google\.genai',
        ]
        
        for pattern in deprecated_patterns:
            matches = re.findall(pattern, self.all_code)
            self.assertEqual(
                len(matches), 0,
                f"Found deprecated import pattern: {pattern}"
            )

    def test_no_client_initialization(self):
        """Test that deprecated Client initialization is not used."""
        client_patterns = [
            r'client\s*=\s*genai\.Client',
            r'genai\.Client\(',
        ]
        
        for pattern in client_patterns:
            matches = re.findall(pattern, self.all_code)
            self.assertEqual(
                len(matches), 0,
                f"Found deprecated Client pattern: {pattern}. Use genai.configure() instead."
            )

    def test_uses_genai_configure(self):
        """Test that genai.configure() is used for API key setup."""
        configure_found = re.search(
            r'genai\.configure\s*\(\s*api_key\s*=',
            self.all_code
        )
        self.assertIsNotNone(
            configure_found,
            "Notebook should use genai.configure(api_key=...) for authentication"
        )

    def test_uses_genai_upload_file(self):
        """Test that genai.upload_file() is used instead of client.files.upload()."""
        upload_patterns = [
            r'genai\.upload_file\s*\(\s*path\s*=',
        ]
        
        found_count = 0
        for pattern in upload_patterns:
            matches = re.findall(pattern, self.all_code)
            found_count += len(matches)
        
        self.assertGreater(
            found_count, 0,
            "Notebook should use genai.upload_file(path=...) for file uploads"
        )

    def test_no_client_files_upload(self):
        """Test that deprecated client.files.upload() is not used."""
        deprecated_patterns = [
            r'client\.files\.upload',
        ]
        
        for pattern in deprecated_patterns:
            matches = re.findall(pattern, self.all_code)
            self.assertEqual(
                len(matches), 0,
                f"Found deprecated pattern: {pattern}. Use genai.upload_file() instead."
            )

    def test_correct_pip_install_command(self):
        """Test that notebook installs correct google-generativeai package."""
        install_pattern = r'%pip\s+install.*google-generativeai'
        install_found = re.search(install_pattern, self.all_code)
        
        self.assertIsNotNone(
            install_found,
            "Notebook should install 'google-generativeai' package"
        )

    def test_no_deprecated_google_genai_package(self):
        """Test that deprecated google-genai package is not installed."""
        deprecated_pattern = r'%pip\s+install.*["\']google-genai[>=<\s]'
        matches = re.findall(deprecated_pattern, self.all_code)
        
        self.assertEqual(
            len(matches), 0,
            "Notebook should not install deprecated 'google-genai' package"
        )

    def test_uses_generative_model(self):
        """Test that notebook uses genai.GenerativeModel for content generation."""
        model_patterns = [
            r'genai\.GenerativeModel\s*\(',
            r'model\s*=\s*genai\.GenerativeModel',
        ]
        
        found = False
        for pattern in model_patterns:
            if re.search(pattern, self.all_code):
                found = True
                break
        
        self.assertTrue(
            found,
            "Notebook should use genai.GenerativeModel() for model initialization"
        )

    def test_no_client_models_generate_content(self):
        """Test that deprecated client.models.generate_content() is not used."""
        deprecated_pattern = r'client\.models\.generate_content'
        matches = re.findall(deprecated_pattern, self.all_code)
        
        self.assertEqual(
            len(matches), 0,
            "Found deprecated client.models.generate_content(). Use model.generate_content() instead."
        )

    def test_no_google_genai_types_import(self):
        """Test that deprecated google.genai.types import is not present."""
        deprecated_pattern = r'from google\.genai import types'
        matches = re.findall(deprecated_pattern, self.all_code)
        
        self.assertEqual(
            len(matches), 0,
            "Found deprecated 'from google.genai import types' import"
        )

    def test_execution_count_reset(self):
        """Test that all execution counts are reset to null."""
        for i, cell in enumerate(self.code_cells):
            execution_count = cell.get('execution_count')
            self.assertIsNone(
                execution_count,
                f"Code cell {i} should have execution_count set to null, found: {execution_count}"
            )

    def test_outputs_cleared(self):
        """Test that all cell outputs are cleared."""
        for i, cell in enumerate(self.code_cells):
            outputs = cell.get('outputs', [])
            self.assertEqual(
                len(outputs), 0,
                f"Code cell {i} should have empty outputs, found {len(outputs)} outputs"
            )

    def test_file_upload_parameter_format(self):
        """Test that file upload uses correct parameter name 'path'."""
        upload_calls = re.findall(
            r'genai\.upload_file\s*\(\s*([^)]+)\)',
            self.all_code
        )
        
        for call_params in upload_calls:
            self.assertIn(
                'path=',
                call_params,
                f"upload_file should use 'path=' parameter, found: {call_params}"
            )

    def test_wget_commands_present(self):
        """Test that wget commands for downloading files are present."""
        wget_pattern = r'!wget\s+https://storage\.googleapis\.com'
        wget_matches = re.findall(wget_pattern, self.all_code)
        
        self.assertGreater(
            len(wget_matches), 0,
            "Notebook should contain wget commands to download required files"
        )

    def test_poppler_utils_installation(self):
        """Test that poppler-utils installation is present for PDF handling."""
        apt_install_pattern = r'!apt\s+install.*poppler-utils'
        apt_found = re.search(apt_install_pattern, self.all_code)
        
        self.assertIsNotNone(
            apt_found,
            "Notebook should install poppler-utils for PDF processing"
        )

    def test_no_quiet_flags_on_system_commands(self):
        """Test that system commands don't use excessive quiet flags."""
        # The updated version removes -q from wget and apt commands for better visibility
        # This is a best practice for debugging
        source_text = self.all_code
        
        # Check that wget doesn't have -q flag (verbose output preferred in notebooks)
        wget_lines = [line for line in source_text.split('\n') if '!wget' in line]
        for line in wget_lines:
            if 'storage.googleapis.com' in line:
                # The new version should not have -q flag
                self.assertNotIn(
                    ' -q ',
                    line,
                    "wget commands should be verbose for better notebook debugging"
                )


class TestVoiceMemosNotebookContentValidation(unittest.TestCase):
    """Test suite for validating notebook content and structure."""

    @classmethod
    def setUpClass(cls):
        """Load the notebook once for all tests."""
        notebook_path = Path(__file__).parent.parent / "examples" / "Voice_memos.ipynb"
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)

    def test_has_copyright_cell(self):
        """Test that notebook has copyright notice."""
        first_cell = self.notebook['cells'][0]
        source = ''.join(first_cell['source'])
        self.assertIn('Copyright', source)
        self.assertIn('2025', source)
        self.assertIn('Google LLC', source)

    def test_has_license_cell(self):
        """Test that notebook has Apache 2.0 license."""
        # License should be in second cell
        license_found = False
        for cell in self.notebook['cells'][:3]:
            source = ''.join(cell['source'])
            if 'Apache License' in source and '2.0' in source:
                license_found = True
                break
        
        self.assertTrue(license_found, "Notebook should include Apache 2.0 license")

    def test_has_colab_badge(self):
        """Test that notebook has Colab badge for easy opening."""
        colab_found = False
        for cell in self.notebook['cells']:
            if cell['cell_type'] == 'markdown':
                source = ''.join(cell['source'])
                if 'colab.research.google.com' in source:
                    colab_found = True
                    break
        
        self.assertTrue(colab_found, "Notebook should have Colab badge")

    def test_has_title(self):
        """Test that notebook has a title."""
        title_found = False
        for cell in self.notebook['cells']:
            if cell['cell_type'] == 'markdown':
                source = ''.join(cell['source'])
                if '# Voice memos' in source or '#Voice memos' in source:
                    title_found = True
                    break
        
        self.assertTrue(title_found, "Notebook should have 'Voice memos' title")

    def test_has_api_key_setup_instructions(self):
        """Test that notebook includes API key setup instructions."""
        api_key_instructions = False
        for cell in self.notebook['cells']:
            if cell['cell_type'] == 'markdown':
                source = ''.join(cell['source']).lower()
                if 'api key' in source or 'google_api_key' in source:
                    api_key_instructions = True
                    break
        
        self.assertTrue(
            api_key_instructions,
            "Notebook should include API key setup instructions"
        )

    def test_uses_colab_userdata(self):
        """Test that notebook uses Colab userdata for API key."""
        code_cells = [
            ''.join(cell['source'])
            for cell in self.notebook['cells']
            if cell['cell_type'] == 'code'
        ]
        all_code = '\n'.join(code_cells)
        
        self.assertIn(
            'from google.colab import userdata',
            all_code,
            "Notebook should use google.colab.userdata for secrets"
        )
        self.assertIn(
            "userdata.get('GOOGLE_API_KEY')",
            all_code,
            "Notebook should retrieve GOOGLE_API_KEY from userdata"
        )


class TestVoiceMemosNotebookAPIUsagePatterns(unittest.TestCase):
    """Test suite for API usage patterns and best practices."""

    @classmethod
    def setUpClass(cls):
        """Load the notebook code cells."""
        notebook_path = Path(__file__).parent.parent / "examples" / "Voice_memos.ipynb"
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        cls.all_code = '\n'.join([
            ''.join(cell['source'])
            for cell in notebook['cells']
            if cell['cell_type'] == 'code'
        ])

    def test_generate_content_usage(self):
        """Test that generate_content is called correctly."""
        # Should use model.generate_content(), not client.models.generate_content()
        correct_pattern = r'\.generate_content\s*\('
        matches = re.findall(correct_pattern, self.all_code)
        
        self.assertGreater(
            len(matches), 0,
            "Notebook should call generate_content()"
        )

    def test_model_initialization_with_name(self):
        """Test that GenerativeModel is initialized with model name."""
        model_init_pattern = r'GenerativeModel\s*\(\s*model_name\s*='
        matches = re.findall(model_init_pattern, self.all_code)
        
        self.assertGreater(
            len(matches), 0,
            "GenerativeModel should be initialized with model_name parameter"
        )

    def test_response_text_access(self):
        """Test that response.text is used to access generated content."""
        response_text_pattern = r'response\.text'
        matches = re.findall(response_text_pattern, self.all_code)
        
        self.assertGreater(
            len(matches), 0,
            "Notebook should access generated content via response.text"
        )

    def test_file_variables_used_correctly(self):
        """Test that file upload returns are assigned to variables and used."""
        # Check for audio_file, blog_file, blog_file2 variables
        file_vars = ['audio_file', 'blog_file', 'blog_file2']
        
        for var_name in file_vars:
            assignment_pattern = rf'{var_name}\s*=\s*genai\.upload_file'
            assignment = re.search(assignment_pattern, self.all_code)
            
            self.assertIsNotNone(
                assignment,
                f"{var_name} should be assigned result of genai.upload_file()"
            )
            
            # Check that variable is used later
            usage_pattern = rf'[,\[].*{var_name}.*[,\]]'
            usage = re.search(usage_pattern, self.all_code)
            
            self.assertIsNotNone(
                usage,
                f"{var_name} should be used in content generation"
            )

    def test_prompt_and_files_passed_together(self):
        """Test that prompt and files are passed together to generate_content."""
        # Should pass both text prompt and file objects
        generate_call_pattern = r'generate_content\s*\(\s*\[([^\]]+)\]'
        matches = re.findall(generate_call_pattern, self.all_code)
        
        self.assertGreater(
            len(matches), 0,
            "generate_content should be called with list of prompt and files"
        )
        
        # Check that both prompt and file variables are in the list
        for match in matches:
            self.assertIn(
                'prompt',
                match,
                "generate_content should include prompt in contents list"
            )

    def test_system_instruction_used(self):
        """Test that system instruction is provided to model."""
        system_instruction_pattern = r'system_instruction\s*='
        matches = re.search(system_instruction_pattern, self.all_code)
        
        self.assertIsNotNone(
            matches,
            "GenerativeModel should be initialized with system_instruction"
        )

    def test_request_options_used(self):
        """Test that request_options with timeout is specified."""
        request_options_pattern = r'request_options\s*=\s*{[^}]*timeout[^}]*}'
        matches = re.search(request_options_pattern, self.all_code)
        
        self.assertIsNotNone(
            matches,
            "generate_content should specify request_options with timeout"
        )


if __name__ == '__main__':
    unittest.main()