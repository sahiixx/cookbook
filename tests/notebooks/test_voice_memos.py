#!/usr/bin/env python3
"""
Copyright 2025 Google LLC
Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
    http://www.apache.org/licenses/LICENSE-2.0

Comprehensive tests for Voice_memos.ipynb and multi_spectral_remote_sensing.ipynb
"""

import json
import unittest
from pathlib import Path


class TestVoiceMemosNotebook(unittest.TestCase):
    """Test suite for Voice_memos.ipynb - SDK migration validation."""

    @classmethod
    def setUpClass(cls):
        """Load the notebook file once for all tests."""
        notebook_path = Path(__file__).parent.parent.parent / 'examples' / 'Voice_memos.ipynb'
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.cells = cls.notebook.get('cells', [])

    def test_notebook_structure(self):
        """Test that notebook has valid structure."""
        self.assertIn('cells', self.notebook)
        self.assertIn('metadata', self.notebook)
        self.assertGreater(len(self.cells), 0)

    def test_copyright_header(self):
        """Test that copyright header is present."""
        found = any('Copyright 2025 Google LLC' in ''.join(c.get('source', [])) 
                   for c in self.cells if c.get('cell_type') == 'markdown')
        self.assertTrue(found, "Copyright header should be present")

    def test_google_generativeai_import(self):
        """Test that notebook uses google.generativeai (not google-genai)."""
        found_correct = False
        found_old = False
        for cell in self.cells:
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                if 'import google.generativeai as genai' in source:
                    found_correct = True
                if 'from google import genai' in source:
                    found_old = True
        self.assertTrue(found_correct, "Should import google.generativeai")
        self.assertFalse(found_old, "Should not use old import")

    def test_pip_install_command(self):
        """Test that correct package is being installed."""
        found_correct = False
        found_old = False
        for cell in self.cells:
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                if 'google-generativeai>=0.7.2' in source:
                    found_correct = True
                if 'google-genai>=1.0.0' in source:
                    found_old = True
        self.assertTrue(found_correct, "Should install google-generativeai>=0.7.2")
        self.assertFalse(found_old, "Should not install google-genai")

    def test_api_configuration(self):
        """Test that API is configured correctly."""
        found_configure = False
        found_old_client = False
        for cell in self.cells:
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                if 'genai.configure(api_key=' in source:
                    found_configure = True
                if 'client = genai.Client' in source:
                    found_old_client = True
        self.assertTrue(found_configure, "Should use genai.configure()")
        self.assertFalse(found_old_client, "Should not create client")

    def test_file_upload_api(self):
        """Test that file upload uses correct API."""
        found_correct = False
        found_old = False
        for cell in self.cells:
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                if 'genai.upload_file(path=' in source:
                    found_correct = True
                if 'client.files.upload(file=' in source:
                    found_old = True
        self.assertTrue(found_correct, "Should use genai.upload_file()")
        self.assertFalse(found_old, "Should not use client.files.upload()")

    def test_model_initialization(self):
        """Test that GenerativeModel is used correctly."""
        found_model = False
        found_old = False
        for cell in self.cells:
            if cell.get('cell_type') == 'code':
                source = ''.join(cell.get('source', []))
                if 'genai.GenerativeModel' in source:
                    found_model = True
                if 'client.models.generate_content' in source:
                    found_old = True
        self.assertTrue(found_model, "Should create GenerativeModel")
        self.assertFalse(found_old, "Should not use client.models")

    def test_no_thinking_config(self):
        """Test that old thinking_config is removed."""
        found = any('thinking_config' in ''.join(c.get('source', [])) or 'ThinkingConfig' in ''.join(c.get('source', []))
                   for c in self.cells if c.get('cell_type') == 'code')
        self.assertFalse(found, "Should not use thinking_config")

    def test_request_options_timeout(self):
        """Test that request_options with timeout is present."""
        found = any('request_options' in ''.join(c.get('source', [])) and 'timeout' in ''.join(c.get('source', []))
                   for c in self.cells if c.get('cell_type') == 'code')
        self.assertTrue(found, "Should include request_options with timeout")

    def test_execution_count_cleared(self):
        """Test that execution counts are cleared."""
        for cell in self.cells:
            if cell.get('cell_type') == 'code':
                self.assertIsNone(cell.get('execution_count'), "Execution count should be null")

    def test_outputs_cleared(self):
        """Test that outputs are cleared."""
        for cell in self.cells:
            if cell.get('cell_type') == 'code':
                self.assertEqual(len(cell.get('outputs', [])), 0, "Outputs should be cleared")


class TestMultiSpectralNotebook(unittest.TestCase):
    """Test suite for multi_spectral_remote_sensing.ipynb."""

    @classmethod
    def setUpClass(cls):
        """Load the notebook file."""
        notebook_path = Path(__file__).parent.parent.parent / 'examples' / 'multi_spectral_remote_sensing.ipynb'
        with open(notebook_path, 'r', encoding='utf-8') as f:
            cls.notebook = json.load(f)
        cls.cells = cls.notebook.get('cells', [])

    def test_typo_introduced(self):
        """Test documenting the introduced typo 'iamges'."""
        found = any('multi-spectral iamges' in ''.join(c.get('source', [])) 
                   for c in self.cells if c.get('cell_type') == 'markdown')
        self.assertTrue(found, "Typo 'iamges' present - should be fixed to 'images'")

    def test_notebook_structure(self):
        """Test that notebook has valid structure."""
        self.assertIsInstance(self.notebook, dict)
        self.assertIn('cells', self.notebook)
        self.assertGreater(len(self.cells), 0)


class TestPackageLockJson(unittest.TestCase):
    """Test suite for package-lock.json validity."""

    @classmethod
    def setUpClass(cls):
        """Load the package-lock.json file."""
        lock_path = Path(__file__).parent.parent.parent / 'quickstarts' / 'file-api' / 'package-lock.json'
        with open(lock_path, 'r', encoding='utf-8') as f:
            cls.lock_file = json.load(f)

    def test_valid_json(self):
        """Test that package-lock.json is valid JSON."""
        self.assertIsInstance(self.lock_file, dict)

    def test_required_fields(self):
        """Test that required fields are present."""
        for field in ['name', 'version', 'lockfileVersion', 'requires', 'packages']:
            self.assertIn(field, self.lock_file, f"Should contain {field}")

    def test_lockfile_version(self):
        """Test lockfile version."""
        self.assertEqual(self.lock_file['lockfileVersion'], 3)

    def test_dependencies_present(self):
        """Test that required dependencies are listed."""
        deps = self.lock_file['packages'][''].get('dependencies', {})
        for dep in ['dotenv', 'googleapis', 'mime-types']:
            self.assertIn(dep, deps, f"Should have {dep}")


if __name__ == '__main__':
    unittest.main()