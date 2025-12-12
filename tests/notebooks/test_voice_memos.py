"""
Tests for Voice_memos.ipynb notebook
Validates the notebook structure, code cells, and API usage patterns
"""
import pytest
import json
import re
from pathlib import Path


@pytest.fixture
def notebook_path():
    """Return the path to the Voice_memos notebook"""
    return Path("examples/Voice_memos.ipynb")


@pytest.fixture
def notebook_content(notebook_path):
    """Load and parse the notebook JSON"""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        return json.load(f)


class TestNotebookStructure:
    """Test the overall structure and metadata of the notebook"""
    
    def test_notebook_exists(self, notebook_path):
        """Verify the notebook file exists"""
        assert notebook_path.exists(), f"Notebook not found at {notebook_path}"
    
    def test_notebook_is_valid_json(self, notebook_content):
        """Verify the notebook is valid JSON"""
        assert isinstance(notebook_content, dict), "Notebook should be a valid JSON object"
        assert "cells" in notebook_content, "Notebook should contain cells"
        assert "metadata" in notebook_content, "Notebook should contain metadata"
    
    def test_notebook_has_cells(self, notebook_content):
        """Verify the notebook contains cells"""
        cells = notebook_content.get("cells", [])
        assert len(cells) > 0, "Notebook should contain at least one cell"
    
    def test_notebook_has_markdown_and_code_cells(self, notebook_content):
        """Verify the notebook has both markdown and code cells"""
        cells = notebook_content.get("cells", [])
        cell_types = [cell.get("cell_type") for cell in cells]
        assert "markdown" in cell_types, "Notebook should have markdown cells"
        assert "code" in cell_types, "Notebook should have code cells"


class TestLicenseAndCopyright:
    """Test copyright and license information"""
    
    def test_has_copyright_notice(self, notebook_content):
        """Verify the notebook has a copyright notice"""
        cells = notebook_content.get("cells", [])
        first_cell = cells[0] if cells else {}
        source = "".join(first_cell.get("source", []))
        assert "Copyright" in source, "First cell should contain copyright notice"
        assert "2025 Google LLC" in source, "Copyright should be for 2025 Google LLC"
    
    def test_has_license_cell(self, notebook_content):
        """Verify the notebook has Apache 2.0 license"""
        cells = notebook_content.get("cells", [])
        # Should be second cell
        if len(cells) > 1:
            license_cell = cells[1]
            source = "".join(license_cell.get("source", []))
            assert "Apache License" in source, "Should contain Apache License reference"
            assert "2.0" in source, "Should be Apache License 2.0"


class TestDependencyInstallation:
    """Test package installation cells"""
    
    def test_installs_google_generativeai(self, notebook_content):
        """Verify the notebook installs the correct google-generativeai package"""
        cells = notebook_content.get("cells", [])
        pip_install_found = False
        correct_version = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "%pip install" in source and "google-generativeai" in source:
                    pip_install_found = True
                    # Check for version >=0.7.2
                    if ">=0.7.2" in source:
                        correct_version = True
        
        assert pip_install_found, "Notebook should install google-generativeai package"
        assert correct_version, "Should install google-generativeai>=0.7.2"
    
    def test_no_old_google_genai_package(self, notebook_content):
        """Verify the notebook doesn't use the old google-genai package"""
        cells = notebook_content.get("cells", [])
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                # Should not have google-genai (without 'ative')
                assert "google-genai" not in source or "google-generativeai" in source, \
                    "Should not reference old google-genai package"


class TestImportStatements:
    """Test import statements in the notebook"""
    
    def test_imports_genai_module(self, notebook_content):
        """Verify the notebook imports google.generativeai as genai"""
        cells = notebook_content.get("cells", [])
        import_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "import google.generativeai as genai" in source:
                    import_found = True
                    break
        
        assert import_found, "Should import google.generativeai as genai"
    
    def test_no_old_client_import(self, notebook_content):
        """Verify the notebook doesn't use old google.genai imports"""
        cells = notebook_content.get("cells", [])
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                assert "from google import genai" not in source, \
                    "Should not use old 'from google import genai' import"


