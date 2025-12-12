#!/usr/bin/env python3
"""
Test runner for all unit and integration tests.

This script discovers and runs all tests, providing a comprehensive report.
"""

import unittest
import sys
from pathlib import Path


def run_all_tests():
    """Discover and run all tests."""
    # Create test loader
    loader = unittest.TestLoader()
    
    # Discover all tests in current directory
    start_dir = '.'
    pattern = 'test_*.py'
    
    suite = loader.discover(start_dir, pattern=pattern)
    
    # Run tests with verbose output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Return exit code based on results
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())