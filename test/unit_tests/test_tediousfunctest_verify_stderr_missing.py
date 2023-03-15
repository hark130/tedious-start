"""Unit test the TediousStart.verify_stderr_missing() methods.

Run the test cases defined in this module using any of the example commands below:

    Usage:
    python -m unittest                                                    # Run *ALL* test cases
    python -m unittest -k TestTFTVerifyStderrMissing                      # Match this test class
    python -m test.unit_tests                                             # Run all unit test cases
    python -m test.unit_tests.test_tediousfunctest_verify_stderr_missing  # Run just these tests
"""

# Standard Imports
from typing import Any
# Third Party Imports
# Local Imports
from tediousstart.tediousfunctest import TediousFuncTest
from tediousstart.tediousstart import execute_test_cases
from tediousstart.tediousunittest import TediousUnitTest


class TestTFTVerifyStderrMissing(TediousUnitTest):
    """TestTFTVerifyMissing unit test class.

    This class provides base functionality to run NEBS unit tests for fail_test_case().
    """
    def __init__(self, *args, **kwargs) -> None:
        """TestTFTVerifyMissing ctor.

        TestTFTVerifyMissing constructor.  Initializes attributes after constructing the parent
        object.

        Args:
            args: Arguments to pass to the parent class ctor
            kwargs: Keyword arguments to pass to the parent class ctor

        Returns:
            None

        Raises:
            None
        """
        super().__init__(*args, **kwargs)

        self._tft_obj = None  # TediousFuncTest object

    def setUp(self) -> None:
        """Prepares Test Case.

        Automate any preparation necessary before each Test Case executes.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        super().setUp()

        self._tft_obj = TediousFuncTest()
        self.validate_return_value(None)

    # CORE CLASS METHODS
    # Methods listed in call order
    def call_callable(self) -> Any:
        """Calls TediousStart.fail_test_case().

        Overrides the parent method.  Defines the way to call TediousStart.fail_test_case().

        Args:
            None

        Returns:
            Return value of TediousFuncTest.verify_stderr_missing()

        Raises:
            Exceptions raised by TediousFuncTest.verify_stderr_missing() are bubbled up and handled
            by TediousUnitTest
        """
        return self._tft_obj.verify_stderr_missing(*self._args, **self._kwargs)

    def validate_return_value(self, return_value: Any) -> None:
        """Validate TediousFuncTest.verify_stderr_missing() return value.

        Overrides the parent method.  Defines how the test framework validates the return value
        of a completed call.  Calls self._validate_return_value() method under the hood.

        Args:
            return_value: This is ignored.  self.fail_test_case() should return None, if ever.
        """
        self._validate_return_value(return_value=None)

    def expect_failure(self, exception_type: Exception, raw_msg: Any) -> None:
        """Wraps self.expect_exception() with normal failure expectations.

        Args:
            exception_type: The Exception expected to be raised
            raw_msg: Pass in a raw message to be wrapped in _test_error
        """
        self.expect_exception(exception_type=exception_type,
                              exception_msg=self._test_error.format(str(raw_msg)))


class NormalTestTFTVerifyStderrMissing(TestTFTVerifyStderrMissing):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_normal_01(self):
        """Valid input, kwarg."""
        self.set_test_input(output=['This should be missing', 'so should this'])
        self.expect_return(None)
        self.run_test()

    def test_normal_02(self):
        """Valid input."""
        self.set_test_input(['This should still be missing', 'this as well'])
        self.expect_return(None)
        self.run_test()


class ErrorTestTFTVerifyStderrMissing(TestTFTVerifyStderrMissing):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_error_01(self):
        """Not enough args."""
        self.set_test_input()
        # This test case won't make it past the interpreter
        self.expect_exception(TypeError, 'required positional argument')
        self.run_test()

    def test_error_02(self):
        """Too many args."""
        self.set_test_input(['one string'], ['two many strings'])
        # This test case won't make it past the interpreter
        self.expect_exception(TypeError, 'positional arguments')
        self.run_test()

    def test_error_03(self):
        """Bad data type."""
        self.set_test_input('one string')
        self.expect_failure(AssertionError, 'output expected type')
        self.run_test()


class BoundaryTestTFTVerifyStderrMissing(TestTFTVerifyStderrMissing):
    """Boundary Test Cases.

    Organize the Boundary Test Cases.
    """

    def test_boundary_01(self):
        """Valid input: no strings."""
        self.set_test_input([])
        self.expect_failure(AssertionError, '')
        self.run_test()

    def test_boundary_02(self):
        """Valid input: one string."""
        self.set_test_input(['Just one string'])
        self.expect_return(None)
        self.run_test()

    def test_boundary_03(self):
        """Valid input: ten strings."""
        self.set_test_input(['String1', 'String2', 'String3', 'String4', 'String5',
                             'String6', 'String7', 'String8', 'String9', 'String10'])
        self.expect_return(None)
        self.run_test()

    def test_boundary_04(self):
        """Valid input: 100 strings."""
        test_input = ['String num: ' + str(num) for num in range(1, 101)]
        self.set_test_input(test_input)
        self.expect_return(None)
        self.run_test()


class SpecialTestTFTVerifyStderrMissing(TestTFTVerifyStderrMissing):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_special_01(self):
        """Empty string."""
        self.set_test_input([''])
        self.expect_return(None)
        self.run_test()

    def test_special_02(self):
        """Empty string buried in a list."""
        self.set_test_input(['string1', '', 'string3'])
        self.expect_return(None)
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
