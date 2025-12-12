#!/usr/bin/env python3
"""
Test runner for notebook validation tests.

Usage:
    python tests/run_tests.py
"""

import sys
import unittest
from pathlib import Path

# Add tests directory to path
tests_dir = Path(__file__).parent
sys.path.insert(0, str(tests_dir))


def run_all_tests():
    """Discover and run all tests."""
    loader = unittest.TestLoader()
    start_dir = tests_dir
    suite = loader.discover(start_dir, pattern='test_*.py')
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return 0 if result.wasSuccessful() else 1


if __name__ == '__main__':
    sys.exit(run_all_tests())