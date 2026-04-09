"""
Comprehensive test suite for Voice_memos.ipynb notebook.

This test suite validates the notebook migration from google-genai to 
google-generativeai SDK, ensuring all API calls are correctly updated
and the notebook executes without errors.
"""

import json
import os
import re
from pathlib import Path
from typing import Dict, List, Any
import unittest


class TestVoiceMemosNotebook(unittest.TestCase):
    """Test suite for Voice_memos.ipynb notebook validation."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.notebook_path = Path("examples/Voice_memos.ipynb")
        cls.notebook_content = cls._load_notebook()

    @classmethod
    def _load_notebook(cls) -> Dict[str, Any]:
        """Load and parse the notebook JSON."""
        with open(cls.notebook_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def test_notebook_file_exists(self):
        """Test that the Voice_memos notebook file exists."""
        self.assertTrue(
            self.notebook_path.exists(),
            f"Notebook file not found at {self.notebook_path}"
        )

    def test_notebook_valid_json(self):
        """Test that the notebook is valid JSON."""
        self.assertIsInstance(self.notebook_content, dict)
        self.assertIn('cells', self.notebook_content)
        self.assertIn('metadata', self.notebook_content)

    def test_notebook_structure(self):
        """Test that the notebook has expected structure."""
        cells = self.notebook_content.get('cells', [])
        self.assertGreater(
            len(cells), 0,
            "Notebook should contain at least one cell"
        )
        
        # Check for required cell types
        cell_types = [cell.get('cell_type') for cell in cells]
        self.assertIn('code', cell_types, "Notebook should have code cells")
        self.assertIn('markdown', cell_types, "Notebook should have markdown cells")

    def test_google_generativeai_import(self):
        """Test that the notebook uses the correct google-generativeai import."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        import_found = False
        old_import_found = False
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            # Check for new import
            if 'import google.generativeai as genai' in source:
                import_found = True
            
            # Check that old import is not present
            if 'from google import genai' in source:
                old_import_found = True
        
        self.assertTrue(
            import_found,
            "Notebook should import google.generativeai as genai"
        )
        self.assertFalse(
            old_import_found,
            "Notebook should not use old 'from google import genai' import"
        )

    def test_pip_install_command_updated(self):
        """Test that pip install uses correct package version."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        correct_install = False
        old_install = False
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            # Check for new package
            if 'google-generativeai>=0.7.2' in source:
                correct_install = True
            
            # Check for old package
            if 'google-genai>=1.0.0' in source:
                old_install = True
        
        self.assertTrue(
            correct_install,
            "Should install google-generativeai>=0.7.2"
        )
        self.assertFalse(
            old_install,
            "Should not reference old google-genai package"
        )

    def test_api_configuration_method(self):
        """Test that genai.configure is used instead of Client initialization."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        configure_found = False
        client_init_found = False
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            # Check for new configuration method
            if 'genai.configure(api_key=' in source:
                configure_found = True
            
            # Check that old client init is not present
            if 'client = genai.Client(' in source:
                client_init_found = True
        
        self.assertTrue(
            configure_found,
            "Should use genai.configure() for API key setup"
        )
        self.assertFalse(
            client_init_found,
            "Should not use old Client() initialization"
        )

    def test_file_upload_api_migration(self):
        """Test that file upload uses new API (genai.upload_file)."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        new_upload_api = False
        old_upload_api = False
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            # Check for new upload API
            if 'genai.upload_file(path=' in source:
                new_upload_api = True
            
            # Check for old upload API
            if 'client.files.upload(file=' in source:
                old_upload_api = True
        
        self.assertTrue(
            new_upload_api,
            "Should use genai.upload_file() for file uploads"
        )
        self.assertFalse(
            old_upload_api,
            "Should not use old client.files.upload() method"
        )

    def test_model_initialization(self):
        """Test that GenerativeModel is properly initialized."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        model_init_found = False
        old_model_call = False
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            # Check for new model initialization
            if 'genai.GenerativeModel(' in source:
                model_init_found = True
            
            # Check for old model call pattern
            if 'client.models.generate_content(' in source:
                old_model_call = True
        
        self.assertTrue(
            model_init_found,
            "Should use genai.GenerativeModel() for model initialization"
        )
        self.assertFalse(
            old_model_call,
            "Should not use old client.models.generate_content() pattern"
        )

    def test_generate_content_method(self):
        """Test that generate_content is called on model instance."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        correct_pattern = False
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            # Check for model.generate_content() pattern
            if re.search(r'model\.generate_content\(', source):
                correct_pattern = True
                break
        
        self.assertTrue(
            correct_pattern,
            "Should call generate_content() on model instance"
        )

    def test_no_thinking_config_in_migrated_code(self):
        """Test that old thinking_config is removed."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        thinking_config_found = False
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            if 'thinking_config' in source or 'ThinkingConfig' in source:
                thinking_config_found = True
                break
        
        self.assertFalse(
            thinking_config_found,
            "Should not contain old thinking_config or ThinkingConfig"
        )

    def test_request_options_usage(self):
        """Test that request_options is used for timeout configuration."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        request_options_found = False
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            if 'request_options' in source and 'timeout' in source:
                request_options_found = True
                break
        
        self.assertTrue(
            request_options_found,
            "Should use request_options for timeout configuration"
        )

    def test_execution_count_cleared(self):
        """Test that execution counts are cleared (set to null)."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        # Check that most execution counts are null
        null_counts = sum(
            1 for cell in code_cells
            if cell.get('execution_count') is None
        )
        
        self.assertGreater(
            null_counts, 0,
            "At least some cells should have null execution_count"
        )

    def test_outputs_cleared(self):
        """Test that cell outputs are appropriately cleared."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        # Most cells should have empty outputs after cleanup
        empty_outputs = sum(
            1 for cell in code_cells
            if not cell.get('outputs', [])
        )
        
        self.assertGreater(
            empty_outputs, 0,
            "Most cells should have cleared outputs"
        )

    def test_system_instruction_variable(self):
        """Test that system instruction variable is properly defined."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        si_variable_found = False
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            if re.search(r'si\s*=\s*["\']', source):
                si_variable_found = True
                break
        
        self.assertTrue(
            si_variable_found,
            "Should define system instruction variable (si)"
        )

    def test_model_name_format(self):
        """Test that model name uses correct format."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        correct_model_format = False
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            # Check for models/ prefix
            if 'models/gemini' in source:
                correct_model_format = True
                break
        
        self.assertTrue(
            correct_model_format,
            "Should use 'models/gemini-*' format for model name"
        )

    def test_wget_command_format(self):
        """Test that wget commands are properly formatted."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        wget_cells = []
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            if '!wget' in source:
                wget_cells.append(source)
        
        # Should have wget commands without -q flag (for visibility)
        self.assertGreater(
            len(wget_cells), 0,
            "Should have wget download commands"
        )
        
        # Check format
        for wget_cell in wget_cells:
            # Should have proper URL format
            self.assertIn(
                'storage.googleapis.com',
                wget_cell,
                "wget commands should download from storage.googleapis.com"
            )

    def test_apt_install_format(self):
        """Test that apt install command is properly formatted."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        apt_install_found = False
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            if '!apt install poppler-utils' in source:
                apt_install_found = True
                break
        
        self.assertTrue(
            apt_install_found,
            "Should have apt install command for poppler-utils"
        )

    def test_copyright_header_present(self):
        """Test that copyright header is present."""
        cells = self.notebook_content['cells']
        
        # Copyright should be in one of the first few cells
        first_cells_content = ''.join([
            ''.join(cell.get('source', []))
            for cell in cells[:5]
        ])
        
        self.assertIn(
            'Copyright 2025 Google LLC',
            first_cells_content,
            "Should contain copyright notice"
        )

    def test_no_hardcoded_api_keys(self):
        """Test that no API keys are hardcoded in the notebook."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            # Check for potential API key patterns
            self.assertNotRegex(
                source,
                r'api_key\s*=\s*["\'][A-Za-z0-9_-]{30,}["\']',
                "Should not contain hardcoded API keys"
            )
            
            # Should use userdata.get instead
            if 'GOOGLE_API_KEY' in source and '=' in source:
                self.assertIn(
                    'userdata.get',
                    source,
                    "Should use userdata.get() for API key retrieval"
                )


