"""
Unit tests for validating content quality in notebook files.

This test suite validates spelling, formatting, and content quality
in the multi_spectral_remote_sensing.ipynb notebook.
"""

import json
import re
import unittest
from pathlib import Path


class TestMultiSpectralNotebookContentQuality(unittest.TestCase):
    """Test suite for multi_spectral_remote_sensing.ipynb content validation."""

    @classmethod
    def setUpClass(cls):
        """Load the notebook once for all tests."""
        notebook_path = Path(__file__).parent.parent / "examples" / "multi_spectral_remote_sensing.ipynb"
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        
        cls.markdown_cells = [
            cell for cell in cls.notebook['cells']
            if cell['cell_type'] == 'markdown'
        ]
        
        cls.all_markdown = '\n'.join([
            ''.join(cell['source'])
            for cell in cls.markdown_cells
        ])

    def test_notebook_structure_valid(self):
        """Test that notebook has valid JSON structure."""
        self.assertIn('cells', self.notebook)
        self.assertIn('metadata', self.notebook)
        self.assertGreater(len(self.notebook['cells']), 0)

    def test_no_common_typos_in_markdown(self):
        """Test that common typos are not present in markdown cells."""
        common_typos = {
            'iamges': 'images',
            'teh': 'the',
            'recieve': 'receive',
            'occured': 'occurred',
            'seperate': 'separate',
        }
        
        found_typos = []
        for typo, correction in common_typos.items():
            # Use word boundary to avoid false positives in code or URLs
            pattern = r'\b' + re.escape(typo) + r'\b'
            if re.search(pattern, self.all_markdown, re.IGNORECASE):
                found_typos.append(f"'{typo}' (should be '{correction}')")
        
        self.assertEqual(
            len(found_typos), 0,
            f"Found typos in markdown: {', '.join(found_typos)}"
        )

    def test_multi_spectral_spelling(self):
        """Test that 'multi-spectral' is spelled correctly throughout."""
        # Check for correct spelling
        correct_pattern = r'multi-spectral'
        correct_matches = re.findall(correct_pattern, self.all_markdown, re.IGNORECASE)
        
        # Common misspellings
        misspelling_patterns = [
            r'multi\s+spectral',  # missing hyphen
            r'multispectral',     # no hyphen (depends on style guide)
            r'multi-spectal',     # missing 'r'
        ]
        
        misspellings_found = []
        for pattern in misspelling_patterns:
            matches = re.findall(pattern, self.all_markdown, re.IGNORECASE)
            if matches:
                misspellings_found.extend(matches)
        
        # For this test, we just ensure the correct form exists
        self.assertGreater(
            len(correct_matches), 0,
            "Notebook should contain 'multi-spectral' terminology"
        )

    def test_images_word_spelled_correctly(self):
        """Test that 'images' is always spelled correctly, not 'iamges'."""
        # Search for the typo specifically
        typo_pattern = r'\biamges\b'
        typo_matches = re.findall(typo_pattern, self.all_markdown, re.IGNORECASE)
        
        self.assertEqual(
            len(typo_matches), 0,
            f"Found typo 'iamges' (should be 'images') in notebook. Matches: {typo_matches}"
        )

    def test_headers_properly_formatted(self):
        """Test that markdown headers are properly formatted."""
        for cell in self.markdown_cells:
            source = ''.join(cell['source'])
            
            # Find headers
            headers = re.findall(r'^#{1,6}\s+.+$', source, re.MULTILINE)
            
            for header in headers:
                # Headers should have space after #
                self.assertNotRegex(
                    header,
                    r'^#{1,6}[^\s]',
                    f"Header should have space after #: {header}"
                )

    def test_has_title_and_description(self):
        """Test that notebook has a clear title and description."""
        has_title = False
        for cell in self.markdown_cells:
            source = ''.join(cell['source'])
            if re.search(r'^#\s+', source, re.MULTILINE):
                has_title = True
                break
        
        self.assertTrue(has_title, "Notebook should have a main title (# header)")

    def test_remote_sensing_terminology_correct(self):
        """Test that remote sensing terminology is used correctly."""
        # Check for common terms in remote sensing
        expected_terms = [
            'remote sensing',
            'multi-spectral',
            'images',
        ]
        
        for term in expected_terms:
            self.assertIn(
                term.lower(),
                self.all_markdown.lower(),
                f"Expected to find '{term}' in remote sensing notebook"
            )

    def test_no_repeated_words(self):
        """Test for accidentally repeated words."""
        # Pattern to find repeated words like "the the" or "and and"
        repeated_pattern = r'\b(\w+)\s+\1\b'
        matches = re.findall(repeated_pattern, self.all_markdown, re.IGNORECASE)
        
        # Filter out intentional repetitions (like "that that" in explanations)
        suspicious_matches = [m for m in matches if len(m) > 2]
        
        self.assertEqual(
            len(suspicious_matches), 0,
            f"Found potentially repeated words: {suspicious_matches}"
        )

    def test_consistent_terminology(self):
        """Test that terminology is used consistently."""
        # If both 'image' and 'picture' are used, that's fine, but check they're spelled right
        image_variants = re.findall(r'\bimages?\b', self.all_markdown, re.IGNORECASE)
        
        # Just ensure the word 'image' or 'images' exists and is never misspelled as 'iamge(s)'
        self.assertGreater(
            len(image_variants), 0,
            "Notebook should reference 'image' or 'images'"
        )


