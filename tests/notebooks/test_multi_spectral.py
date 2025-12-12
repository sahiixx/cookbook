"""
Tests for multi_spectral_remote_sensing.ipynb notebook
Validates spelling and content correctness
"""
import pytest
import json
from pathlib import Path


@pytest.fixture
def notebook_path():
    """Return the path to the multi_spectral notebook"""
    return Path("examples/multi_spectral_remote_sensing.ipynb")


@pytest.fixture
def notebook_content(notebook_path):
    """Load and parse the notebook JSON"""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class TestNotebookExists:
    """Test notebook file exists"""
    
    def test_notebook_file_exists(self, notebook_path):
        """Verify the notebook exists"""
        assert notebook_path.exists(), f"Notebook not found at {notebook_path}"


class TestSpelling:
    """Test spelling corrections"""
    
    def test_images_spelling_correct(self, notebook_content):
        """Verify 'images' is spelled correctly, not 'iamges'"""
        cells = notebook_content.get("cells", [])
        
        for cell in cells:
            if cell.get("cell_type") in ["markdown", "code"]:
                source = "".join(cell.get("source", []))
                # Check that the typo doesn't exist
                assert "iamges" not in source.lower(), \
                    "Found typo 'iamges' - should be 'images'"
    
    def test_multi_spectral_images_mentioned(self, notebook_content):
        """Verify 'multi-spectral images' is mentioned correctly"""
        cells = notebook_content.get("cells", [])
        images_mention = False
        
        for cell in cells:
            if cell.get("cell_type") in ["markdown", "code"]:
                source = "".join(cell.get("source", []))
                if "multi-spectral image" in source.lower():
                    images_mention = True
                    break
        
        assert images_mention, "Should mention 'multi-spectral images' correctly"


class TestSectionHeadings:
    """Test section headings"""
    
    def test_has_remote_sensing_section(self, notebook_content):
        """Verify there's a section about remote sensing"""
        cells = notebook_content.get("cells", [])
        section_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "markdown":
                source = "".join(cell.get("source", []))
                if "## Remote sensing with multi-spectral image" in source:
                    section_found = True
                    break
        
        assert section_found, "Should have 'Remote sensing with multi-spectral images' section"


class TestNotebookStructure:
    """Test overall notebook structure"""
    
    def test_is_valid_json(self, notebook_content):
        """Verify notebook is valid JSON"""
        assert isinstance(notebook_content, dict), "Notebook should be valid JSON"
        assert "cells" in notebook_content, "Should have cells"
    
    def test_has_cells(self, notebook_content):
        """Verify notebook has cells"""
        cells = notebook_content.get("cells", [])
        assert len(cells) > 0, "Should have at least one cell"