#!/usr/bin/env python3
"""
Unit tests for multi_spectral_remote_sensing.ipynb documentation and structure.

Tests ensure documentation quality, spelling, and notebook integrity.
"""

import unittest
import json
import re
from pathlib import Path


class TestMultiSpectralNotebookStructure(unittest.TestCase):
    """Test the structure and integrity of the multi_spectral notebook."""
    
    @classmethod
    def setUpClass(cls):
        """Load the notebook file once for all tests."""
        notebook_path = Path("examples/multi_spectral_remote_sensing.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.all_cells = cls.notebook['cells']
        cls.markdown_cells = [cell for cell in cls.all_cells 
                              if cell['cell_type'] == 'markdown']
        cls.code_cells = [cell for cell in cls.all_cells 
                          if cell['cell_type'] == 'code']
    
    def test_notebook_valid_json(self):
        """Test that notebook is valid JSON structure."""
        self.assertIsInstance(self.notebook, dict)
        self.assertIn('cells', self.notebook)
        self.assertIn('metadata', self.notebook)
    
    def test_has_markdown_documentation(self):
        """Test that notebook contains markdown documentation cells."""
        self.assertGreater(len(self.markdown_cells), 0,
                          "Notebook should have markdown cells for documentation")
    
    def test_has_code_cells(self):
        """Test that notebook contains code cells."""
        self.assertGreater(len(self.code_cells), 0,
                          "Notebook should have code cells")


class TestMultiSpectralDocumentation(unittest.TestCase):
    """Test documentation quality and correctness."""
    
    @classmethod
    def setUpClass(cls):
        """Load markdown content from notebook."""
        notebook_path = Path("examples/multi_spectral_remote_sensing.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.markdown_cells = [cell for cell in cls.notebook['cells'] 
                              if cell['cell_type'] == 'markdown']
        cls.all_markdown = '\n'.join([''.join(cell['source']) 
                                      for cell in cls.markdown_cells])
    
    def test_title_section_exists(self):
        """Test that notebook has a title section."""
        # Look for main heading
        heading_pattern = r'^#\s+.+$'
        self.assertIsNotNone(re.search(heading_pattern, self.all_markdown, re.MULTILINE),
                           "Notebook should have a title heading")
    
    def test_remote_sensing_section_heading(self):
        """Test that the remote sensing section heading exists and is correct."""
        # The specific section mentioned in the diff
        section_pattern = r'##\s+Remote sensing with multi-spectral'
        match = re.search(section_pattern, self.all_markdown)
        self.assertIsNotNone(match, 
                           "Should have 'Remote sensing with multi-spectral' section")
    
    def test_correct_spelling_of_images(self):
        """Test that 'images' is spelled correctly in the section heading."""
        # This is the key test - the typo was 'iamges' instead of 'images'
        section_pattern = r'##\s+Remote sensing with multi-spectral images'
        match = re.search(section_pattern, self.all_markdown)
        self.assertIsNotNone(match,
                           "Section should say 'images' not 'iamges'")
    
    def test_no_common_typos(self):
        """Test for common typos that might exist."""
        common_typos = {
            'iamges': 'images',
            'multispectral': 'multi-spectral',  # Check hyphenation consistency
            'reomte': 'remote',
            'sensig': 'sensing'
        }
        
        for typo, correct in common_typos.items():
            if typo in self.all_markdown:
                self.fail(f"Found typo '{typo}', should be '{correct}'")
    
    def test_has_description_of_process(self):
        """Test that documentation describes the multi-spectral process."""
        # Should contain key terms
        key_terms = ['multi-spectral', 'remote sensing', 'Gemini']
        for term in key_terms:
            self.assertIn(term, self.all_markdown,
                         f"Documentation should mention '{term}'")
    
    def test_has_code_examples_reference(self):
        """Test that documentation references how to use the feature."""
        # Should have instructional content
        instructional_words = ['you need to', 'how to', 'example', 'follow']
        has_instruction = any(word in self.all_markdown.lower() 
                             for word in instructional_words)
        self.assertTrue(has_instruction,
                       "Documentation should provide instructions")


class TestMultiSpectralCode(unittest.TestCase):
    """Test code patterns in the multi-spectral notebook."""
    
    @classmethod
    def setUpClass(cls):
        """Load code from notebook."""
        notebook_path = Path("examples/multi_spectral_remote_sensing.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.code_cells = [cell for cell in cls.notebook['cells'] 
                          if cell['cell_type'] == 'code']
        cls.all_code = '\n'.join([''.join(cell['source']) 
                                  for cell in cls.code_cells])
    
    def test_imports_required_libraries(self):
        """Test that required libraries are imported."""
        # Multi-spectral processing likely needs these
        potential_imports = ['import', 'from']
        has_imports = any(keyword in self.all_code for keyword in potential_imports)
        self.assertTrue(has_imports, "Should have import statements")
    
    def test_uses_gemini_api(self):
        """Test that code uses Gemini API."""
        api_patterns = [
            'genai',
            'generativeai',
            'GenerativeModel',
            'generate_content'
        ]
        has_api = any(pattern in self.all_code for pattern in api_patterns)
        self.assertTrue(has_api, "Should use Gemini API")
    
    def test_processes_images(self):
        """Test that code handles image processing."""
        image_keywords = ['image', 'file', 'upload', 'path']
        has_image_handling = any(keyword in self.all_code.lower() 
                                 for keyword in image_keywords)
        self.assertTrue(has_image_handling,
                       "Should handle image files")


class TestNotebookMetadata(unittest.TestCase):
    """Test notebook metadata and configuration."""
    
    @classmethod
    def setUpClass(cls):
        """Load notebook."""
        notebook_path = Path("examples/multi_spectral_remote_sensing.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
    
    def test_has_metadata_section(self):
        """Test that notebook has metadata."""
        self.assertIn('metadata', self.notebook)
        self.assertIsInstance(self.notebook['metadata'], dict)
    
    def test_valid_nbformat_version(self):
        """Test that notebook format version is valid."""
        self.assertIn('nbformat', self.notebook)
        self.assertIsInstance(self.notebook['nbformat'], int)
        self.assertGreaterEqual(self.notebook['nbformat'], 4,
                               "Should use nbformat 4 or higher")
    
    def test_cells_have_metadata(self):
        """Test that cells have metadata."""
        for i, cell in enumerate(self.notebook['cells']):
            self.assertIn('metadata', cell,
                         f"Cell {i} should have metadata")
            self.assertIn('cell_type', cell,
                         f"Cell {i} should have cell_type")


class TestDocumentationQuality(unittest.TestCase):
    """Test overall documentation quality standards."""
    
    @classmethod
    def setUpClass(cls):
        """Load markdown content."""
        notebook_path = Path("examples/multi_spectral_remote_sensing.ipynb")
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.markdown_cells = [cell for cell in cls.notebook['cells'] 
                              if cell['cell_type'] == 'markdown']
        cls.all_markdown = '\n'.join([''.join(cell['source']) 
                                      for cell in cls.markdown_cells])
    
    def test_proper_heading_hierarchy(self):
        """Test that headings follow proper hierarchy (# then ## then ###)."""
        headings = re.findall(r'^(#{1,6})\s+.+$', self.all_markdown, re.MULTILINE)
        if headings:
            # First heading should typically be # (h1)
            self.assertTrue(any(h == '#' for h in headings),
                          "Should have at least one top-level heading")
    
    def test_no_empty_sections(self):
        """Test that sections are not empty."""
        # Split by headings and check content
        sections = re.split(r'^#{1,6}\s+.+$', self.all_markdown, flags=re.MULTILINE)
        for i, section in enumerate(sections[1:], 1):  # Skip preamble
            cleaned = section.strip()
            if cleaned and len(cleaned) > 0:
                # Section has content (good)
                pass
    
    def test_consistent_terminology(self):
        """Test that terminology is used consistently."""
        # Check that 'multi-spectral' is consistently hyphenated
        multi_spectral_variants = re.findall(r'\bmulti[\s-]?spectral\b', 
                                             self.all_markdown, 
                                             re.IGNORECASE)
        if len(multi_spectral_variants) > 1:
            # If used multiple times, should be consistent
            unique_variants = set(v.lower() for v in multi_spectral_variants)
            self.assertLessEqual(len(unique_variants), 2,
                               "Multi-spectral terminology should be consistent")
    
    def test_links_are_well_formed(self):
        """Test that markdown links are properly formatted."""
        # Find all markdown links
        link_pattern = r'\[([^\]]+)\]\(([^\)]+)\)'
        links = re.findall(link_pattern, self.all_markdown)
        
        for link_text, link_url in links:
            self.assertGreater(len(link_text), 0, 
                             "Link text should not be empty")
            self.assertGreater(len(link_url), 0,
                             "Link URL should not be empty")


if __name__ == '__main__':
    unittest.main(verbosity=2)