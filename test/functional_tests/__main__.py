"""Defines the logic for running all existing unit tests as a module.

    Typical usage example:

    python -m test.functional_tests
"""
# Standard Imports
import sys
# Third Party Imports
# Local Imports
from test.loader import load_and_run_dynamic


if __name__ == '__main__':
    # Run all test cases discovered in this package
    # Exit 0 on success, 1 otherwise
    sys.exit(not load_and_run_dynamic('test/functional_tests'))
