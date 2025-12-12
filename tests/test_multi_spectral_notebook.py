"""
Test suite for multi_spectral_remote_sensing.ipynb notebook.

Validates the notebook content and verifies the typo fix.
"""

import json
from pathlib import Path
import unittest


class TestMultiSpectralNotebook(unittest.TestCase):
    """Test suite for multi_spectral_remote_sensing.ipynb."""

    @classmethod
    def setUpClass(cls):
        """Set up test fixtures."""
        cls.notebook_path = Path("examples/multi_spectral_remote_sensing.ipynb")
        if cls.notebook_path.exists():
            with open(cls.notebook_path, 'r', encoding='utf-8') as f:
                cls.notebook_content = json.load(f)
        else:
            cls.notebook_content = None

    def test_notebook_exists(self):
        """Test that the notebook file exists."""
        self.assertTrue(
            self.notebook_path.exists(),
            f"Notebook not found: {self.notebook_path}"
        )

    def test_notebook_valid_structure(self):
        """Test that the notebook has valid structure."""
        if self.notebook_content is None:
            self.skipTest("Notebook not loaded")
        
        self.assertIsInstance(self.notebook_content, dict)
        self.assertIn('cells', self.notebook_content)
        self.assertGreater(len(self.notebook_content['cells']), 0)

    def test_typo_fixed_in_markdown(self):
        """Test that the typo 'iamges' is fixed to 'images'."""
        if self.notebook_content is None:
            self.skipTest("Notebook not loaded")
        
        markdown_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'markdown'
        ]
        
        # Check that the typo is fixed
        typo_found = False
        correct_spelling_found = False
        
        for cell in markdown_cells:
            source = ''.join(cell.get('source', []))
            
            # Look for the specific section about multi-spectral images
            if 'Remote sensing with multi-spectral' in source:
                if 'iamges' in source:
                    typo_found = True
                if 'images' in source:
                    correct_spelling_found = True
        
        self.assertFalse(
            typo_found,
            "Typo 'iamges' should be fixed to 'images'"
        )
        self.assertTrue(
            correct_spelling_found,
            "Correct spelling 'images' should be present"
        )

    def test_no_typos_in_all_markdown_cells(self):
        """Test that common typos are not present in markdown cells."""
        if self.notebook_content is None:
            self.skipTest("Notebook not loaded")
        
        common_typos = [
            'iamges',  # images
            'teh',     # the
            'adn',     # and
            'recieve', # receive
        ]
        
        markdown_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'markdown'
        ]
        
        found_typos = []
        
        for cell in markdown_cells:
            source = ''.join(cell.get('source', [])).lower()
            for typo in common_typos:
                if typo in source:
                    found_typos.append(typo)
        
        self.assertEqual(
            len(found_typos), 0,
            f"Found typos in markdown cells: {found_typos}"
        )

    def test_markdown_heading_structure(self):
        """Test that markdown cells have proper heading structure."""
        if self.notebook_content is None:
            self.skipTest("Notebook not loaded")
        
        markdown_cells = [
            cell for cell in self.notebook_content['cells']
            if cell.get('cell_type') == 'markdown'
        ]
        
        # Should have at least some headings
        heading_count = 0
        
        for cell in markdown_cells:
            source = ''.join(cell.get('source', []))
            if source.strip().startswith('#'):
                heading_count += 1
        
        self.assertGreater(
            heading_count, 0,
            "Notebook should have markdown headings"
        )


if __name__ == '__main__':
    unittest.main()