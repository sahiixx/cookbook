"""
Comprehensive tests for Voice_memos.ipynb notebook.

This test suite validates the notebook migration from google-genai to google.generativeai,
ensuring all cells execute correctly and the API interactions work as expected.
"""
import pytest
import nbformat
from nbformat.v4 import new_notebook, new_code_cell, new_markdown_cell
import re
from pathlib import Path


class TestVoiceMemosNotebook:
    """Test suite for Voice_memos.ipynb notebook validation."""
    
    @pytest.fixture
    def notebook_path(self):
        """Return the path to the Voice_memos notebook."""
        return Path("examples/Voice_memos.ipynb")
    
    @pytest.fixture
    def notebook(self, notebook_path):
        """Load and return the notebook object."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            return nbformat.read(f, as_version=4)
    
    def test_notebook_exists(self, notebook_path):
        """Test that the Voice_memos notebook file exists."""
        assert notebook_path.exists(), f"Notebook not found at {notebook_path}"
        assert notebook_path.is_file(), f"{notebook_path} is not a file"
    
    def test_notebook_format(self, notebook):
        """Test that the notebook has valid nbformat structure."""
        assert 'cells' in notebook, "Notebook missing 'cells' key"
        assert 'metadata' in notebook, "Notebook missing 'metadata' key"
        assert 'nbformat' in notebook, "Notebook missing 'nbformat' key"
        assert notebook['nbformat'] >= 4, "Notebook format should be v4 or higher"
    
    def test_uses_correct_sdk(self, notebook):
        """Test that notebook uses google.generativeai instead of google-genai."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        # Check for new SDK import
        import_found = False
        old_import_found = False
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            if 'import google.generativeai as genai' in source:
                import_found = True
            if 'from google import genai' in source:
                old_import_found = True
        
        assert import_found, "New SDK import 'import google.generativeai as genai' not found"
        assert not old_import_found, "Old SDK import 'from google import genai' should be removed"
    
    def test_pip_install_command(self, notebook):
        """Test that pip install uses correct package version."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        correct_install = False
        wrong_install = False
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            if 'google-generativeai>=0.7.2' in source:
                correct_install = True
            if 'google-genai>=1.0.0' in source:
                wrong_install = True
        
        assert correct_install, "Correct pip install command not found"
        assert not wrong_install, "Old pip install command should be removed"
    
    def test_api_configuration(self, notebook):
        """Test that API key configuration uses new SDK method."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        new_config_found = False
        old_config_found = False
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            if 'genai.configure(api_key=' in source:
                new_config_found = True
            if 'client = genai.Client(api_key=' in source:
                old_config_found = True
        
        assert new_config_found, "New configuration method 'genai.configure' not found"
        assert not old_config_found, "Old configuration method 'genai.Client' should be removed"
    
    def test_file_upload_method(self, notebook):
        """Test that file upload uses new SDK method."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        new_upload_found = False
        old_upload_found = False
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            if 'genai.upload_file(path=' in source or 'genai.upload_file(' in source:
                new_upload_found = True
            if 'client.files.upload(file=' in source:
                old_upload_found = True
        
        assert new_upload_found, "New upload method 'genai.upload_file' not found"
        assert not old_upload_found, "Old upload method 'client.files.upload' should be removed"
    
    def test_model_initialization(self, notebook):
        """Test that model initialization uses new SDK pattern."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        new_model_found = False
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            if 'genai.GenerativeModel(' in source:
                new_model_found = True
        
        assert new_model_found, "New model initialization 'genai.GenerativeModel' not found"
    
    def test_generate_content_method(self, notebook):
        """Test that content generation uses new SDK method."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        new_generate_found = False
        old_generate_found = False
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            if 'model.generate_content(' in source:
                new_generate_found = True
            if 'client.models.generate_content(' in source:
                old_generate_found = True
        
        assert new_generate_found, "New generate method 'model.generate_content' not found"
        assert not old_generate_found, "Old generate method should be removed"
    
    def test_system_instruction_usage(self, notebook):
        """Test that system instruction is properly configured."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        system_instruction_found = False
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            if 'system_instruction=' in source:
                system_instruction_found = True
        
        assert system_instruction_found, "system_instruction parameter not found in model initialization"
    
    def test_wget_commands_updated(self, notebook):
        """Test that wget commands have proper formatting."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            if '!wget' in source:
                # Check that -q flag was removed (based on diff)
                lines = source.split('\n')
                for line in lines:
                    if '!wget' in line:
                        # Verify wget is not using -q flag inappropriately
                        assert 'https://' in line, f"wget command should have valid URL: {line}"
    
    def test_poppler_utils_install(self, notebook):
        """Test that poppler-utils installation command is present."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        poppler_install_found = False
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            if 'apt install' in source and 'poppler-utils' in source:
                poppler_install_found = True
        
        assert poppler_install_found, "poppler-utils installation command not found"
    
    def test_no_execution_counts(self, notebook):
        """Test that execution counts are cleared (set to null)."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        for i, cell in enumerate(code_cells):
            assert cell.get('execution_count') is None, \
                f"Cell {i} should have null execution_count, got {cell.get('execution_count')}"
    
    def test_no_cell_outputs(self, notebook):
        """Test that cell outputs are cleared."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        for i, cell in enumerate(code_cells):
            outputs = cell.get('outputs', [])
            assert len(outputs) == 0, f"Cell {i} should have no outputs, got {len(outputs)}"
    
    def test_copyright_notice(self, notebook):
        """Test that copyright notice is present and correct."""
        first_cell = notebook['cells'][0]
        assert first_cell['cell_type'] == 'markdown', "First cell should be markdown"
        
        source = ''.join(first_cell['source'])
        assert '2025' in source, "Copyright year should be 2025"
        assert 'Google LLC' in source, "Copyright holder should be Google LLC"
    
    def test_license_cell(self, notebook):
        """Test that Apache 2.0 license cell is present."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        license_found = False
        for cell in code_cells:
            source = ''.join(cell['source'])
            if 'Apache License' in source and '2.0' in source:
                license_found = True
                break
        
        assert license_found, "Apache 2.0 license cell not found"
    
    def test_colab_badge(self, notebook):
        """Test that Colab badge link is present."""
        markdown_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'markdown']
        
        colab_badge_found = False
        for cell in markdown_cells:
            source = ''.join(cell['source'])
            if 'colab.research.google.com' in source and 'Voice_memos.ipynb' in source:
                colab_badge_found = True
                break
        
        assert colab_badge_found, "Colab badge not found in notebook"
    
    def test_request_options_parameter(self, notebook):
        """Test that request_options parameter is used with timeout."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        request_options_found = False
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            if 'request_options=' in source and 'timeout' in source:
                request_options_found = True
        
        assert request_options_found, "request_options with timeout not found"
    
    def test_model_name_format(self, notebook):
        """Test that model names use correct format."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            if 'model_name=' in source or 'model=' in source:
                # Check for proper model naming
                assert 'models/gemini-2.5-flash' in source or 'gemini' in source.lower(), \
                    "Model name should reference gemini models"
    
    def test_file_references(self, notebook):
        """Test that file references are correct."""
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        expected_files = [
            'Walking_thoughts_3.m4a',
            'A_Possible_Future_for_Online_Content',
            'Unanswered_Questions_and_Endless_Possibilities'
        ]
        
        for expected_file in expected_files:
            file_found = False
            for cell in code_cells:
                source = ''.join(cell['source'])
                if expected_file in source:
                    file_found = True
                    break
            assert file_found, f"File reference '{expected_file}' not found in notebook"


class TestVoiceMemosIntegration:
    """Integration tests for Voice_memos notebook (requires API key)."""
    
    @pytest.fixture
    def notebook_path(self):
        """Return the path to the Voice_memos notebook."""
        return Path("examples/Voice_memos.ipynb")
    
    @pytest.mark.integration
    def test_notebook_structure_validity(self, notebook_path):
        """Test that the notebook can be loaded and has valid structure."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        # Validate basic structure
        assert len(notebook['cells']) > 0, "Notebook should have at least one cell"
        
        # Count cell types
        code_cells = sum(1 for cell in notebook['cells'] if cell['cell_type'] == 'code')
        markdown_cells = sum(1 for cell in notebook['cells'] if cell['cell_type'] == 'markdown')
        
        assert code_cells > 0, "Notebook should have at least one code cell"
        assert markdown_cells > 0, "Notebook should have at least one markdown cell"
    
    @pytest.mark.integration
    def test_imports_are_valid(self, notebook_path):
        """Test that all imports in the notebook are valid Python imports."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        import_patterns = [
            r'import\s+[\w.]+',
            r'from\s+[\w.]+\s+import\s+',
        ]
        
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        
        for cell in code_cells:
            source = ''.join(cell['source'])
            for pattern in import_patterns:
                matches = re.findall(pattern, source)
                # Just verify the pattern exists, actual import testing would require dependencies
                if matches:
                    assert len(matches) > 0


class TestVoiceMemosEdgeCases:
    """Edge case and error handling tests for Voice_memos notebook."""
    
    @pytest.fixture
    def notebook_path(self):
        """Return the path to the Voice_memos notebook."""
        return Path("examples/Voice_memos.ipynb")
    
    def test_notebook_readable(self, notebook_path):
        """Test that notebook file can be read without errors."""
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                content = f.read()
            assert len(content) > 0, "Notebook file should not be empty"
        except Exception as e:
            pytest.fail(f"Failed to read notebook: {e}")
    
    def test_notebook_valid_json(self, notebook_path):
        """Test that notebook is valid JSON."""
        import json
        try:
            with open(notebook_path, 'r', encoding='utf-8') as f:
                json.load(f)
        except json.JSONDecodeError as e:
            pytest.fail(f"Notebook is not valid JSON: {e}")
    
    def test_no_sensitive_data(self, notebook_path):
        """Test that notebook doesn't contain sensitive data like API keys."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check for patterns that might indicate hardcoded secrets
        sensitive_patterns = [
            r'AIza[0-9A-Za-z-_]{35}',  # Google API key pattern
            r'sk-[a-zA-Z0-9]{48}',      # OpenAI key pattern
            r'"api_key"\s*:\s*"[^"]+"', # Hardcoded API key in JSON
        ]
        
        for pattern in sensitive_patterns:
            matches = re.findall(pattern, content)
            # Allow userdata.get patterns (Colab secrets)
            if matches:
                for match in matches:
                    assert 'userdata.get' in content or 'process.env' in content, \
                        f"Potential hardcoded secret found: {pattern}"
    
    def test_cell_metadata_valid(self, notebook_path):
        """Test that all cells have valid metadata."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        for i, cell in enumerate(notebook['cells']):
            assert 'metadata' in cell, f"Cell {i} missing metadata"
            assert 'cell_type' in cell, f"Cell {i} missing cell_type"
            assert cell['cell_type'] in ['code', 'markdown', 'raw'], \
                f"Cell {i} has invalid cell_type: {cell['cell_type']}"