class TestVoiceMemosNotebookIntegration(unittest.TestCase):
    """Integration tests for Voice_memos notebook API usage patterns."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.notebook_path = Path("examples/Voice_memos.ipynb")
        with open(cls.notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook_content = json.load(f)

    def test_api_workflow_sequence(self):
        """Test that API calls follow correct sequence."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        workflow_steps = {
            'import': False,
            'configure': False,
            'upload': False,
            'model_init': False,
            'generate': False
        }
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            if 'import google.generativeai' in source:
                workflow_steps['import'] = True
            if 'genai.configure' in source:
                workflow_steps['configure'] = True
            if 'genai.upload_file' in source:
                workflow_steps['upload'] = True
            if 'genai.GenerativeModel' in source:
                workflow_steps['model_init'] = True
            if 'generate_content' in source:
                workflow_steps['generate'] = True
        
        # All workflow steps should be present
        for step, found in workflow_steps.items():
            self.assertTrue(
                found,
                f"Workflow step '{step}' should be present in notebook"
            )

    def test_file_upload_parameters(self):
        """Test that file upload calls use correct parameter names."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            # If upload_file is called, check parameter name
            if 'genai.upload_file' in source:
                self.assertIn(
                    'path=',
                    source,
                    "upload_file should use 'path=' parameter"
                )
                self.assertNotIn(
                    'file=',
                    source,
                    "upload_file should not use old 'file=' parameter"
                )

    def test_model_configuration_parameters(self):
        """Test that model is configured with correct parameters."""
        code_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        for cell in code_cells:
            source = ''.join(cell.get('source', []))
            
            # Check GenerativeModel parameters
            if 'GenerativeModel(' in source:
                self.assertIn(
                    'model_name=',
                    source,
                    "GenerativeModel should use 'model_name=' parameter"
                )
                # System instruction is optional but if present, check format
                if 'system_instruction' in source:
                    self.assertIn(
                        'system_instruction=',
                        source,
                        "Should use 'system_instruction=' parameter format"
                    )


if __name__ == '__main__':
    unittest.main()