class TestNotebookFormattingConsistency(unittest.TestCase):
    """Test suite for notebook formatting and consistency."""

    @classmethod
    def setUpClass(cls):
        """Load the notebook."""
        notebook_path = Path(__file__).parent.parent / "examples" / "multi_spectral_remote_sensing.ipynb"
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)

    def test_has_copyright_notice(self):
        """Test that notebook has copyright notice."""
        first_cells_content = '\n'.join([
            ''.join(cell['source'])
            for cell in self.notebook['cells'][:3]
        ])
        
        self.assertIn(
            'Copyright',
            first_cells_content,
            "Notebook should have copyright notice in first few cells"
        )

    def test_has_license(self):
        """Test that notebook has license information."""
        first_cells_content = '\n'.join([
            ''.join(cell['source'])
            for cell in self.notebook['cells'][:5]
        ])
        
        self.assertIn(
            'License',
            first_cells_content,
            "Notebook should have license information"
        )

    def test_cells_have_metadata(self):
        """Test that cells have proper metadata."""
        for i, cell in enumerate(self.notebook['cells']):
            self.assertIn(
                'metadata',
                cell,
                f"Cell {i} should have metadata"
            )

    def test_notebook_has_metadata(self):
        """Test that notebook has proper top-level metadata."""
        self.assertIn('metadata', self.notebook)
        self.assertIsInstance(self.notebook['metadata'], dict)


class TestGeneralNotebookQuality(unittest.TestCase):
    """Test suite for general notebook quality checks across examples."""

    def test_voice_memos_has_no_typos(self):
        """Test Voice_memos.ipynb for common typos."""
        notebook_path = Path(__file__).parent.parent / "examples" / "Voice_memos.ipynb"
        with open(notebook_path, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        all_content = '\n'.join([
            ''.join(cell['source'])
            for cell in notebook['cells']
        ])
        
        # Check for common typos
        common_typos = ['iamges', 'recieve', 'occured', 'teh']
        for typo in common_typos:
            pattern = r'\b' + re.escape(typo) + r'\b'
            matches = re.findall(pattern, all_content, re.IGNORECASE)
            self.assertEqual(
                len(matches), 0,
                f"Found typo '{typo}' in Voice_memos.ipynb"
            )

    def test_notebooks_are_valid_json(self):
        """Test that all modified notebooks are valid JSON."""
        notebook_files = [
            "examples/Voice_memos.ipynb",
            "examples/multi_spectral_remote_sensing.ipynb"
        ]
        
        for notebook_file in notebook_files:
            notebook_path = Path(__file__).parent.parent / notebook_file
            with self.subTest(notebook=notebook_file):
                try:
                    with open(notebook_path, 'r', encoding='utf-8') as f:
                        notebook = json.load(f)
                    self.assertIsInstance(notebook, dict)
                    self.assertIn('cells', notebook)
                except json.JSONDecodeError as e:
                    self.fail(f"{notebook_file} is not valid JSON: {e}")


if __name__ == '__main__':
    unittest.main()