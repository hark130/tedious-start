"""Functionally test TediousFuncTest.

Functionally test TediousFuncTest by:
    * Inheriting from this class
    * Override run_this_test()
    * Define your own functionality
    * Then either:
        * Use this "shunt" functionality by:
            * Operating on self._tft_obj
            * Calling create_std*()
            * Calling run_this_test()
        * Use the base TediousFuncTest functionality

NOTE: The child class was not intended to use all aspects of TediousFuncTest().  Rather, this
      test framework shunts around the established framework, only using the pieces it needs to.
      E.g., these test cases do *NOT* necessarily need to call run_test().  Rather, a local
      method calls the pieces/parts of run_test() needed for this framework.
"""

# Standard Imports
from typing import Any
# Third Party Imports
# Local Imports
from tediousstart.tediousfunctest import TediousFuncTest


# pylint: disable=protected-access
# We know what we're doing Pylint.  We're testing TEST with TEST.
class TestTFT(TediousFuncTest):
    """TestTediousFuncTest test class.

    This class provides common functionality to run NEBS functional tests against TediousFuncTest.
    """

    # CORE CLASS METHODS
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

        self._tft_obj = None     # TediousFuncTest object
        self._std_output = None  # Test input for the call to verify_stdout_missing()
        self._std_error = None   # Test input for the call to verify_stderr_missing()

    def create_stderr(self, std_err: str) -> None:
        """Append some example output to the TediousFuncTest object's _raw_stderr.

        Append some 'Stderr from command execution' to test against.

        Args:
            std_err: A string containing all the stderr from what would have been command
                execution.  Know that standard multi-line execution would include newlines in
                this string but it's not mandatory.

        Returns:
            None

        Raises:
            None.  Calls self.fail() instead.
        """
        self._validate_string(std_err, 'std_err', can_be_empty=True)
        self._tft_obj._raw_stderr = self._tft_obj._raw_stderr + std_err

    def create_stdout(self, std_out: str) -> None:
        """Append some example output to the TediousFuncTest object's _raw_stdout.

        Append some 'Stdout from command execution' to test against.

        Args:
            std_out: A string containing all the stdout from what would have been command
                execution.  Know that standard multi-line execution would include newlines in
                this string but it's not mandatory.

        Returns:
            None

        Raises:
            None.  Calls self.fail() instead.
        """
        self._validate_string(std_out, 'std_out', can_be_empty=True)
        self._tft_obj._raw_stdout = self._tft_obj._raw_stdout + std_out

# pylint: disable=broad-except
    def expect_failure(self, exception_type: Exception, exception_msg: str) -> None:
        """Expect that everything went fine and the test case passed."""
        # INPUT VALIDATION
        # exception_type
        self._validate_type(exception_type, 'exception_type', type)
        # exception_msg
        self._validate_string(exception_msg, 'exception_msg', can_be_empty=True)

        # EXPECT IT
        try:
            self.run_this_test()
        except Exception as err:
            if not isinstance(err, exception_type):
                self._add_test_failure(f'Expected Exception of type {exception_type} but '
                                       f'caught an Exception of type {type(err)}: {err}')
            elif exception_msg.lower() not in str(err).lower():
                self._add_test_failure(f'Expected the message "{exception_msg}" in {str(err)}')
        else:
            self._add_test_failure(f'Expected Exception of type {exception_type} but '
                                   'no Exception was raised')

        # DONE
        self._present_test_failures()

    def expect_success(self) -> None:
        """Expect that everything went fine and the test case passed."""
        try:
            self.run_this_test()
        except AssertionError as err:
            self.fail(f'This test case failed with an AssertionError of {str(err)}')
        except Exception as err:
            self.fail(f'This test case failed with an unanticipated Exception of {repr(err)}')

        # DONE
        self._present_test_failures()
# pylint: enable=broad-except

    def run_this_test(self) -> None:
        """Child class defines how to validate results of the command.

        This method must be overridden by the child class (even if you decide not to implement
        any functionality here).  This method will be called by self.expect_failure() and
        self.expect_success().
        Examples of what to do here:
            - Verify something (e.g., a file) exists
            - Verify something (e.g., a directory) is missing
            - Validate an environment variable
            - Call a self._tft_obj method() to setup the test case parameters
            - Call a self._tft_obj method() to test TediousFuncTest

        Args:
            None

        Returns:
            None

        Raises:
            NotImplementedError: The child class hasn't overridden this method.
        """
        raise NotImplementedError(
            self._test_error.format('The child class must override the run_this_test method'))

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

    def validate_results(self) -> Any:
        """Overrides parent class method to validate EXECUTABLE execution.

        This method was overridden because it must be.  This method will be called by
        self._run_test() once the command has exited.

        Args:
            None

        Returns:
            None

        Raises:
            None
        """
        # Verification is handled by other methods
        # Sometimes, TediousFuncTest is all you need
# pylint: enable=protected-access
