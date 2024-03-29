"""Functionally test TediousFuncTest.verify_*_missing() methods.

Functionally test the TediousFuncTest.verify_*_missing() methods by:
    * Creating and storing raw output (as a functional test would do)
    * Call the verify_*_missing() methods with test input
    * Validate their results by using _validate_default_results() and _present_test_failures()

NOTE: These functional test cases do *NOT* use all aspects of TediousFuncTest().  Rather, this
      test framework shunts around the established framework, only using the pieces it needs to.
      E.g., these test cases do *NOT* call run_test().  Rather, a local method calls the pieces/
      parts of run_test() needed for this framework.

Run the test cases defined in this module using any of the example commands below:

    Usage:
    python -m unittest                                                   # Run *ALL* test cases
    python -m unittest -k TestTFTVerifyMissing                           # Match this test class
    python -m test.functional_tests                                      # Run all functional tests
    python -m test.functional_tests.test_tediousfunctest_verify_missing  # Run just these tests
"""

# Standard Imports
from typing import Any
# Third Party Imports
# Local Imports
from test.functional_tests.test_tediousfunctest import TestTFT
from tediousstart.tediousstart import execute_test_cases


# pylint: disable=protected-access
# We know what we're doing Pylint.  We're testing TEST with TEST.
class TestTFTVerifyMissing(TestTFT):
    """TestTFTVerifyMissing functional test class.

    This class provides base functionality to run NEBS functional tests for
    TediousFuncTest.verify_*_missing().
    """

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
        if self._std_output is not None:
            self._tft_obj.verify_stdout_missing(self._std_output)
        if self._std_error is not None:
            self._tft_obj.verify_stderr_missing(self._std_error)
        self._tft_obj._validate_default_results()  # Checks stdout and stderr output
        self._tft_obj._present_test_failures()     # Presents test failures

    def set_test_input(self, std_output: Any = None, std_error: Any = None) -> None:
        """Sets test case input for the calls to verify_*_missing().

        Args:
            std_output: If not None, calls verify_stdout_missing() with this value during
                the call to run_this_test().  Good input is a lists of strings.
            std_error: If not None, calls verify_stderr_missing() with this value during
                the call to run_this_test().  Good input is a lists of strings.

        Returns:
            None

        Raises:
            None
        """
        self._std_output = std_output
        self._std_error = std_error


class NormalTestTFTVerifyMissing(TestTFTVerifyMissing):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_normal_01(self):
        """Stdout actually missing; stderr actually missing; expect test case success."""
        self.create_stdout('Here is some stdout for the test case.\nYou are welcome.')
        self.create_stderr('Here is some stderr for the test case.\nYou have some errors.')
        self.set_test_input(std_output=["Can't find this"], std_error=['NOT HERE'])
        self.expect_success()

    def test_normal_02(self):
        """Stdout *not* missing; stderr actually missing; expect test case failure."""
        needle = 'some stdout for'
        self.create_stdout('Here is some stdout for the test case.\nYou are welcome.')
        self.create_stderr('Here is some stderr for the test case.\nYou have some errors.')
        self.set_test_input(std_output=[needle], std_error=['NOT HERE'])
        self.expect_failure(AssertionError, f'Found excluded entry {needle} in stdout')

    def test_normal_03(self):
        """Stdout actually missing; stderr *not* missing; expect test case failure."""
        needle = 'some stderr for'
        self.create_stdout('Here is some stdout for the test case.\nYou are welcome.')
        self.create_stderr('Here is some stderr for the test case.\nYou have some errors.')
        self.set_test_input(std_output=['NOT HERE'], std_error=[needle])
        self.expect_failure(AssertionError, f'Found excluded entry {needle} in stderr')


class ErrorTestTFTVerifyMissing(TestTFTVerifyMissing):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_error_01(self):
        """Verify stdout missing argument contains a non-list."""
        self.set_test_input(std_output='this is a non-list')
        self.expect_failure(AssertionError, "TEST CASE ERROR: output expected type "
                            "<class 'list'>, instead received type <class 'str'>")

    def test_error_02(self):
        """Verify stderr missing argument contains a non-list."""
        self.set_test_input(std_error=42)
        self.expect_failure(AssertionError, "TEST CASE ERROR: output expected type "
                            "<class 'list'>, instead received type <class 'int'>")

    def test_error_03(self):
        """Verify stdout missing argument is empty."""
        self.set_test_input(std_output=[])
        self.expect_failure(AssertionError, 'TEST CASE ERROR: "output" can not be empty')

    def test_error_04(self):
        """Verify stderr missing argument is empty."""
        self.set_test_input(std_error=[])
        self.expect_failure(AssertionError, 'TEST CASE ERROR: "output" can not be empty')


class BoundaryTestTFTVerifyMissing(TestTFTVerifyMissing):
    """Boundary Test Cases.

    Organize the Boundary Test Cases.
    """

    def test_boundary_01(self):
        """Stdout barely missing; stderr actually missing; expect test case success."""
        needle = 'some stdout far'
        self.create_stdout('Here is some stdout for the test case.\nYou are welcome.')
        self.create_stderr('Here is some stderr for the test case.\nYou have some errors.')
        self.set_test_input(std_output=[needle], std_error=['NOT HERE'])
        self.expect_success()

    def test_boundary_02(self):
        """Stdout actually missing; stderr barely missing; expect test case success."""
        needle = 'same stderr for'
        self.create_stdout('Here is some stdout for the test case.\nYou are welcome.')
        self.create_stderr('Here is some stderr for the test case.\nYou have some errors.')
        self.set_test_input(std_output=['NOT HERE'], std_error=[needle])
        self.expect_success()

    def test_boundary_03(self):
        """Stdout needle same as the raw stdout; expect test case failure."""
        needle = 'this is all there is'
        self.create_stdout(needle)
        self.create_stderr('Here is some stderr for the test case.\nYou have some errors.')
        self.set_test_input(std_output=[needle], std_error=['NOT HERE'])
        self.expect_failure(AssertionError, f'Found excluded entry {needle} in stdout')

    def test_boundary_04(self):
        """Stderr needle same as the raw stderr; expect test case failure."""
        needle = 'this is all there is'
        self.create_stdout('Here is some stdout for the test case.\nYou are welcome.')
        self.create_stderr(needle)
        self.set_test_input(std_output=['NOT HERE'], std_error=[needle])
        self.expect_failure(AssertionError, f'Found excluded entry {needle} in stderr')


class SpecialTestTFTVerifyMissing(TestTFTVerifyMissing):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_special_01(self):
        """Raw stdout and raw stderr empty; Verify missing."""
        self.set_test_input(std_output=["Can't find this"], std_error=['NOT HERE'])
        self.expect_success()
# pylint: enable=protected-access


if __name__ == '__main__':
    execute_test_cases()
