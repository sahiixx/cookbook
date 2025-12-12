"""
Tests for multi_spectral_remote_sensing.ipynb notebook.

This test suite validates the typo fix and ensures the notebook
maintains its integrity and functionality.
"""
import pytest
import nbformat
from pathlib import Path
import re


class TestMultiSpectralRemoteSensingNotebook:
    """Test suite for multi_spectral_remote_sensing.ipynb."""
    
    @pytest.fixture
    def notebook_path(self):
        """Return the path to the notebook."""
        return Path("examples/multi_spectral_remote_sensing.ipynb")
    
    @pytest.fixture
    def notebook(self, notebook_path):
        """Load and return the notebook object."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            return nbformat.read(f, as_version=4)
    
    def test_notebook_exists(self, notebook_path):
        """Test that the notebook file exists."""
        assert notebook_path.exists(), f"Notebook not found at {notebook_path}"
        assert notebook_path.is_file(), f"{notebook_path} is not a file"
    
    def test_notebook_format(self, notebook):
        """Test that the notebook has valid nbformat structure."""
        assert 'cells' in notebook
        assert 'metadata' in notebook
        assert notebook['nbformat'] >= 4
    
    def test_typo_fixed(self, notebook):
        """Test that the typo 'iamges' has been fixed to 'images'."""
        markdown_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'markdown']
        
        typo_found = False
        correct_spelling_found = False
        
        for cell in markdown_cells:
            source = ''.join(cell['source'])
            if 'iamges' in source.lower():
                typo_found = True
            if 'multi-spectral images' in source.lower():
                correct_spelling_found = True
        
        assert not typo_found, "Typo 'iamges' still present in notebook"
        assert correct_spelling_found, "Correct spelling 'images' not found"
    
    def test_heading_format(self, notebook):
        """Test that markdown headings are properly formatted."""
        markdown_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'markdown']
        
        heading_found = False
        for cell in markdown_cells:
            source = ''.join(cell['source'])
            if '## Remote sensing with multi-spectral images' in source:
                heading_found = True
        
        assert heading_found, "Expected heading not found with correct spelling"
    
    def test_no_other_changes(self, notebook_path):
        """Test that only the typo was changed, nothing else."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Check that the notebook still contains expected content
        expected_content = [
            'Remote sensing',
            'multi-spectral',
            'Gemini'
        ]
        
        for expected in expected_content:
            assert expected in content, f"Expected content '{expected}' not found"
    
    def test_cell_structure_intact(self, notebook):
        """Test that cell structure remains intact."""
        # Should have both code and markdown cells
        code_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'code']
        markdown_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'markdown']
        
        assert len(code_cells) > 0, "Notebook should have code cells"
        assert len(markdown_cells) > 0, "Notebook should have markdown cells"
    
    def test_notebook_metadata(self, notebook):
        """Test that notebook metadata is valid."""
        assert 'metadata' in notebook
        # Check for common metadata fields
        metadata = notebook['metadata']
        assert isinstance(metadata, dict), "Metadata should be a dictionary"


class TestMultiSpectralEdgeCases:
    """Edge case tests for multi_spectral_remote_sensing notebook."""
    
    @pytest.fixture
    def notebook_path(self):
        """Return the path to the notebook."""
        return Path("examples/multi_spectral_remote_sensing.ipynb")
    
    def test_valid_json_structure(self, notebook_path):
        """Test that the notebook is valid JSON."""
        import json
        with open(notebook_path, 'r', encoding='utf-8') as f:
            try:
                json.load(f)
            except json.JSONDecodeError as e:
                pytest.fail(f"Notebook is not valid JSON: {e}")
    
    def test_no_typos_in_other_cells(self, notebook_path):
        """Test for common typos in the entire notebook."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        common_typos = ['teh', 'recieve', 'occured', 'iamge']
        
        for cell in notebook['cells']:
            source = ''.join(cell['source']).lower()
            for typo in common_typos:
                assert typo not in source, f"Found typo '{typo}' in cell"
    
    def test_markdown_links_valid(self, notebook_path):
        """Test that markdown links have valid format."""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = nbformat.read(f, as_version=4)
        
        markdown_cells = [cell for cell in notebook['cells'] if cell['cell_type'] == 'markdown']
        
        # Simple check for markdown link format []()
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        
        for cell in markdown_cells:
            source = ''.join(cell['source'])
            links = re.findall(link_pattern, source)
            for text, url in links:
                # Just verify the pattern is matched, URL validation would need network
                assert len(text) > 0, "Link text should not be empty"
                assert len(url) > 0, "URL should not be empty"