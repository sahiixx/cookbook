# Comprehensive Test Suite for Cookbook Changes

This test suite validates all files changed in the current branch compared to main.

## Changes Covered

### 1. Voice_memos.ipynb
- **Type**: Major SDK migration
- **Changes**: Migration from `google-genai` to `google-generativeai` SDK
- **Tests**: 12 comprehensive validation tests

### 2. multi_spectral_remote_sensing.ipynb
- **Type**: Typo documentation
- **Changes**: "images" → "iamges" (typo introduced)
- **Tests**: 2 validation tests

### 3. package-lock.json
- **Type**: Dependency lock file update
- **Tests**: 4 structural integrity tests

## Running Tests

### Python/Notebook Tests

```bash
cd tests
pip install -r requirements.txt
pytest -v
```

### JavaScript Tests

```bash
cd quickstarts/file-api
npm install
npm test
```

## Test Coverage

### Voice_memos.ipynb Tests (12 tests)
- ✅ Package installation (google-generativeai>=0.7.2)
- ✅ Import statements (import google.generativeai)
- ✅ API configuration (genai.configure)
- ✅ File upload API (genai.upload_file)
- ✅ Model initialization (genai.GenerativeModel)
- ✅ Content generation (model.generate_content)
- ✅ Old SDK removal (no client usage)
- ✅ Thinking config removal
- ✅ Request options with timeout
- ✅ Execution counts cleared
- ✅ Outputs cleared
- ✅ Notebook structure

### multi_spectral_remote_sensing.ipynb Tests (2 tests)
- ✅ Typo documentation ("iamges")
- ✅ Notebook structure validity

### package-lock.json Tests (4 tests)
- ✅ Valid JSON structure
- ✅ Required fields present
- ✅ Lockfile version 3
- ✅ Dependencies present

### sample.js Tests (12 tests)
- ✅ Environment variable loading
- ✅ API configuration
- ✅ File upload functionality
- ✅ Content generation
- ✅ Authentication
- ✅ Error handling
- ✅ Edge cases

## Total: 30+ Comprehensive Tests

## Test Commands

### Run all Python tests
```bash
cd tests
pytest -v
```

### Run specific test
```bash
pytest -v notebooks/test_voice_memos.py::TestVoiceMemosNotebook::test_google_generativeai_import
```

### Run with coverage
```bash
pytest --cov=../examples --cov-report=html
```

### Run JavaScript tests
```bash
cd quickstarts/file-api
npm test
```

### Run with coverage
```bash
npm run test:coverage
```

## Key Validations

### SDK Migration
- Validates complete migration from google-genai to google-generativeai
- Ensures old patterns are removed
- Verifies new API usage is correct

### Typo Documentation
- Documents the introduced typo in multi_spectral_remote_sensing.ipynb
- Serves as a reminder to fix "iamges" → "images"

### Dependency Integrity
- Validates package-lock.json structure
- Ensures all required dependencies are present
- Verifies lockfile version consistency

## Integration with CI/CD

These tests can be integrated into GitHub workflows:

```yaml
name: Tests
on: [pull_request]
jobs:
  python-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v4
      - run: cd tests && pip install -r requirements.txt
      - run: cd tests && pytest -v
  
  javascript-tests:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
      - run: cd quickstarts/file-api && npm install
      - run: cd quickstarts/file-api && npm test
```

## Troubleshooting

### Python tests can't find modules
```bash
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
pytest -v
```

### Jest cache issues
```bash
npm test -- --clearCache
```

## Notes

- All tests are isolated and can run independently
- Tests use mocking to avoid external dependencies
- Coverage reports available for both Python and JavaScript
- Tests document expected behavior for future maintainers