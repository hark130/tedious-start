"""Template unit test module.

Use this module as an example/template to write unit tests for callables (e.g., functions,
basic classes).  If you decide to separate your test class and Test Cases into separate modules
within this package, ensure the Test Case module filename begins with `test_`.  The class's module
may be named IAW PEP8 naming standards.

    Usage:
    1. Copy this file and rename it to `test_CALLABLE.py`
    2. Rename the internal 'CALLABLE' placeholders accordingly
    3. Source-control discretely named file-based test input (if applicable)
    4. Define numbered Test Cases within the NEBS classes whose name begins with `test_<NEBS>`
    5. `python3 -m test.unit_tests.test_CALLABLE` to run your test cases

    Troubleshooting:
    Q1. Why didn't my test cases run when I executed `python3 -m unittest`?
    A1a. Ensure your test case module's filename start with `test_`?
    A1b. Is there at least one method name that starts with `test_`?
    Q2. Why didn't my test cases execute with `python3 -m test.unit_tests.test_CALLABLE`?
    A2. Consider the following:
        - Did you replace the command's 'test_CALLABLE' with the actual name of your module?
        - Did you remove or comment out `execute_test_cases()` or the code block that executes
            `execute_test_cases()`?
        - Did you remove, comment, or modify `execute_test_cases()`'s behavior?
        - Is there at least one Test Case whose name starts with `test_`?
        - Try `python3 -m unittest -k CALLABLE` but replace CALLABLE with a substring related
            to your test cases and/or module
"""

# Standard Imports
from typing import Any
import sys
# Third Party Imports
# Local Imports
from badcode.maths import divide_it
from tediousstart.tediousstart import execute_test_cases
from tediousstart.tediousunittest import TediousUnitTest

MAX_INT_VALUE = sys.maxsize  # https://docs.python.org/3.1/library/sys.html#sys.maxsize


class TestCALLABLE(TediousUnitTest):
    """CALLABLE unit test class.

    This class provides base functionality to run NEBS unit tests for CALLABLE.
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    # pylint: disable=useless-super-delegation
    # Reason?  Leaving this here has a placeholder for the copy/pasters of the world.
    def __init__(self, *args, **kwargs) -> None:
        """TestCALLABLE ctor.

        TestCALLABLE constructor.  Initializes attributes after constructing the parent
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
    # pylint: enable=useless-super-delegation

    # pylint: disable=useless-super-delegation
    # Reason?  Leaving this here has a placeholder for the copy/pasters of the world.
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
    # pylint: enable=useless-super-delegation

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
        return divide_it(*self._args, **self._kwargs)

    def validate_return_value(self, return_value: Any) -> None:
        """Validate CALLABLE return value.

        Overrides the parent method.  Defines how the test framework validates the return value
        of a completed call.  Calls self._validate_return_value() method under the hood.

        Args:
            return_value: The data to check against what the test author defined as the expected
                return value.  The intended practice is to use the return value of the
                call_callable() method.

        Returns:
            None

        Raises:
            None
        """
        self._validate_return_value(return_value=return_value)


class NormalTestCALLABLE(TestCALLABLE):
    """Normal Test Cases.

    Organize the Normal Test Cases
    """

    def test_normal_01(self):
        """Normal input that's expected to pass."""
        self.set_test_input(1, 2)
        self.expect_return(0.5)
        self.run_test()

    def test_normal_02(self):
        """Normal input, using keywords, that's expected to pass."""
        self.set_test_input(numerator=90, denominator=16)
        self.expect_return(expected_result=5.625)
        self.run_test()


class ErrorTestCALLABLE(TestCALLABLE):
    """Error Test Cases.

    Organize the Error Test Cases
    """

    def test_error_01(self):
        """Error input that's expected to fail."""
        self.set_test_input([90], 318)
        self.expect_exception(TypeError, 'numerator must be an int')
        self.run_test()

    def test_error_02(self):
        """Error input, using keywords, that's expected to fail."""
        self.set_test_input(numerator=90, denominator='318')
        self.expect_exception(exception_type=TypeError, exception_msg='denominator must be an int')
        self.run_test()


class BoundaryTestCALLABLE(TestCALLABLE):
    """Boundary Test Cases.

    Organize the Boundary Test Cases
    """

    def test_boundary_01(self):
        """Boundary input: max int numerator"""
        self.set_test_input(MAX_INT_VALUE, 1)
        self.expect_return(float(MAX_INT_VALUE))
        self.run_test()

    def test_boundary_02(self):
        """Boundary input: max int denominator"""
        self.set_test_input(1, MAX_INT_VALUE)
        self.expect_return(float(1 / MAX_INT_VALUE))
        self.run_test()


class SpecialTestCALLABLE(TestCALLABLE):
    """Special Test Cases.

    Organize the Special Test Cases
    """

    def test_special_01(self):
        """Special input that that tests an edge case."""
        self.set_test_input(numerator=90, denominator=0)
        self.expect_exception(exception_type=ValueError, exception_msg='You may not divide by zero')
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
