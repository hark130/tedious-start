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
from enum import Enum
from typing import Any
import io
import random
import string
# Third Party Imports
# Local Imports
from tediousstart.redirect_std_streams import RedirectStdStreams
from tediousstart.tediousstart import execute_test_cases
from tediousstart.verbosity import Verbosity
from test.functional_tests.test_tediousfunctest import TestTFT


MB = 1048576  # Size of 1 MB


class TestTFTRunTest(TestTFT):
    """TestTFTRunTest functional test class.

    This class provides base functionality to run NEBS functional tests for
    TediousFuncTest.run_test().
    """

    # CORE CLASS METHODS
    def __init__(self, *args, **kwargs) -> None:
        """TestTFTRunTest ctor.

        TestTFTRunTest constructor.  Initializes attributes after constructing the parent
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

        self._test_case_verbosity = None  # Copy of test case input for verbosity
        self._test_case_stdout = ''       # Copy of test case input for raw stdout
        self._test_case_stderr = ''       # Copy of test case input for raw stderr
        self._test_case_fail_list = []    # Copy of test case input for test failures

    def add_raw_output(self, raw_stdout: str = '', raw_stderr: str = '') -> None:
        """Concatenates raw output locally and to relevant TediousFuncTest object attributes.

        Use this method to add raw output.  Many test cases will want *actual* output to exist
        for the purposes of output validation.  Validation is handled by the parent class methods.

        Args:
            raw_stdout: Optional; Add this string to self._tft_obj._raw_stdout.  Normal _raw_stdout
                contents tend to have newlines but that is not necessary for these tests.
            raw_stderr: Optional; Add this string to self._tft_obj._raw_stderr.  Normal _raw_stderr
                contents tend to have newlines but that is not necessary for these tests.

        Returns:
            None

        Raises:
            None.  Calls self.fail() instead.
        """
        # ADD IT
        # Test object
        self.create_stdout(raw_stdout)
        self.create_stderr(raw_stderr)
        # Save it
        self._test_case_stdout = self._test_case_stdout + raw_stdout
        self._test_case_stderr = self._test_case_stderr + raw_stderr

    def add_test_failures(self, failure_list: list[str]) -> None:
        """Add a Test Case failure message to the TediousFuncTest object being tested.

        Use this method to add potential output.  Many test cases will want want to add example
        errors to test the formatting of the verbose printing.

        Args:
            failure_msg: Non-empty list of non-empty failure message strings.

        Returns:
            None

        Raises:
            None.  Calls self.fail() instead.
        """
        # INPUT VALIDATION
        # We're not testing self._tft_obj._add_test_failure() here so let's ensure we give it
        # good input.
        self._validate_list(failure_list, 'failure_list', can_be_empty=False)
        for failure_msg in failure_list:
            self._validate_string(failure_msg, 'failure_list entry', can_be_empty=False)
            # ADD IT
            # Test object
            self._tft_obj._add_test_failure(failure_msg=failure_msg)
            # Save it
            self._test_case_fail_list.append(failure_msg)

    def expect_stderr_verbose(self) -> None:
        """Formats raw output and failure list into self.expect_stderr() call."""
        # LOCAL VARIABLES
        stderr_list = []

        # EXPECT IT
        # Stdout
        stderr_list.append(self._verb_stdout_hdr)
        if self._test_case_stdout:
            stderr_list.append(self._test_case_stdout)
        else:
            stderr_list.append(self._verb_empty_msg)

        # Stderr
        stderr_list.append(self._verb_stdout_hdr)
        if self._test_case_stderr:
            stderr_list.append(self._test_case_stderr)
        else:
            stderr_list.append(self._verb_empty_msg)
        # Failure List
        stderr_list.append(self._verb_failure_hdr)
        if self._test_case_fail_list:
            for index in range(0, len(self._test_case_fail_list)):
                stderr_list.append(f'{str(index+1)}. {self._test_case_fail_list[index]}')
        else:
            stderr_list.append(self._verb_empty_msg)

        # DONE
        self.expect_stderr(stderr_list)

    def expect_verbose_failure(self) -> None:
        """Prepares expected failure messages and calls self.expect_failure().

        Wraps existing expected failure messages in the expected format/status, in accordance
        with the established verbosity, and calls self.expect_failure().
        """
        if isinstance(self._test_case_verbosity, Verbosity):
            if self._test_case_verbosity == Verbosity.DEFAULT:
                self.expect_failure(AssertionError, '\n'.join(self._test_case_fail_list))
            elif self._test_case_verbosity == Verbosity.FAIL:
                self.expect_failure(AssertionError, 'See stderr for test case details')
            elif self._test_case_verbosity == Verbosity.ALL:
                self.expect_failure(AssertionError, 'See stderr for test case details')
            else:
                self.expect_failure(AssertionError, 'Unsupported Verbosity selection')
        else:
            self.expect_failure(AssertionError, self._test_error.format(''))

    def expect_verbose_success(self) -> None:
        """Prepares expected success messages and calls self.expect_success().

        Wraps existing expected success messages in the expected format/status, in accordance
        with the established verbosity, and calls self.expect_success().
        """
        if isinstance(self._test_case_verbosity, Verbosity):
            if self._test_case_verbosity == Verbosity.DEFAULT:
                self.verify_stdout_empty()
                self.verify_stderr_empty()
            elif self._test_case_verbosity == Verbosity.FAIL:
                self.verify_stdout_empty()
                self.verify_stderr_empty()
            elif self._test_case_verbosity == Verbosity.ALL:
                self.verify_stdout_empty()
                self.expect_stderr_verbose()
            else:
                self.fail_test_case('The test class is unaware of how to support '
                                    'this Verbosity selection')
            self.expect_success()
        else:
            self.fail_test_case('Test case verbosity has not been set')

    def prepare_test_case(self, verbosity: Any, raw_stdout: str = '',
                          raw_stderr: str = '') -> None:
        """Simplifies test case setup by wrapping common method calls.

        Calls relevant test case methods with test author input: set_test_input(),
        add_raw_output().  Input validation is handled by the 'callee' methods.

        Args:
            verbosity: Value for the TediousFuncTest object's _verbosity attribute.  Good input is
                a Verbosity object.
            raw_stdout: Optional; Add this string to self._tft_obj._raw_stdout.  Normal _raw_stdout
                contents tend to have newlines but that is not necessary for these tests.
            raw_stderr: Optional; Add this string to self._tft_obj._raw_stderr.  Normal _raw_stderr
                contents tend to have newlines but that is not necessary for these tests.

        Returns:
            None

        Raises:
            None.  Calls self.fail() instead.
        """
        self.set_test_input(verbosity)
        self.add_raw_output(raw_stdout=raw_stdout, raw_stderr=raw_stderr)

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
        # LOCAL VARIABLES
        stdout_stream = io.StringIO()  # Save the stdout stream externally so we can read it
        stderr_stream = io.StringIO()  # Save the stderr stream externally so we can read it

        # RUN IT
        with RedirectStdStreams(stdout=stdout_stream, stderr=stderr_stream) as temp_obj:
            try:
                self._tft_obj._present_test_results()  # Presents test failures IAW verbosity level
                (self._raw_stdout, self._raw_stderr) = temp_obj.communicate()  # Save it
            except (AssertionError, TypeError, ValueError) as err:
                stdout_stream.seek(0)
                stderr_stream.seek(0)
                self._raw_stdout = stdout_stream.read()
                self._raw_stderr = stderr_stream.read()
                raise err

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
        # Test object
        self._tft_obj._verbosity = verbosity
        # Save it
        self._test_case_verbosity = verbosity


class NormalTestTFTRunTest(TestTFTRunTest):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_normal_01(self):
        """Use case: default; stdout X, stderr X, failures X."""
        self.prepare_test_case(Verbosity.DEFAULT)
        self.expect_verbose_success()

    def test_normal_02(self):
        """Use case: default; stdout ✓, stderr X, failures X."""
        self.prepare_test_case(Verbosity.DEFAULT, raw_stdout='This is some stdout.')
        self.expect_verbose_success()

    def test_normal_03(self):
        """Use case: default; stdout X, stderr ✓, failures X."""
        self.prepare_test_case(Verbosity.DEFAULT, raw_stderr='This is some stderr.')
        self.expect_verbose_success()

    def test_normal_04(self):
        """Use case: default; stdout X, stderr X, failures ✓."""
        test_failure_list = ['This is the first failure', 'This is the second failure',
                             'This is the third failure']
        self.prepare_test_case(Verbosity.DEFAULT)
        self.verify_stdout_empty()
        self.add_test_failures(test_failure_list)
        self.expect_verbose_failure()

    def test_normal_05(self):
        """Use case: default; stdout ✓, stderr ✓, failures ✓."""
        test_failure_list = ['This is the first failure', 'This is the second failure',
                             'This is the third failure']
        self.prepare_test_case(Verbosity.DEFAULT, raw_stdout='This is some stdout.',
                               raw_stderr='This is some stderr.')
        self.add_test_failures(test_failure_list)
        self.expect_verbose_failure()

    def test_normal_06(self):
        """Use case: fail; stdout X, stderr X, failures X."""
        self.prepare_test_case(Verbosity.FAIL)
        self.expect_verbose_success()

    def test_normal_07(self):
        """Use case: fail; stdout ✓, stderr X, failures X."""
        self.prepare_test_case(Verbosity.FAIL, raw_stdout='This is some stdout.')
        self.expect_verbose_success()

    def test_normal_08(self):
        """Use case: fail; stdout X, stderr ✓, failures X."""
        self.prepare_test_case(Verbosity.FAIL, raw_stderr='This is some stderr.')
        self.expect_verbose_success()

    def test_normal_09(self):
        """Use case: fail; stdout X, stderr X, failures ✓."""
        test_failure_list = ['This is the first failure', 'This is the second failure',
                             'This is the third failure']
        self.prepare_test_case(Verbosity.FAIL)
        self.verify_stdout_empty()
        self.add_test_failures(test_failure_list)
        self.expect_verbose_failure()

    def test_normal_10(self):
        """Use case: fail; stdout ✓, stderr ✓, failures ✓."""
        test_failure_list = ['This is the first failure', 'This is the second failure',
                             'This is the third failure']
        self.prepare_test_case(Verbosity.FAIL, raw_stdout='This is some stdout.',
                               raw_stderr='This is some stderr.')
        self.add_test_failures(test_failure_list)
        self.expect_verbose_failure()

    def test_normal_11(self):
        """Use case: all; stdout X, stderr X, failures X."""
        self.prepare_test_case(Verbosity.ALL)
        self.expect_verbose_success()

    def test_normal_12(self):
        """Use case: all; stdout ✓, stderr X, failures X."""
        self.prepare_test_case(Verbosity.ALL, raw_stdout='This is some stdout.')
        self.expect_verbose_success()

    def test_normal_13(self):
        """Use case: all; stdout X, stderr ✓, failures X."""
        self.prepare_test_case(Verbosity.ALL, raw_stderr='This is some stderr.')
        self.expect_verbose_success()

    def test_normal_14(self):
        """Use case: all; stdout X, stderr X, failures ✓."""
        test_failure_list = ['This is the first failure', 'This is the second failure',
                             'This is the third failure']
        self.prepare_test_case(Verbosity.ALL)
        self.verify_stdout_empty()
        self.add_test_failures(test_failure_list)
        self.expect_verbose_failure()

    def test_normal_15(self):
        """Use case: all; stdout ✓, stderr ✓, failures ✓."""
        test_failure_list = ['This is the first failure', 'This is the second failure',
                             'This is the third failure']
        self.prepare_test_case(Verbosity.ALL, raw_stdout='This is some stdout.',
                               raw_stderr='This is some stderr.')
        self.add_test_failures(test_failure_list)
        self.expect_verbose_failure()


class ErrorTestTFTRunTest(TestTFTRunTest):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_error_01(self):
        """Bad data type."""
        self.prepare_test_case('ALL')
        self.expect_verbose_failure()

    def test_error_02(self):
        """Unsupported Verbosity Enum."""
        class Verbosity(Enum):
            """Overrode the class to pass in a bad Enum value."""
            BAD=13  # Bad value
        self.prepare_test_case(Verbosity.BAD)
        self.expect_verbose_failure()


class BoundaryTestTFTRunTest(TestTFTRunTest):
    """Boundary Test Cases.

    Organize the Boundary Test Cases.
    """

    def test_boundary_01(self):
        """Use case: all; Noisy stdout."""
        self.prepare_test_case(Verbosity.ALL, raw_stdout=''.join(random.choices(string.printable,
                                                                                k=10*MB)))
        self.expect_verbose_success()

    def test_boundary_02(self):
        """Use case: all; Noisy stderr."""
        self.prepare_test_case(Verbosity.ALL, raw_stderr=''.join(random.choices(string.printable,
                                                                                k=10*MB)))
        self.expect_verbose_success()

    def test_boundary_03(self):
        """Use case: all; Numerous failures."""
        test_failure_list = []
        for number in range(1, 101):
            test_failure_list.append(f'This is failure number {str(number)}?!')
        self.prepare_test_case(Verbosity.ALL)
        self.add_test_failures(test_failure_list)
        self.expect_verbose_failure()

    def test_boundary_04(self):
        """Use case: all; It all comes crashing down."""
        test_failure_list = []
        for number in range(1, 101):
            test_failure_list.append(f'Too many errors to count...')
        self.prepare_test_case(Verbosity.ALL,
                               raw_stdout=''.join(random.choices(string.printable, k=5*MB)),
                               raw_stderr=''.join(random.choices(string.printable, k=5*MB)))
        self.add_test_failures(test_failure_list)
        self.expect_verbose_failure()


class SpecialTestTFTRunTest(TestTFTRunTest):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_special_01(self):
        """Use the new feature here: Fail."""
        std_output = 'SpecialTestTFTRunTest Special 01 is set to Verbosity.FAIL'
        self.set_command_list(['echo', '-n', std_output])
        self.expect_stdout([std_output])
        self.verify_stderr_empty()
        self.run_test(Verbosity.FAIL)

    def test_special_02(self):
        """Use the new feature here: All."""
        std_output = 'SpecialTestTFTRunTest Special 02 is set to Verbosity.ALL'
        self.set_command_list(['echo', '-n', std_output])
        self.expect_stdout([std_output])
        self.verify_stderr_empty()
        self.run_test(Verbosity.ALL)


if __name__ == '__main__':
    execute_test_cases()
