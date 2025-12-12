# Test Suite for Google AI Cookbook

Comprehensive tests for the changed files in the cookbook repository.

## Changed Files Tested

1. **examples/Voice_memos.ipynb** - API migration from google-genai to google-generativeai
2. **examples/multi_spectral_remote_sensing.ipynb** - Typo correction ("iamges" → "images")
3. **quickstarts/file-api/package-lock.json** - Lockfile integrity validation

## Running Tests

```bash
# Install dependencies
pip install -r tests/requirements-test.txt

# Run all tests
pytest tests/ -v

# Run specific test file
pytest tests/notebooks/test_voice_memos_notebook.py -v
pytest tests/notebooks/test_multi_spectral_notebook.py -v
pytest tests/lockfiles/test_package_lock.py -v
```

## Test Coverage

- **Voice Memos**: API migration validation, security checks, best practices
- **Multi-Spectral**: Typo correction, spelling quality
- **Package Lock**: JSON validity, structure validation, security checks

## Total Tests: 15+ comprehensive validation tests