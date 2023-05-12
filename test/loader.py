"""Defines functionality to assist with automated test case loading and execution.

Execute load_and_run() from the __main__.py of a Python package that implements unittest-based
test cases.

    Typical usage example:

    # File: test/unit_test/__main__.py
    from test.loader import load_and_run

    if __name__ == '__main__':
        load_and_run('test/unit_test')  # Loads and runs all unit tests
"""


# Standard Imports
from os import environ
import unittest
# Third Party Imports
from test import TEST_ENV_VAR_NAME, TEST_VERB_LEVELS
from hobo.disk_operations import validate_directory
from hobo.validation import validate_type
# Local Imports
from tediousstart.tediousstart import execute_test_cases


def determine_verbosity() -> int:
    """Determine the dynamic verbosity based on project environment variables.

    This function will determine desired verbosity based on the environment variable defined
    in test.TEST_ENV_VAR_NAME.  Only integer values contained in test.TEST_VERB_LEVELS will
    be supported.  If the environment variable is missing or unsupported then this function
    returns None.
    """
    # LOCAL VARIABLES
    verb_level = None  # Unit test verbosity level: None indicates default verbosity value

    # DETERMINE ITE
    if TEST_ENV_VAR_NAME in environ:
        try:
            verb_level = int(environ.get(TEST_ENV_VAR_NAME))
            if verb_level not in TEST_VERB_LEVELS:
                verb_level = None
        except ValueError:
            verb_level = None

    # DONE
    return verb_level


def exec_verbose_test_cases(sys_exit: bool = True) -> None:
    """Execute test cases with dynamic verbosity.

    Call this within a module to execute its Test Cases as a stand-alone collection with
    project-defined dynamic verbosity.  Calls execute_test_cases() under the hood after
    using determine_verbosity() to dynamically determine the desired verbosity level.
    If missing, then execute_test_cases() will still be called with its default verbosity value.

    Args:
        sys_exit: Optional; Call sys.exit() when the test cases are complete.  This value is
            passed to unittest.main(exit).

    Raises:
        TypeError: Invalid data type.
    """
    # LOCAL VARIABLES
    verb_level = None  # Unit test verbosity level: None indicates default verbosity value

    # PREPARE
    verb_level = determine_verbosity()

    # LOAD AND RUN
    if isinstance(verb_level, int):
        execute_test_cases(sys_exit=sys_exit, verbosity=verb_level)
    else:
        execute_test_cases(sys_exit=sys_exit)


def load_and_run(dirname: str, verbosity: int = 2) -> bool:
    """Load and run all unittest test cases found within dirname.

    Args:
        dirname: Directory, relative or absolute, to begin searching for test cases.
        verbosity: Optional; Verbosity level passed to unittest.TextTestRunner
            0 (quiet): total numbers of tests executed and the global result
            1 (default): verbosity=0 plus a dot for every successful test or a F for every failure
            2 (verbose): you get the help string of every test and the result

    Returns:
        True if all test cases passed, false otherwise.

    Raises:
        TypeError: Invalid data type.
        ValueError: Empty dirname or unsupported verbosity level.
        FileNotFoundError: Unable to locate dirname.
    """
    # LOCAL VARIABLES
    loader = None       # Test case loading object
    test_suite = None   # Test Suite of "discovered" test cases
    test_runner = None  # Test Runner object to run the test suite and display results

    # INPUT VALIDATION
    # dirname
    validate_directory(dirname, 'dirname', must_exist=True)
    # verbosity
    validate_type(verbosity, 'verbosity', int)
    if verbosity not in [0, 1, 2]:
        raise ValueError(f'Unsupported verbosity level: {verbosity}')

    # LOAD
    loader = unittest.TestLoader()  # Test case loading object
    test_suite = loader.discover(dirname)
    test_runner = unittest.TextTestRunner(verbosity=verbosity)

    # RUN
    return test_runner.run(test_suite).wasSuccessful()


def load_and_run_dynamic(dirname: str) -> bool:
    """Load and run all unittest test cases within dirname with dynamic verbosity.

    Calls load_and_run() under the hood after using determine_verbosity() to dynamically determine
    the desired verbosity level.  If missing, then load_and_run() will still be called with
    its default verbosity value.

    Args:
        dirname: Directory, relative or absolute, to begin searching for test cases.
    """
    # LOCAL VARIABLES
    ret_val = None     # Return value of load_and_run()
    verb_level = None  # Unit test verbosity level: None indicates default verbosity value

    # PREPARE
    verb_level = determine_verbosity()

    # LOAD AND RUN
    if isinstance(verb_level, int):
        ret_val = load_and_run(dirname=dirname, verbosity=verb_level)
    else:
        ret_val = load_and_run(dirname=dirname)

    # DONE
    return ret_val
