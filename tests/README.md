# Test Suite for Notebook Changes

This directory contains comprehensive unit and integration tests for validating changes to Jupyter notebooks in the repository.

## Test Files

### 1. `test_notebook_api_migration.py`
Tests the API migration in `Voice_memos.ipynb` from the deprecated `google-genai` library to the current `google-generativeai` library.

**Key Test Areas:**
- Correct library imports (`google.generativeai`)
- No deprecated imports (`from google import genai`)
- Use of `genai.configure()` instead of `genai.Client()`
- Use of `genai.upload_file()` instead of `client.files.upload()`
- Use of `genai.GenerativeModel()` for content generation
- Proper parameter names (`path=` for file uploads)
- Cleared execution counts and outputs
- System command improvements (verbose output)

### 2. `test_notebook_content_quality.py`
Tests content quality and spelling in `multi_spectral_remote_sensing.ipynb`.

**Key Test Areas:**
- No typos (specifically "iamges" → "images")
- Consistent terminology
- Proper markdown formatting
- No repeated words
- Correct spelling throughout

### 3. `test_notebook_integration.py`
Integration tests that validate overall notebook structure and API usage patterns.

**Key Test Areas:**
- Valid JSON structure
- Complete workflows (file upload, content generation)
- No deprecated API patterns
- Proper dependency installation
- Package-lock.json integrity

## Running the Tests

### Run All Tests
```bash
cd tests
python3 -m unittest discover -v
```

### Run Specific Test File
```bash
cd tests
python3 -m unittest test_notebook_api_migration -v
python3 -m unittest test_notebook_content_quality -v
python3 -m unittest test_notebook_integration -v
```

### Run Specific Test Class
```bash
cd tests
python3 -m unittest test_notebook_api_migration.TestVoiceMemosNotebookAPIValidation -v
```

### Run Specific Test Method
```bash
cd tests
python3 -m unittest test_notebook_api_migration.TestVoiceMemosNotebookAPIValidation.test_correct_library_import -v
```

## Test Coverage

The test suite covers:

1. **API Migration Validation** (Voice_memos.ipynb)
   - ✅ Correct imports of google-generativeai library
   - ✅ No deprecated google-genai imports
   - ✅ Proper authentication with genai.configure()
   - ✅ File upload using genai.upload_file(path=...)
   - ✅ Content generation with GenerativeModel
   - ✅ No deprecated Client-based patterns
   - ✅ Cleared execution counts
   - ✅ Verbose system commands

2. **Content Quality** (multi_spectral_remote_sensing.ipynb)
   - ✅ No spelling errors (especially "iamges")
   - ✅ Consistent terminology
   - ✅ Proper formatting
   - ✅ Clear headers and structure

3. **Integration Tests**
   - ✅ Valid JSON structure
   - ✅ Complete API workflows
   - ✅ Dependency management
   - ✅ Package integrity

## Expected Test Results

All tests should pass. If any test fails, it indicates:

- **API Migration Tests**: The notebook still uses deprecated API patterns
- **Content Quality Tests**: There are typos or formatting issues in markdown
- **Integration Tests**: The notebook structure or workflow is incomplete

## CI/CD Integration

These tests can be integrated into the existing GitHub Actions workflow:

```yaml
- name: Run notebook tests
  run: |
    cd tests
    python3 -m unittest discover -v
```

## Dependencies

Tests require Python 3.7+ and use only the standard library:
- `unittest` - Testing framework
- `json` - JSON parsing
- `re` - Regular expressions
- `pathlib` - Path handling

No additional dependencies need to be installed.

## Contributing

When adding new notebooks or modifying existing ones:
1. Run the full test suite to ensure no regressions
2. Add new tests for new functionality
3. Update existing tests if API patterns change
4. Ensure all tests pass before submitting PR

## Test Philosophy

These tests follow the principle of **bias for action** as requested:
- Comprehensive coverage of all changes
- Tests for both happy paths and edge cases
- Validation of deprecated pattern removal
- Content quality checks
- Integration validation

The tests are designed to catch:
- API migration issues
- Spelling and grammar errors
- Structural problems
- Deprecated code usage
- Inconsistent patterns