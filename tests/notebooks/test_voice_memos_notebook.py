"""
Comprehensive tests for Voice_memos.ipynb notebook.

This test suite validates the notebook structure, API usage patterns,
and ensures the migration from google-genai to google-generativeai is correct.
"""

import json
import re
import pytest
from pathlib import Path


class TestVoiceMemosNotebook:
    """Test suite for Voice_memos.ipynb"""
    
    @pytest.fixture
    def notebook_path(self):
        """Path to the Voice_memos notebook"""
        return Path("examples/Voice_memos.ipynb")
    
    @pytest.fixture
    def notebook_content(self, notebook_path):
        """Load notebook content"""
        with open(notebook_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def test_notebook_exists(self, notebook_path):
        """Test that the Voice_memos notebook file exists"""
        assert notebook_path.exists(), f"Notebook not found at {notebook_path}"
        assert notebook_path.is_file(), f"{notebook_path} is not a file"
    
    def test_notebook_structure(self, notebook_content):
        """Test that notebook has valid structure"""
        assert "cells" in notebook_content, "Notebook missing 'cells' key"
        assert "metadata" in notebook_content, "Notebook missing 'metadata' key"
        assert "nbformat" in notebook_content, "Notebook missing 'nbformat' key"
        assert isinstance(notebook_content["cells"], list), "Cells should be a list"
    
    def test_uses_correct_api_library(self, notebook_content):
        """Test that notebook uses google.generativeai (not google-genai)"""
        code_cells = [cell for cell in notebook_content["cells"] 
                     if cell.get("cell_type") == "code"]
        
        source_text = ""
        for cell in code_cells:
            source = cell.get("source", [])
            if isinstance(source, list):
                source_text += "".join(source)
            else:
                source_text += source
        
        assert "google.generativeai" in source_text or "google-generativeai" in source_text, \
            "Notebook should use google.generativeai library"
        assert "from google import genai" not in source_text, \
            "Notebook should not use deprecated 'from google import genai'"
    
    def test_pip_install_command(self, notebook_content):
        """Test that pip install uses correct package"""
        code_cells = [cell for cell in notebook_content["cells"] 
                     if cell.get("cell_type") == "code"]
        
        pip_commands = []
        for cell in code_cells:
            source = cell.get("source", [])
            source_text = "".join(source) if isinstance(source, list) else source
            if "%pip install" in source_text or "!pip install" in source_text:
                pip_commands.append(source_text)
        
        assert len(pip_commands) > 0, "Notebook should contain pip install command"
        
        found_correct_package = False
        for cmd in pip_commands:
            if "google-generativeai>=0.7.2" in cmd:
                found_correct_package = True
                break
        
        assert found_correct_package, \
            "Notebook should install 'google-generativeai>=0.7.2'"
    
    def test_no_old_client_pattern(self, notebook_content):
        """Test that old client initialization pattern is not used"""
        code_cells = [cell for cell in notebook_content["cells"] 
                     if cell.get("cell_type") == "code"]
        
        for cell in code_cells:
            source = cell.get("source", [])
            source_text = "".join(source) if isinstance(source, list) else source
            
            assert "client = genai.Client" not in source_text, \
                "Notebook should not use deprecated client = genai.Client pattern"
            assert "client.files.upload" not in source_text, \
                "Notebook should not use deprecated client.files.upload pattern"