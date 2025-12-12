# Test Suite for Cookbook Repository

This directory contains comprehensive tests for the cookbook repository, focusing on validating Jupyter notebooks and configuration files.

## Test Files

### Python Tests

1. **test_voice_memos_notebook.py**
   - Validates the Voice_memos.ipynb notebook structure and content
   - Tests API migration from google-genai to google-generativeai
   - Verifies correct usage of new SDK patterns
   - Checks for security best practices (no hardcoded API keys)
   - Validates file upload and model initialization patterns

2. **test_notebook_api_migration.py**
   - Tests API migration patterns across notebooks
   - Validates package version consistency
   - Checks API key handling security
   - Verifies file handling and model initialization patterns
   - Tests for deprecated configuration options

3. **test_multi_spectral_notebook.py**
   - Validates the multi_spectral_remote_sensing.ipynb notebook
   - Verifies typo fixes (iamges -> images)
   - Checks markdown structure and content quality

### JavaScript Tests

4. **quickstarts/file-api/test/lockfile.test.js**
   - Validates package-lock.json structure and integrity
   - Checks dependency consistency
   - Verifies security (HTTPS URLs, no known vulnerabilities)
   - Validates package entries and integrity hashes

## Running Tests

### Python Tests

Run all Python tests:
```bash
python tests/run_tests.py
```

Run individual test files:
```bash
python -m unittest tests.test_voice_memos_notebook
python -m unittest tests.test_notebook_api_migration
python -m unittest tests.test_multi_spectral_notebook
```

Run specific test classes:
```bash
python -m unittest tests.test_voice_memos_notebook.TestVoiceMemosNotebook
python -m unittest tests.test_voice_memos_notebook.TestVoiceMemosNotebookIntegration
```

### JavaScript Tests

First, install testing dependencies (if not already installed):
```bash
cd quickstarts/file-api
npm install --save-dev mocha
```

Run JavaScript tests:
```bash
cd quickstarts/file-api
npx mocha test/lockfile.test.js
```

Or add to package.json:
```json
{
  "scripts": {
    "test": "mocha test/**/*.test.js"
  }
}
```

Then run:
```bash
npm test
```

## Test Coverage

### Voice_memos.ipynb Tests
- ✅ File existence and valid JSON structure
- ✅ Notebook structure validation
- ✅ Import statement migration (google-genai → google-generativeai)
- ✅ Package version updates (>=0.7.2)
- ✅ API configuration (Client → genai.configure)
- ✅ File upload API (client.files.upload → genai.upload_file)
- ✅ Model initialization (GenerativeModel)
- ✅ Content generation pattern
- ✅ No deprecated thinking_config
- ✅ Request options usage
- ✅ System instruction variable
- ✅ Model name format
- ✅ Security: No hardcoded API keys
- ✅ API workflow sequence
- ✅ Parameter validation

### multi_spectral_remote_sensing.ipynb Tests
- ✅ File existence and structure
- ✅ Typo fix validation (iamges → images)
- ✅ Common typo checks
- ✅ Markdown heading structure

### package-lock.json Tests
- ✅ Valid JSON structure
- ✅ Required top-level fields
- ✅ Lockfile version
- ✅ Name and version consistency
- ✅ Dependencies listing
- ✅ Integrity hashes
- ✅ Resolved URLs
- ✅ HTTPS usage
- ✅ Path validation
- ✅ Security checks
- ✅ Version consistency

## Requirements

### Python Requirements
- Python 3.7+
- No external dependencies required (uses stdlib only)

### JavaScript Requirements
- Node.js 14+
- npm (for package management)
- mocha (testing framework)

Install dev dependencies:
```bash
cd quickstarts/file-api
npm install --save-dev mocha
```

## CI/CD Integration

These tests can be integrated into CI/CD pipelines:

### GitHub Actions Example
```yaml
name: Test Notebooks

on: [push, pull_request]

jobs:
  test-python:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-python@v2
        with:
          python-version: '3.9'
      - name: Run Python tests
        run: python tests/run_tests.py

  test-javascript:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: actions/setup-node@v2
        with:
          node-version: '14'
      - name: Install dependencies
        run: cd quickstarts/file-api && npm ci
      - name: Run JavaScript tests
        run: cd quickstarts/file-api && npm test
```

## Contributing

When adding new tests:

1. Follow existing naming conventions: `test_*.py` for Python, `*.test.js` for JavaScript
2. Use descriptive test method names that explain what is being tested
3. Include docstrings for test classes and methods
4. Group related tests in the same test class
5. Use appropriate assertions with clear failure messages
6. Keep tests independent and idempotent
7. Update this README with new test descriptions

## Test Philosophy

These tests follow the principle of **validation over execution**:

- **Jupyter Notebooks**: We validate structure, API patterns, and code quality without executing cells (which may require API keys and external resources)
- **Configuration Files**: We validate syntax, structure, and security without making external calls
- **Focus on Migration**: Tests emphasize correct API migration patterns from old to new SDKs

This approach allows tests to run quickly in CI/CD without requiring:
- API credentials
- External service access
- Long-running notebook execution
- Network connectivity

## Future Enhancements

Potential additions:
- [ ] Notebook execution tests (with mocked API calls)
- [ ] Static code analysis integration
- [ ] Dependency vulnerability scanning
- [ ] Documentation generation from tests
- [ ] Performance benchmarks
- [ ] Integration tests with actual API calls (for local development)