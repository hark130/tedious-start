"""Template functional test module.

Use this module as an example/template to write functional tests for executables (e.g.,
python packages, python modules, eggsecutables, commands, binaries).  If you decide to separate
your test class and Test Cases into separate modules within this package, ensure the Test Case
module filename begins with `test_`.  The class's module may be named IAW PEP8 naming standards.

    Usage:
    1. Copy this file and rename it to `test_EXECUTABLE.py`
    2. Rename the internal 'EXECUTABLE' placeholders accordingly
    3. Source-control discretely named file-based test input (if applicable)
    4. Define numbered Test Cases within the NEBS classes whose name begins with `test_<NEBS>`
    5. `python3 -m test.functional_tests.test_EXECUTABLE` to run your test cases

    Troubleshooting:
    Q1. Why didn't my test cases run when I executed `python3 -m unittest`?
    A1a. Ensure your test case module's filename start with `test_`?
    A1b. Is there at least one method name that starts with `test_`?
    Q2. Why didn't my test cases execute with `python3 -m test.unit_tests.test_EXECUTABLE`?
    A2. Consider the following:
        - Did you replace the command's 'test_EXECUTABLE' with the actual name of your module?
        - Did you remove or comment out `execute_test_cases()` or the code block that executes
            `execute_test_cases()`?
        - Did you remove, comment, or modify `execute_test_cases()`'s behavior?
        - Is there at least one Test Case whose name starts with `test_`?
        - Try `python3 -m unittest -k EXECUTABLE` but replace EXECUTABLE with a substring related
            to your test cases and/or module
"""

# Standard Imports
from typing import Any
import sys
import unittest
# Third Party Imports
# Local Imports
from tediousstart.tediousstart import execute_test_cases
from tediousstart.tediousfunctest import TediousFuncTest

MAX_INT_VALUE = sys.maxsize  # https://docs.python.org/3.1/library/sys.html#sys.maxsize


class TestEXECUTABLE(TediousFuncTest):
    """EXECUTABLE unit test class.

    This class provides base functionality to run NEBS functional tests for EXECUTABLE.
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    # pylint: disable=useless-super-delegation
    # Reason?  Leaving this here has a placeholder for the copy/pasters of the world.
    def __init__(self, *args, **kwargs) -> None:
        """TestEXECUTABLE ctor.

        TestEXECUTABLE constructor.  Initializes attributes after constructing the parent
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

    def validate_results(self) -> Any:
        """Overrides parent class method to validate EXECUTABLE execution.

        This method was overridden because it must be.  This method will be called by
        self._run_test() once the command has exited.

        Args:
            None

        Returns:
            None

        Raises:
            None.  Calls self._add_test_failure() instead.
        """
        # Verification is handled by other methods
        pass  # Sometimes, TediousFuncTest is all you need

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
        super(TestEXECUTABLE, self).setUp()
    # pylint: enable=useless-super-delegation

    def expect_failure(self, exp_output: list, exp_exit: int) -> None:
        """Expect this test case to fail.

        Extricate common code usage for test cases expected to fail.

        Args:
            exp_output: List of strings to find in stderr
            exp_exit: Expected exit code

        Returns:
            None

        Raises:
            None.  Calls self.fail() instead.
        """
        # INPUT VALIDATION
        # exp_output
        self._validate_list(validate_this=exp_output, param_name='exp_output', can_be_empty=True)
        # exp_output contents
        for entry in exp_output:
            self._validate_string(validate_this=entry, param_name='exp_output entry',
                                  can_be_empty=False)
        # exp_exit
        self._validate_type(validate_this=exp_exit, param_name='exp_exit', param_type=int)

        # EXPECT IT
        # stdout
        self.verify_stdout_empty()
        # stderr
        self.expect_stderr(output=exp_output)
        # exit code
        self.expect_exit_code(exit_code=exp_exit)  # 1 on bad arg(s), 2 on failed execution

    def expect_success(self, numerator: int, denominator: int, quotient: float) -> None:
        """Expect this test case to pass.

        Extricate common code usage for test cases expected to succeed.

        Args:
            exp_output: List of strings to find in stderr
            exp_exit: Expected exit code

        Returns:
            None

        Raises:
            None.  Calls self.fail() instead.
        """
        # INPUT VALIDATION
        self._validate_type(validate_this=numerator, param_name='numerator', param_type=int)
        self._validate_type(validate_this=denominator, param_name='denominator', param_type=int)
        self._validate_type(validate_this=quotient, param_name='quotient', param_type=float)

        # EXPECT IT
        # stdout
        self.expect_stdout(output=[f'{numerator} / {denominator} = {quotient}'])
        # stderr
        self.verify_stderr_empty()
        # exit code
        self.expect_exit_code(exit_code=0)  # 0 on success, 1 on bad arg(s), 2 on failed execution