class TestAPIConfiguration:
    """Test API key configuration"""
    
    def test_uses_genai_configure(self, notebook_content):
        """Verify the notebook uses genai.configure() for API key"""
        cells = notebook_content.get("cells", [])
        configure_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "genai.configure(api_key=GOOGLE_API_KEY)" in source:
                    configure_found = True
                    break
        
        assert configure_found, "Should use genai.configure(api_key=...)"
    
    def test_no_old_client_initialization(self, notebook_content):
        """Verify the notebook doesn't use old Client() pattern"""
        cells = notebook_content.get("cells", [])
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                assert "genai.Client(" not in source and "client = genai.Client" not in source, \
                    "Should not use old Client() initialization pattern"


class TestFileUpload:
    """Test file upload functionality"""
    
    def test_uses_genai_upload_file(self, notebook_content):
        """Verify the notebook uses genai.upload_file()"""
        cells = notebook_content.get("cells", [])
        upload_patterns = []
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "genai.upload_file(path=" in source:
                    upload_patterns.append(source)
        
        assert len(upload_patterns) > 0, "Should use genai.upload_file(path=...)"
    
    def test_no_old_files_upload(self, notebook_content):
        """Verify the notebook doesn't use old client.files.upload()"""
        cells = notebook_content.get("cells", [])
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                assert "client.files.upload" not in source, \
                    "Should not use old client.files.upload() pattern"


class TestModelUsage:
    """Test model initialization and usage"""
    
    def test_uses_generative_model_class(self, notebook_content):
        """Verify the notebook uses GenerativeModel class"""
        cells = notebook_content.get("cells", [])
        model_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "genai.GenerativeModel" in source:
                    model_found = True
                    break
        
        assert model_found, "Should use genai.GenerativeModel class"
    
    def test_uses_correct_model_name(self, notebook_content):
        """Verify the notebook uses gemini-2.5-flash model"""
        cells = notebook_content.get("cells", [])
        model_name_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "gemini-2.5-flash" in source:
                    model_name_found = True
                    break
        
        assert model_name_found, "Should reference gemini-2.5-flash model"
    
    def test_no_old_client_models_generate(self, notebook_content):
        """Verify the notebook doesn't use old client.models.generate_content()"""
        cells = notebook_content.get("cells", [])
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                assert "client.models.generate_content" not in source, \
                    "Should not use old client.models.generate_content() pattern"


class TestWgetCommands:
    """Test wget download commands"""
    
    def test_wget_commands_present(self, notebook_content):
        """Verify wget commands are present for downloading files"""
        cells = notebook_content.get("cells", [])
        wget_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "!wget" in source:
                    wget_found = True
                    break
        
        assert wget_found, "Should have wget commands for downloading sample files"
    
    def test_downloads_audio_file(self, notebook_content):
        """Verify the notebook downloads the Walking_thoughts_3.m4a file"""
        cells = notebook_content.get("cells", [])
        audio_download = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "Walking_thoughts_3.m4a" in source and "!wget" in source:
                    audio_download = True
                    break
        
        assert audio_download, "Should download Walking_thoughts_3.m4a audio file"
    
    def test_downloads_pdf_files(self, notebook_content):
        """Verify the notebook downloads PDF files"""
        cells = notebook_content.get("cells", [])
        pdf_downloads = 0
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if ".pdf" in source and "!wget" in source:
                    pdf_downloads += 1
        
        assert pdf_downloads >= 2, "Should download at least 2 PDF files"


class TestPDFConversion:
    """Test PDF to text conversion"""
    
    def test_has_pdftotxt_command(self, notebook_content):
        """Verify the notebook uses pdftotxt for PDF conversion"""
        cells = notebook_content.get("cells", [])
        pdftotxt_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "pdftotxt" in source:
                    pdftotxt_found = True
                    break
        
        assert pdftotxt_found, "Should use pdftotxt command for PDF conversion"
    
    def test_installs_poppler_utils(self, notebook_content):
        """Verify the notebook installs poppler-utils"""
        cells = notebook_content.get("cells", [])
        poppler_install = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "apt install" in source and "poppler-utils" in source:
                    poppler_install = True
                    break
        
        assert poppler_install, "Should install poppler-utils package"


