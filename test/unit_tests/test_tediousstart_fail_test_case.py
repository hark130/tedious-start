"""Unit test the TediousStart.fail_test_case() method.

Run the test cases defined in this module using any of the example commands below:

    Usage:
    python -m unittest
    python -m unittest -k TestTESTFailTestCase
    python -m test.unit_tests.test_tediousstart_fail_test_case
"""

# Standard Imports
from typing import Any
import sys
# Third Party Imports
# Local Imports
from tediousstart.tediousstart import execute_test_cases, TediousStart
from tediousstart.tediousunittest import TediousUnitTest

MAX_INT_VALUE = sys.maxsize  # https://docs.python.org/3.1/library/sys.html#sys.maxsize


class TestTESTFailTestCase(TediousUnitTest):
    """TestTESTFailTestCase unit test class.

    This class provides base functionality to run NEBS unit tests for fail_test_case().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Calls CALLABLE.

        Overrides the parent method.  Defines the way to call CALLABLE.

        Args:
            None

        Returns:
            Return value of CALLABLE

        Raises:
            Exceptions raised by CALLABLE are bubbled up and handled by TediousUnitTest
        """
        test_obj = TediousStart()
        return test_obj.fail_test_case(*self._args, **self._kwargs)

    def validate_return_value(self, return_value: Any) -> None:
        """Validate CALLABLE return value.

        Overrides the parent method.  Defines how the test framework validates the return value
        of a completed call.  Calls self._validate_return_value() method under the hood.

        Args:
            return_value: This is ignored.  self.fail_test_case() should return None, if ever.
        """
        self._validate_return_value(return_value=None)

    def expect_success(self, test_msg: Any) -> None:
        """Wraps self.expect_exception() with normal failure expectations.

        Expects AssertionError with a certain messsage included.

        Args:
            test_msg: Pass in as msg
        """
        self.expect_exception(exception_type=AssertionError,
                              exception_msg=self._test_error.format(str(test_msg)))


class NormalTestTESTFailTestCase(TestTESTFailTestCase):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_normal_01(self):
        """Fail with a string, kwarg."""
        test_msg = 'This is my failing keyword test'
        self.set_test_input(msg=test_msg)
        self.expect_success(test_msg)
        self.run_test()

    def test_normal_02(self):
        """Fail with a string."""
        test_msg = 'This is my failing test'
        self.set_test_input(test_msg)
        self.expect_success(test_msg)
        self.run_test()


class ErrorTestTESTFailTestCase(TestTESTFailTestCase):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_error_01(self):
        """Not enough args."""
        self.set_test_input()
        self.expect_exception(exception_type=TypeError,
                              exception_msg='required positional argument')
        self.run_test()

    def test_error_02(self):
        """Too many args."""
        test_msg = 'This is my failing test'
        self.set_test_input(test_msg, test_msg)
        self.expect_exception(exception_type=TypeError, exception_msg='positional arguments')
        self.run_test()


class SpecialTestTESTFailTestCase(TestTESTFailTestCase):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_special_01(self):
        """Fail with None."""
        self.set_test_input(None)
        self.expect_success(None)
        self.run_test()

    def test_special_02(self):
        """Fail with an integer."""
        self.set_test_input(90318)
        self.expect_success(90318)
        self.run_test()

    def test_special_03(self):
        """Fail with an empty string."""
        self.set_test_input('')
        self.expect_success('')
        self.run_test()

    def test_special_04(self):
        """Fail with an Exception."""
        test_msg = TypeError('What are you even doing?!')
        self.set_test_input(test_msg)
        self.expect_exception(AssertionError, 'TEST CASE ERROR: What are you even doing?!')
        self.run_test()

    def test_special_05(self):
        """Fail with a function."""
        test_msg = print
        self.set_test_input(test_msg)
        self.expect_success('<built-in function print>')
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
