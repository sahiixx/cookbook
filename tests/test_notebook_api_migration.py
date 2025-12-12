"""
Test suite for validating API migration patterns across notebooks.

Ensures that notebooks properly migrate from google-genai to 
google-generativeai SDK with correct API patterns.
"""

import json
import re
from pathlib import Path
from typing import Dict, List, Tuple
import unittest


class TestNotebookAPIMigration(unittest.TestCase):
    """Test API migration patterns in notebooks."""

    API_MIGRATION_PATTERNS = {
        'old_import': r'from google import genai',
        'new_import': r'import google\.generativeai as genai',
        'old_client': r'client\s*=\s*genai\.Client\(',
        'new_configure': r'genai\.configure\(api_key=',
        'old_upload': r'client\.files\.upload\(file=',
        'new_upload': r'genai\.upload_file\(path=',
        'old_generate': r'client\.models\.generate_content\(',
        'new_model_init': r'genai\.GenerativeModel\(',
        'new_generate': r'model\.generate_content\(',
    }

    def test_voice_memos_migration_complete(self):
        """Test that Voice_memos.ipynb has complete API migration."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        
        if not notebook_path.exists():
            self.skipTest(f"Notebook not found: {notebook_path}")
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        code_cells = [
            ''.join(cell.get('source', []))
            for cell in notebook['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        all_code = '\n'.join(code_cells)
        
        # Check that old patterns are NOT present
        old_patterns_found = []
        for pattern_name in ['old_import', 'old_client', 'old_upload', 'old_generate']:
            if re.search(self.API_MIGRATION_PATTERNS[pattern_name], all_code):
                old_patterns_found.append(pattern_name)
        
        self.assertEqual(
            len(old_patterns_found), 0,
            f"Found old API patterns that should be migrated: {old_patterns_found}"
        )
        
        # Check that new patterns ARE present
        new_patterns_missing = []
        for pattern_name in ['new_import', 'new_configure', 'new_upload', 
                            'new_model_init', 'new_generate']:
            if not re.search(self.API_MIGRATION_PATTERNS[pattern_name], all_code):
                new_patterns_missing.append(pattern_name)
        
        self.assertEqual(
            len(new_patterns_missing), 0,
            f"Missing required new API patterns: {new_patterns_missing}"
        )

    def test_package_version_consistency(self):
        """Test that package versions are consistent."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        
        if not notebook_path.exists():
            self.skipTest(f"Notebook not found: {notebook_path}")
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        code_cells = [
            ''.join(cell.get('source', []))
            for cell in notebook['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        # Check for version specifications
        for cell_code in code_cells:
            # Should not reference old package
            self.assertNotIn(
                'google-genai',
                cell_code,
                "Should not reference old google-genai package"
            )
            
            # If installing generativeai, check version
            if 'google-generativeai' in cell_code:
                # Should specify minimum version
                version_match = re.search(
                    r'google-generativeai>=(\d+\.\d+\.\d+)',
                    cell_code
                )
                if version_match:
                    version = version_match.group(1)
                    major, minor, patch = map(int, version.split('.'))
                    
                    # Should be at least 0.7.2
                    self.assertTrue(
                        (major, minor, patch) >= (0, 7, 2),
                        f"Version should be >= 0.7.2, got {version}"
                    )

    def test_api_key_handling(self):
        """Test that API key handling follows security best practices."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        
        if not notebook_path.exists():
            self.skipTest(f"Notebook not found: {notebook_path}")
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        code_cells = [
            ''.join(cell.get('source', []))
            for cell in notebook['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        for cell_code in code_cells:
            # API key should come from userdata
            if 'GOOGLE_API_KEY' in cell_code and '=' in cell_code:
                self.assertIn(
                    'userdata.get',
                    cell_code,
                    "API key should be retrieved using userdata.get()"
                )
            
            # Should not have hardcoded keys
            self.assertNotRegex(
                cell_code,
                r'api_key\s*=\s*["\'][A-Za-z0-9_-]{30,}["\']',
                "API keys should not be hardcoded"
            )

    def test_file_handling_migration(self):
        """Test that file handling follows new API patterns."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        
        if not notebook_path.exists():
            self.skipTest(f"Notebook not found: {notebook_path}")
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        code_cells = [
            ''.join(cell.get('source', []))
            for cell in notebook['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        for cell_code in code_cells:
            # Check file upload patterns
            if 'upload_file' in cell_code:
                # Should use path parameter
                self.assertIn(
                    'path=',
                    cell_code,
                    "upload_file should use 'path=' parameter"
                )
                
                # Should not use old file parameter
                self.assertNotRegex(
                    cell_code,
                    r'\.upload\(file=',
                    "Should not use old 'file=' parameter syntax"
                )

    def test_model_initialization_pattern(self):
        """Test that model initialization follows new patterns."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        
        if not notebook_path.exists():
            self.skipTest(f"Notebook not found: {notebook_path}")
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        code_cells = [
            ''.join(cell.get('source', []))
            for cell in notebook['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        model_init_found = False
        generate_content_found = False
        
        for cell_code in code_cells:
            # Check for model initialization
            if 'GenerativeModel(' in cell_code:
                model_init_found = True
                
                # Should have model_name parameter
                self.assertIn(
                    'model_name=',
                    cell_code,
                    "GenerativeModel should use 'model_name=' parameter"
                )
            
            # Check for generate_content call on model instance
            if re.search(r'model\.generate_content\(', cell_code):
                generate_content_found = True
        
        self.assertTrue(
            model_init_found,
            "Should initialize model with GenerativeModel()"
        )
        self.assertTrue(
            generate_content_found,
            "Should call generate_content() on model instance"
        )


class TestNotebookCodeQuality(unittest.TestCase):
    """Test code quality and best practices in notebooks."""

    def test_no_deprecated_config_options(self):
        """Test that notebooks don't use deprecated configuration options."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        
        if not notebook_path.exists():
            self.skipTest(f"Notebook not found: {notebook_path}")
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        deprecated_patterns = [
            'thinking_config',
            'ThinkingConfig',
            'thinking_budget',
        ]
        
        code_cells = [
            ''.join(cell.get('source', []))
            for cell in notebook['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        for cell_code in code_cells:
            for pattern in deprecated_patterns:
                self.assertNotIn(
                    pattern,
                    cell_code,
                    f"Should not use deprecated config option: {pattern}"
                )

    def test_timeout_configuration(self):
        """Test that timeouts are properly configured."""
        notebook_path = Path("examples/Voice_memos.ipynb")
        
        if not notebook_path.exists():
            self.skipTest(f"Notebook not found: {notebook_path}")
        
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        code_cells = [
            ''.join(cell.get('source', []))
            for cell in notebook['cells']
            if cell.get('cell_type') == 'code'
        ]
        
        timeout_configured = False
        
        for cell_code in code_cells:
            # Check for request_options with timeout
            if 'request_options' in cell_code and 'timeout' in cell_code:
                timeout_configured = True
                
                # Extract timeout value if possible
                timeout_match = re.search(r'timeout["\']?\s*:\s*(\d+)', cell_code)
                if timeout_match:
                    timeout_value = int(timeout_match.group(1))
                    self.assertGreater(
                        timeout_value, 0,
                        "Timeout should be a positive integer"
                    )
        
        self.assertTrue(
            timeout_configured,
            "Should configure timeout in request_options"
        )


if __name__ == '__main__':
    unittest.main()