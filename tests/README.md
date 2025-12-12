# Test Suite for Gemini Cookbook

Comprehensive tests for changed files in the current branch.

## Quick Start

```bash
# Run all tests
./run_tests.sh

# Or individually:
pytest tests/ -v                  # Python tests
cd quickstarts/file-api && npm test  # JavaScript tests
```

## Test Files

- `tests/notebooks/test_voice_memos.py` - SDK migration validation (40+ tests)
- `tests/notebooks/test_multi_spectral_remote_sensing.py` - Typo fix validation (15+ tests)
- `tests/quickstarts/test_package_lock.py` - Package lock validation (50+ tests)
- `quickstarts/file-api/__tests__/sample.test.js` - JS code tests (50+ tests)

## Test Coverage

### Voice Memos Notebook
✓ SDK migration (google-genai → google.generativeai)
✓ Import statements, API configuration, file uploads
✓ Model initialization and content generation
✓ Security checks (no hardcoded secrets)

### Multi-Spectral Notebook
✓ Typo fix validation (iamges → images)
✓ Structure integrity checks

### Package Lock
✓ JSON schema validation (npm v3 format)
✓ Dependency integrity and consistency
✓ Version compatibility checks

### JavaScript Sample
✓ Environment configuration and API setup
✓ File upload and content generation
✓ Error handling and edge cases
✓ Comprehensive mocking (no actual API calls)

## Requirements

**Python**: pytest, nbformat, jsonschema, google-generativeai
**JavaScript**: jest

Install with:
```bash
pip install -r tests/requirements.txt
cd quickstarts/file-api && npm install --save-dev jest
```

## CI/CD

Skip integration tests in CI:
```bash
pytest tests/ -m "not integration"
```