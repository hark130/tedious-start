"""Unit test the tediousstart.execute_test_cases() function.

NOTE: No 'expect pass' test cases (e.g., Normal) were written as unit tests.  If
execute_test_cases() were to run normally here, it would recursively execute these test cases and
we don't need that.  'Expect pass' behavior was manually tested but we'll consider writing
functional test cases to programmatically verify that behavior.

Run the test cases defined in this module using any of the example commands below:

    Usage:
    python -m unittest
    python -m unittest -k TestTESTExecuteTestCases
    python -m test.unit_tests.test_tediousstart_execute_test_cases
"""

# Standard Imports
from typing import Any
# Third Party Imports
# Local Imports
from tediousstart.tediousstart import execute_test_cases
from tediousstart.tediousunittest import TediousUnitTest


class TestTESTExecuteTestCases(TediousUnitTest):
    """TestTESTExecuteTestCases unit test class.

    This class provides base functionality to run NEBS unit tests for fail_test_case().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Calls execute_test_cases().

        Overrides the parent method.  Defines the way to call execute_test_cases().

        Args:
            None

        Returns:
            Return value of execute_test_cases()

        Raises:
            Exceptions raised by execute_test_cases() are bubbled up and handled by
            TediousUnitTest
        """
        return execute_test_cases(*self._args, **self._kwargs)

    def validate_return_value(self, return_value: Any) -> None:
        """Validate execute_test_cases() return value.

        Overrides the parent method.  Defines how the test framework validates the return value
        of a completed call.  Calls self._validate_return_value() method under the hood.

        Args:
            return_value: This is ignored.  execute_test_cases() should return None.
        """
        self._validate_return_value(return_value=None)


class ErrorTestTESTExecuteTestCases(TestTESTExecuteTestCases):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_error_01(self):
        """Bad data type: sys_exit."""
        self.set_test_input(sys_exit='False')
        self.expect_exception(exception_type=TypeError,
                              exception_msg='sys_exit')
        self.run_test()

    def test_error_02(self):
        """Bad data type: verbosity."""
        self.set_test_input(verbosity='1')
        self.expect_exception(exception_type=TypeError,
                              exception_msg='verbosity')
        self.run_test()


class BoundaryTestTESTExecuteTestCases(TestTESTExecuteTestCases):
    """Boundary Test Cases.

    Organize the Boundary Test Cases.
    """

    def test_boundary_01(self):
        """Barely bad verbosity value."""
        input_verbosity = -1
        self.set_test_input(verbosity=input_verbosity)
        self.expect_exception(exception_type=ValueError,
                              exception_msg=f'Verbosity value of {input_verbosity} '
                                            'is not supported')
        self.run_test()

    def test_boundary_02(self):
        """Very bad verbosity value."""
        input_verbosity = -1000000000000000
        self.set_test_input(verbosity=input_verbosity)
        self.expect_exception(exception_type=ValueError,
                              exception_msg=f'Verbosity value of {input_verbosity} '
                                            'is not supported')
        self.run_test()


if __name__ == '__main__':
    # Does this count as a "Normal" (see: NEBS) unit test case?
    execute_test_cases(sys_exit=True, verbosity=2)
