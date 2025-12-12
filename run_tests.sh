#!/bin/bash
set -e

echo "======================================"
echo "  Gemini Cookbook Test Suite Runner  "
echo "======================================"
echo ""

# Check for Python tests
if [ -d "tests" ]; then
    echo "→ Running Python/Notebook Tests..."
    pip install -q -r tests/requirements.txt 2>/dev/null || echo "  Dependencies already installed"
    pytest tests/ -v --tb=short || exit 1
    echo "✓ Python tests passed"
    echo ""
fi

# Check for JavaScript tests
if [ -d "quickstarts/file-api/__tests__" ]; then
    echo "→ Running JavaScript Tests..."
    cd quickstarts/file-api
    npm install --silent 2>/dev/null || true
    npm test || exit 1
    echo "✓ JavaScript tests passed"
    cd ../..
    echo ""
fi

echo "======================================"
echo "✓ All tests passed successfully!"
echo "======================================"