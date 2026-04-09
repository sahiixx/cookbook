"""
Tests for multi_spectral_remote_sensing.ipynb notebook.
"""

import json
import pytest
from pathlib import Path


class TestMultiSpectralNotebook:
    """Test suite for multi_spectral_remote_sensing.ipynb"""
    
    @pytest.fixture
    def notebook_path(self):
        return Path("examples/multi_spectral_remote_sensing.ipynb")
    
    @pytest.fixture
    def notebook_content(self, notebook_path):
        with open(notebook_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_notebook_exists(self, notebook_path):
        """Test that the notebook file exists"""
        assert notebook_path.exists(), f"Notebook not found at {notebook_path}"
    
    def test_typo_corrected_in_title(self, notebook_content):
        """Test that 'images' is spelled correctly in the section title"""
        markdown_cells = [cell for cell in notebook_content["cells"] 
                         if cell.get("cell_type") == "markdown"]
        
        for cell in markdown_cells:
            source = cell.get("source", [])
            source_text = "".join(source) if isinstance(source, list) else source
            
            if "Remote sensing with multi-spectral" in source_text:
                assert "multi-spectral iamges" not in source_text, \
                    "Typo 'iamges' should be corrected to 'images'"
    
    def test_no_typo_in_entire_notebook(self, notebook_content):
        """Test that the typo 'iamges' is not present anywhere"""
        all_text = []
        
        for cell in notebook_content["cells"]:
            source = cell.get("source", [])
            if isinstance(source, list):
                all_text.extend(source)
            else:
                all_text.append(source)
        
        full_text = "".join(all_text)
        typo_count = full_text.lower().count("iamges")
        assert typo_count == 0, \
            f"Found {typo_count} instance(s) of typo 'iamges' in notebook"