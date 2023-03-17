"""Functionally test TediousFuncTest.run_test() method.

Functionally test the TediousFuncTest.run_test() method's new optional argument by:
    * Creating and storing raw output (as a functional test would do)
    * ???
    * Call the run_test() method with test input
    * Validate the results by ...???

NOTE: These functional test cases do *NOT* use all aspects of TediousFuncTest().  Rather, this
      test framework shunts around the established framework, only using the pieces it needs to.
      E.g., these test cases do *NOT* ???.  Rather, a local method calls the pieces/
      parts of run_test() needed for this framework.

Run the test cases defined in this module using any of the example commands below:

    Usage:
    python -m unittest                                             # Run *ALL* test cases
    python -m unittest -k TestTFTRunTest                           # Match this test class
    python -m test.functional_tests                                # Run all functional tests
    python -m test.functional_tests.test_tediousfunctest_run_test  # Run just these tests
"""

# Standard Imports
from typing import Any
# Third Party Imports
# Local Imports
from tediousstart.tediousstart import execute_test_cases
from test.functional_tests.test_tediousfunctest import TestTFT


class TestTFTRunTest(TestTFT):
    """TestTFTRunTest functional test class.

    This class provides base functionality to run NEBS functional tests for
    TediousFuncTest.run_test().
    """

    def add_test_failure(self, failure_msg: str) -> None:
        """Add a Test Case failure message to the TediousFuncTest object being tested.

        Use this method to add potential output.  Many test cases will want want to add example
        errors to test the formatting of the verbose printing.

        Args:
            failure_msg: Non-empty string containing a failure message.

        Returns:
            None

        Raises:
            None.  Calls self.fail() instead.
        """
        # INPUT VALIDATION
        # We're not testing self._tft_obj._add_test_failure() here so let's ensure we give it
        # good input.
        self._validate_string(failure_msg, 'failure_msg')

        # ADD IT
        self._tft_obj._add_test_failure(failure_msg=failure_msg)

    def run_this_test(self) -> None:
        """Defines a specific technique of executing this test.

        Overrides the parent class method.  This test class will not be 'executing' from the
        command line, as is the normal usage of TediousFuncTest().  Instead it will be executing
        select methods within the TediousFuncTest() object itself.
        TL;DR - Do *not* use run_test().

        Raises:
            If any 'test failures' exist, the call to _present_test_failures() will raise an
            AssertionError Exception, the message of which will contain all the failures.
        """
        self._tft_obj._present_test_results()  # Presents test failures based on verbosity level

    def set_test_input(self, verbosity: Any) -> None:
        """Sets test case input.

        Args:
            verbosity: Value for the TediousFuncTest object's _verbosity attribute.  Good input is
            a Verbosity object.

        Returns:
            None

        Raises:
            None
        """
        self._tft_obj._verbosity = verbosity


class NormalTestTFTRunTest(TestTFTRunTest):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_normal_01(self):
        """TO DO: DON'T DO NOW... define this test case."""


class ErrorTestTFTRunTest(TestTFTRunTest):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_error_01(self):
        """TO DO: DON'T DO NOW... define this test case."""


class BoundaryTestTFTRunTest(TestTFTRunTest):
    """Boundary Test Cases.

    Organize the Boundary Test Cases.
    """

    def test_boundary_01(self):
        """TO DO: DON'T DO NOW... define this test case."""


class SpecialTestTFTRunTest(TestTFTRunTest):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_special_01(self):
        """TO DO: DON'T DO NOW... define this test case."""


if __name__ == '__main__':
    execute_test_cases()