class NormalTestEXECUTABLE(TestEXECUTABLE):
    """Normal Test Cases.

    Organize the Normal Test Cases
    """

    def test_normal_01(self):
        """Normal input that's expected to pass."""
        # LOCAL VARIABLES
        in_num = 1     # Input numerator
        in_den = 2     # Input denominator
        exp_quo = 0.5  # Expected result

        # TEST CASE SETUP
        self.set_command_list(['python3', '-m', 'badcode', str(in_num), str(in_den)])
        self.expect_success(in_num, in_den, exp_quo)
        
        # DO IT
        self.run_test()

    def test_normal_02(self):
        """More different normal input."""
        # LOCAL VARIABLES
        in_num = 4     # Input numerator
        in_den = 2     # Input denominator
        exp_quo = 2.0  # Expected result

        # TEST CASE SETUP
        self.set_command_list(['python3', '-m', 'badcode', str(in_num), str(in_den)])
        self.expect_success(in_num, in_den, exp_quo)
        
        # DO IT
        self.run_test()


class ErrorTestEXECUTABLE(TestEXECUTABLE):
    """Error Test Cases.

    Organize the Error Test Cases
    """

    def test_error_01(self):
        """Error input that's expected to fail."""
        # LOCAL VARIABLES
        exp_exit = 1   # Expected exit code: 0 on success, 1 on bad arg(s), 2 on failed execution

        # TEST CASE SETUP
        self.set_command_list(['python3', '-m', 'badcode', '1'])
        self.expect_failure(exp_output=['RUNTIME ERROR: Invalid usage: Not enough arguments'],
                            exp_exit=exp_exit)
        
        # DO IT
        self.run_test()

    def test_error_02(self):
        """Error input that's also expected to fail."""
        # LOCAL VARIABLES
        exp_exit = 1   # Expected exit code: 0 on success, 1 on bad arg(s), 2 on failed execution

        # TEST CASE SETUP
        self.set_command_list(['python3', '-m', 'badcode', '1', '2', '3?!'])
        self.expect_failure(exp_output=['RUNTIME ERROR: Invalid usage: Too many arguments'],
                            exp_exit=exp_exit)
        
        # DO IT
        self.run_test()

    def test_error_03(self):
        """Error input that's definitely expected to fail."""
        # LOCAL VARIABLES
        exp_exit = 1     # Expected exit code: 0 on success, 1 on bad arg(s), 2 on failed execution
        bad_num = 'one'  # Bad numerator

        # TEST CASE SETUP
        self.set_command_list(['python3', '-m', 'badcode', bad_num, '2'])
        self.expect_failure(exp_output=["VALUE ERROR: invalid literal for int() with base 10: "
                                   f"'{bad_num}'"],
                            exp_exit=exp_exit)
        
        # DO IT
        self.run_test()

    def test_error_03(self):
        """Error input that's definitely expected to fail even more."""
        # LOCAL VARIABLES
        exp_exit = 1     # Expected exit code: 0 on success, 1 on bad arg(s), 2 on failed execution
        bad_den = 'two'  # Bad numerator

        # TEST CASE SETUP
        self.set_command_list(['python3', '-m', 'badcode', '1', bad_den])
        self.expect_failure(exp_output=["VALUE ERROR: invalid literal for int() with base 10: "
                                   f"'{bad_den}'"],
                            exp_exit=exp_exit)
        
        # DO IT
        self.run_test()


class BoundaryTestEXECUTABLE(TestEXECUTABLE):
    """Boundary Test Cases.

    Organize the Boundary Test Cases
    """

    def test_boundary_01(self):
        """Boundary input: max int numerator"""
        # LOCAL VARIABLES
        in_num = MAX_INT_VALUE          # Input numerator
        in_den = 1                      # Input denominator
        exp_quo = float(MAX_INT_VALUE)  # Expected result

        # TEST CASE SETUP
        self.set_command_list(['python3', '-m', 'badcode', str(in_num), str(in_den)])
        self.expect_success(in_num, in_den, exp_quo)
        
        # DO IT
        self.run_test()

    def test_boundary_02(self):
        """Boundary input: max int denominator"""
        # LOCAL VARIABLES
        in_num = 1                          # Input numerator
        in_den = MAX_INT_VALUE              # Input denominator
        exp_quo = float(1 / MAX_INT_VALUE)  # Expected result

        # TEST CASE SETUP
        self.set_command_list(['python3', '-m', 'badcode', str(in_num), str(in_den)])
        self.expect_success(in_num, in_den, exp_quo)
        # DO IT
        self.run_test()


class SpecialTestEXECUTABLE(TestEXECUTABLE):
    """Special Test Cases.

    Organize the Special Test Cases
    """

    def test_special_01(self):
        # LOCAL VARIABLES
        exp_exit = 2   # Expected exit code: 0 on success, 1 on bad arg(s), 2 on failed execution

        # TEST CASE SETUP
        self.set_command_list(['python3', '-m', 'badcode', '9', '0'])
        self.expect_failure(exp_output=['VALUE ERROR: You may not divide by zero'],
                            exp_exit=exp_exit)
        
        # DO IT
        self.run_test()


if __name__ == '__main__':
    execute_test_cases()
