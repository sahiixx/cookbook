#!/bin/bash
# Test runner script for notebook validation tests

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

echo "=================================="
echo "Running Notebook Validation Tests"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to run tests with proper error handling
run_test_suite() {
    local test_file=$1
    local test_name=$2
    
    echo "Running $test_name..."
    echo "----------------------------------------"
    
    if python3 -m unittest "$test_file" -v 2>&1; then
        echo -e "${GREEN}✓ $test_name PASSED${NC}"
        return 0
    else
        echo -e "${RED}✗ $test_name FAILED${NC}"
        return 1
    fi
}

# Track overall success
OVERALL_SUCCESS=0

# Run each test suite
echo "1. API Migration Tests"
if ! run_test_suite "test_notebook_api_migration" "API Migration Tests"; then
    OVERALL_SUCCESS=1
fi
echo ""

echo "2. Content Quality Tests"
if ! run_test_suite "test_notebook_content_quality" "Content Quality Tests"; then
    OVERALL_SUCCESS=1
fi
echo ""

echo "3. Integration Tests"
if ! run_test_suite "test_notebook_integration" "Integration Tests"; then
    OVERALL_SUCCESS=1
fi
echo ""

# Summary
echo "=================================="
echo "Test Summary"
echo "=================================="

if [ $OVERALL_SUCCESS -eq 0 ]; then
    echo -e "${GREEN}All tests PASSED ✓${NC}"
    exit 0
else
    echo -e "${RED}Some tests FAILED ✗${NC}"
    exit 1
fi