class TestContentGeneration:
    """Test content generation functionality"""
    
    def test_has_generate_content_call(self, notebook_content):
        """Verify the notebook calls generate_content()"""
        cells = notebook_content.get("cells", [])
        generate_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "generate_content" in source:
                    generate_found = True
                    break
        
        assert generate_found, "Should call generate_content() method"
    
    def test_uses_request_options_timeout(self, notebook_content):
        """Verify the notebook uses request_options with timeout"""
        cells = notebook_content.get("cells", [])
        timeout_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "request_options" in source and "timeout" in source:
                    timeout_found = True
                    break
        
        assert timeout_found, "Should use request_options with timeout parameter"
    
    def test_prints_response_text(self, notebook_content):
        """Verify the notebook prints response.text"""
        cells = notebook_content.get("cells", [])
        print_response = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "print(response.text)" in source:
                    print_response = True
                    break
        
        assert print_response, "Should print response.text"


class TestSystemInstruction:
    """Test system instruction usage"""
    
    def test_has_system_instruction(self, notebook_content):
        """Verify the notebook defines system instruction"""
        cells = notebook_content.get("cells", [])
        si_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "si =" in source and ("system_instruction" in source or len(source) > 50):
                    si_found = True
                    break
        
        assert si_found, "Should define system instruction variable"
    
    def test_uses_system_instruction_in_model(self, notebook_content):
        """Verify system instruction is passed to GenerativeModel"""
        cells = notebook_content.get("cells", [])
        si_in_model = False
        
        for cell in cells:
            if cell.get("cell_type") == "code":
                source = "".join(cell.get("source", []))
                if "GenerativeModel" in source and "system_instruction=si" in source:
                    si_in_model = True
                    break
        
        assert si_in_model, "Should pass system_instruction to GenerativeModel"


class TestCodeCellExecutionCounts:
    """Test that execution counts are removed for clean notebooks"""
    
    def test_execution_counts_are_null(self, notebook_content):
        """Verify code cells have null execution_count for clean notebooks"""
        cells = notebook_content.get("cells", [])
        code_cells = [c for c in cells if c.get("cell_type") == "code"]
        
        # All code cells should have null execution_count
        for cell in code_cells:
            exec_count = cell.get("execution_count")
            assert exec_count is None, \
                f"Code cell should have null execution_count for clean notebooks, got {exec_count}"


class TestOutputsCleaned:
    """Test that outputs are cleaned from code cells"""
    
    def test_code_cells_have_empty_outputs(self, notebook_content):
        """Verify code cells have empty outputs array"""
        cells = notebook_content.get("cells", [])
        code_cells = [c for c in cells if c.get("cell_type") == "code"]
        
        for cell in code_cells:
            outputs = cell.get("outputs", [])
            assert outputs == [], \
                f"Code cell outputs should be empty array, got {outputs}"


class TestColabBadge:
    """Test Colab badge presence"""
    
    def test_has_colab_badge(self, notebook_content):
        """Verify the notebook has a Colab badge"""
        cells = notebook_content.get("cells", [])
        colab_badge_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "markdown":
                source = "".join(cell.get("source", []))
                if "colab.research.google.com" in source and "badge" in source.lower():
                    colab_badge_found = True
                    break
        
        assert colab_badge_found, "Should have a Colab badge link"


class TestTitle:
    """Test notebook title"""
    
    def test_has_title(self, notebook_content):
        """Verify the notebook has a title"""
        cells = notebook_content.get("cells", [])
        title_found = False
        
        for cell in cells:
            if cell.get("cell_type") == "markdown":
                source = "".join(cell.get("source", []))
                if "# Voice memos" in source or "#Voice memos" in source:
                    title_found = True
                    break
        
        assert title_found, "Should have 'Voice memos' as title"