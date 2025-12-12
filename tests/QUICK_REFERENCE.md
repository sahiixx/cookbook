# Quick Reference Guide for Notebook Tests

## Running Tests

```bash
# All tests
cd tests && python3 -m unittest discover -v

# Using test runner script
cd tests && ./run_tests.sh

# Specific file
python3 -m unittest test_notebook_api_migration -v

# Specific class
python3 -m unittest test_notebook_api_migration.TestVoiceMemosNotebookAPIValidation -v

# Specific test
python3 -m unittest test_notebook_api_migration.TestVoiceMemosNotebookAPIValidation.test_correct_library_import -v
```

## Test Files Overview

| File | Purpose | Test Count |
|------|---------|------------|
| `test_notebook_api_migration.py` | API migration validation | 31 tests |
| `test_notebook_content_quality.py` | Content quality checks | 16 tests |
| `test_notebook_integration.py` | Integration workflows | 12 tests |

## Common Test Commands

```bash
# Run tests with verbose output
python3 -m unittest discover -v

# Run tests and stop on first failure
python3 -m unittest discover -f

# Run tests and show local variables on failure
python3 -m unittest discover -v --locals

# Run specific test file
python3 -m unittest test_notebook_api_migration

# List all tests without running
python3 -m unittest discover --list
```

## What Each Test File Validates

###  `test_notebook_api_migration.py`
**Focus:** Voice_memos.ipynb API migration

✓ Correct imports (`google.generativeai`)  
✓ No deprecated imports (`from google import genai`)  
✓ Auth with `genai.configure()`  
✓ File upload with `genai.upload_file(path=...)`  
✓ Model init with `genai.GenerativeModel()`  
✓ No `client.files.upload()` or `client.models.generate_content()`  
✓ Cleared execution counts and outputs  
✓ Proper documentation and structure  

### `test_notebook_content_quality.py`
**Focus:** Content quality in multi_spectral_remote_sensing.ipynb

✓ No spelling errors (especially "iamges" → "images")  
✓ Consistent terminology  
✓ Proper markdown formatting  
✓ Headers formatted correctly  
✓ No repeated words  
✓ Professional documentation standards  

### `test_notebook_integration.py`
**Focus:** End-to-end validation

✓ Valid JSON structure  
✓ Complete workflows  
✓ Proper import patterns  
✓ Resource management  
✓ Package.json integrity  

## Expected Test Failures

Some tests are **expected to fail** on the current branch because they validate issues that need fixing:

### ❌ Voice_memos.ipynb
- `test_outputs_cleared` - Cell outputs need to be cleared

### ❌ multi_spectral_remote_sensing.ipynb  
- `test_images_word_spelled_correctly` - Typo: "iamges" → "images"
- `test_no_common_typos_in_markdown` - Related to above typo
- `test_headers_properly_formatted` - Related to line with typo

## Quick Fixes

### Fix 1: Clear Cell Outputs
```bash
# Using nbconvert
jupyter nbconvert --clear-output --inplace examples/Voice_memos.ipynb

# Or in Jupyter UI: Cell → All Output → Clear
```

### Fix 2: Fix Typo
Edit `examples/multi_spectral_remote_sensing.ipynb` line ~321:
```markdown
## Remote sensing with multi-spectral iamges  # ❌ Wrong
## Remote sensing with multi-spectral images  # ✅ Correct
```

## Test Patterns

### Check for presence
```python
self.assertIn('expected_code', actual_code)
```

### Check for absence
```python
self.assertNotIn('deprecated_code', actual_code)
```

### Regex pattern matching
```python
pattern = r'function\s*\([^)]*\)'
self.assertIsNotNone(re.search(pattern, code))
```

### Multiple alternatives
```python
alternatives = ['option1', 'option2']
found = any(alt in code for alt in alternatives)
self.assertTrue(found)
```

## Assertion Methods

| Method | Use Case |
|--------|----------|
| `assertEqual(a, b)` | Check exact equality |
| `assertIn(a, b)` | Check `a` is in `b` |
| `assertNotIn(a, b)` | Check `a` is not in `b` |
| `assertTrue(x)` | Check `x` is truthy |
| `assertFalse(x)` | Check `x` is falsy |
| `assertIsNone(x)` | Check `x` is None |
| `assertIsNotNone(x)` | Check `x` is not None |
| `assertGreater(a, b)` | Check `a > b` |
| `assertRegex(text, pattern)` | Check regex match |
| `assertNotRegex(text, pattern)` | Check no regex match |

## Debugging Failed Tests

### See full error details
```bash
python3 -m unittest test_file.TestClass.test_method -v
```

### Add print statements
```python
def test_something(self):
    code = self.get_all_code()
    print(f"Code length: {len(code)}")  # Debug output
    self.assertIn('expected', code)
```

### Use Python debugger
```bash
python3 -m pdb -m unittest test_file.TestClass.test_method
```

## File Structure