"""Tedious Start (TEST) functional test class module.

Tedious Start (TEST) functional test base class module.  Implements common functionality to
functionally test a binary, script, command, etc that can be executed from the command line
interface.

    Typical usage example:

    1. Inherit from TediousFuncTest
    2. Define the validate_results() method
    3. Define additional functionality if necessary
    4. Define unittest Test Cases that:
        4.1. Set Test Input
        self.set_command_list()
        4.2. Set Expected Exit Code
        self.expect_exit_code(exit_code=exitcode)  # OPTIONAL
        4.3. Set Expected Output
        4.3.1. Standard Output
        self.expect_stdout(output=['I succeeded!'])  # OPTIONAL
        -or-
        self.verify_stdout_empty()  # OPTIONAL
        4.3.2. Standard Error
        self.expect_stderr(output=['...but I also had an error'])  # OPTIONAL
        -or-
        self.verify_stderr_empty()  # OPTIONAL
        4.4. Run Test
        self.run_test()
"""

# Standard Imports
from typing import Any
import sys
# Third Party Imports
from hobo.subprocess_wrapper import start_subprocess_cmd
# Local Imports
from tediousstart.tediousstart import TediousStart
from tediousstart.verbosity import Verbosity


# pylint: disable=too-many-instance-attributes
# TO DO: DON'T DO NOW... Refactor a couple of these attributes into tuples
class TediousFuncTest(TediousStart):
    """TEST functional test class.

    This class defines common functionality to execute functional test cases.

        General usage:
        1. Inherit from this class
        2. Look for necessary functionality among the 'sibling' classes (and move it up a level)
        3. Define the functionality you need
    """

    _verb_stdout_hdr = 'STDOUT'
    _verb_stderr_hdr = 'STDERR'
    _verb_failure_hdr = 'FAILURE LIST'
    _verb_empty_msg = '<EMPTY>'

    # CORE CLASS METHODS
    # Methods listed in call order
    def __init__(self, *args, **kwargs) -> None:
        """TediousFuncTest ctor.

        TediousFuncTest constructor.  Initializes attributes after constructing the parent
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

        self._cmd_list = []                  # Command list to pass to subprocess as args
        self._verbosity = Verbosity.DEFAULT  # Current test case verbosity level
        # stdout
        self._raw_stdout = ''                # Stdout from command execution
        self._check_stdout = False           # Test author's desire to verify stdout
        self._exp_stdout = []                # List of strings to verify in stdout
        self._excl_stdout = []               # List of strings to verify are *not* in stdout
        self._verify_stdout_empty = False    # Test author's desire to verify stdout is empty
        # stderr
        self._raw_stderr = ''                # Stderr from command execution
        self._check_stderr = False           # Test author's desire to verify stderr
        self._exp_stderr = []                # List of strings to verify in stderr
        self._excl_stderr = []               # List of strings to verify are *not* in stderr
        self._verify_stderr_empty = False    # Test author's desire to verify stderr is empty
        # Exit Code
        self._check_exit_code = False        # Test author's desire to verify exit codes
        self._exp_exit_code = 0              # Optional expected exit code defined by the user

    def validate_results(self) -> Any:
        """Child class defines how to validate results of the command.

        This method must be overridden by the child class (even if you decide not to implement
        any functionality here).  This method will be called by self._run_test() once the command
        has exited.  Examples of what to do here:
            - Verify something (e.g., a file) exists
            - Verify something (e.g., a directory) is missing
            - Validate an environment variable

        Args:
            None

        Returns:
            None

        Raises:
            NotImplementedError: The child class hasn't overridden this method.
        """
        # Example Usage:
        # from hobo.disk_operations import validate_directory
        # try:
        #     validate_directory(validate_dir='/tmp', param_name='Test Dir')
        # except FileNotFoundError:
        #     self._add_test_failure(f'Unable to verify /tmp')
        raise NotImplementedError(
            self._test_error.format('The child class must override the validate_results method'))

    # TEST AUTHOR METHODS
    # Methods listed in "suggested" call order
    # 1. Set Command List
    def set_command_list(self, cmd_list: list) -> Any:
        """Specifies the command to execute for a test case.

        This method must define how the test framework utilizes subprocess to call the command
        being tested.  If any command line input is necessary, feel free to define additional
        input methods for the test author to utilize and then add that to the cmd_list.  The
        command list defined here will be utilized by self._run_test() to execute the code
        being tested.

        Args:
            None

        Returns:
            None

        Raises:
            None.  Calls self.fail() instead.
        """
        # INPUT VALIDATION
        # cmd_list
        self._validate_list(validate_this=cmd_list, param_name='cmd_list', can_be_empty=False)
        # cmd_list contents
        for cmd_entry in cmd_list:
            self._validate_string(validate_this=cmd_entry, param_name='cmd_list entry',
                                  can_be_empty=False)

        # STORE IT
        self._cmd_list = cmd_list

    # 2. Set Expected Exit Code (OPTIONAL)
    def expect_exit_code(self, exit_code: int = 0) -> None:
        """Verify the commands's exit code."""
        # INPUT VALIDATION
        self._validate_type(validate_this=exit_code, param_name='exit_code', param_type=int)
        # SET IT
        self._check_exit_code = True
        self._exp_exit_code = exit_code

    # 3. Set Expected Output (OPTIONAL)
    # 3.1 Stdout
    def expect_stdout(self, output: list) -> None:
        """Search stdout for output entries."""
        # INPUT VALIDATION
        self._validate_expected_output(output=output)
        # SET IT
        self._check_stdout = True
        self._exp_stdout += output

    def verify_stdout_empty(self) -> None:
        """Verify stdout is empty."""
        self._check_stdout = True
        self._verify_stdout_empty = True

    def verify_stdout_missing(self, output: list) -> None:
        """Verify stdout is missing the output list entries."""
        # INPUT VALIDATION
        self._validate_expected_output(output=output)
        self._check_stdout = True
        self._excl_stdout += output

    # 3.2 Stderr
    def expect_stderr(self, output: list) -> None:
        """Search stdout for output entries."""
        # INPUT VALIDATION
        self._validate_expected_output(output=output)
        # SET IT
        self._check_stderr = True
        self._exp_stderr += output

    def verify_stderr_empty(self) -> None:
        """Verify stdout is empty."""
        self._check_stderr = True
        self._verify_stderr_empty = True

    def verify_stderr_missing(self, output: list) -> None:
        """Verify stderr is missing the output list entries."""
        # INPUT VALIDATION
        self._validate_expected_output(output=output)
        self._check_stderr = True
        self._excl_stderr += output

    # 4. Run Test
    def run_test(self, verbosity: Verbosity = Verbosity.DEFAULT) -> None:
        """Execute the test case.

        Execute the test author's command and validate the results accordingly.
        This method:
        1. Validates the test author's usage
        2. Executes the command list and validates the results
        3. Presents all test failures

        Args:
            verbosity: Optional; Desired verbosity level for this test case.

        Returns:
            None

        Raises:
            None.  Calls self.fail() or self._add_test_failure() instead.
        """
        # INPUT VALIDATION
        self._verbosity = verbosity  # Store it...
        self._validate_verbosity()   # ...then check it

        # RUN IT
        # 1. CONTEXT VALIDATION
        self._validate_usage()

        # 2. RUN TEST
        self._run_test()

        # 3. REPORT
        self._present_test_results()

    # CLASS HELPER METHODS
    # Methods listed in alphabetical order
    def _execute_cmd(self) -> int:
        """Execute the command list, store output, and return the exit code.

        Override this method if you want to control execution.

        Returns:
            Exit code from execution.
        """
        # LOCAL VARIABLES
        popen_obj = start_subprocess_cmd(self._cmd_list)  # Popen object

        # RUN IT
        self._raw_stdout, self._raw_stderr = popen_obj.communicate()

        # DONE
        return popen_obj.returncode  # Exit code

    def _present_verbose_failures(self) -> None:
        """Present test failures in a verbose manner."""
        # LOCAL VARIABLES
        formatted_failures = []  # Add line numbers
        raw_stdout = []          # Pass this to _print_verbose_output()
        raw_stderr = []          # Pass this to _print_verbose_output()

        # PRESENT IT
        # Stdout
        if self._raw_stdout:
            raw_stdout.append(self._raw_stdout)
        self._print_verbose_output(self._verb_stdout_hdr, raw_stdout)
        # Stderr
        if self._raw_stderr:
            raw_stderr.append(self._raw_stderr)
        self._print_verbose_output(self._verb_stderr_hdr, raw_stderr)
        # Test Failures
        for index, failure_item in enumerate(self._test_failure_list):
            formatted_failures.append(f'{str(index+1)}. {failure_item}')
        self._print_verbose_output(self._verb_failure_hdr, formatted_failures)

    def _run_test(self) -> None:
        """Execute the test case and test results.

        1. Call a subprocess_wrapper function
        2. Validate output/exit code
        3. Validate results

        Raises:
            None.  Calls self.fail() or self._add_test_failure() instead.
        """
        # LOCAL VARIABLES
        exit_code = self._execute_cmd()  # Exit code

        # TEST RESULTS
        # Output and exit code
        self._validate_default_results(exit_code)
        # Other results
        self.validate_results()

    def _present_test_results(self) -> None:
        """Handles verbosity reporting for this test case."""
        # INTERNAL VALIDATION
        self._validate_verbosity()  # Is it valid?

        # PRESENT TEST RESULTS
        if self._verbosity is Verbosity.DEFAULT:
            self._present_test_failures()
        elif self._verbosity is Verbosity.FAIL:
            if self._test_failure_list:
                self._present_verbose_failures()
        elif self._verbosity is Verbosity.ALL:
            self._present_verbose_failures()
        else:
            self.fail_test_case(f'Unsupported Verbosity selection: {self._verbosity.name}')

        # DID WE FAIL?
        if self._test_failure_list:
            # Only executed for non-DEFAULT failures since _p_t_f() calls fail()
            self.fail('See stderr for test case details')

    def _print_verbose_output(self, header: str, contents: list[str]) -> None:
        """Format verbose output on behalf of TediousFuncTest.

        Formats and prints verbose output to stderr.

        ====================
        HEADER
        --------------------
        Contents[0]
        --------------------
        Contents[n-2]
        --------------------
        Contents[n-1]
        ====================

        Args:
            header: Header title to print in upper case.
            contents: Contents to print after the header.  If empty, prints self._verb_empty_msg
                as the contents.  If contents contains one entry, no divider will be printed.
                If contents is longer, each entry will get its own line split by dividers.

        Returns:
            None

        Raises:
            None.  Calls self.fail() instead.
        """
        # LOCAL VARIABLES
        bookend = '=' * 20  # Starts and ends the verbose table
        divider = '-' * 20  # Splits internal sections

        # INPUT VALIDATION
        self._validate_string(header, 'header', can_be_empty=False)
        self._validate_list(contents, 'contents', can_be_empty=True)

        # PRINT IT
        print(f'\n{bookend}\n{header.upper()}\n{divider}', file=sys.stderr)
        if not contents:
            print(self._verb_empty_msg, file=sys.stderr)
        else:
            print(f'{contents[0]}', file=sys.stderr)
            for entry in contents[1:]:
                print(f'{divider}\n{entry}', file=sys.stderr)
        print(bookend, file=sys.stderr)

    def _validate_expected_output(self, output: list) -> None:
        """Validates test author's expected stdout/stderr input.

        Raises:
            None.  Calls self.fail() instead.
        """
        # INPUT VALIDATION
        # output
        self._validate_list(validate_this=output, param_name='output', can_be_empty=False)
        # output entries
        for output_entry in output:
            self._validate_string(validate_this=output_entry, param_name='stdout entry',
                                  can_be_empty=True)

    # pylint: disable=too-many-branches
    def _validate_default_results(self, exit_code: int = 0) -> None:
        """Checks stdout, stderr and the exit code as applicable.

        Responds to the test cases's desire to validate stdout, stderr, and the exit code as
        indicated.  Verifies expected content exists and verifies excluded content is missing.

        Args:
            exit_code: Optional; Exit code from command execution.

        Returns:
            None

        Raises:
            None.  Calls self.fail() or self._add_test_failure() instead.
        """
        # TEST THE RESULTS
        # stdout
        if self._check_stdout:
            if self._verify_stdout_empty and self._raw_stdout:
                self._add_test_failure(f'Stdout was not empty: {self._raw_stdout}')
            else:
                for entry in self._exp_stdout:
                    if entry not in self._raw_stdout:
                        self._add_test_failure(f'Unable to locate {entry} in stdout')
                for entry in self._excl_stdout:
                    if entry in self._raw_stdout:
                        self._add_test_failure(f'Found excluded entry {entry} in stdout')
        # stderr
        if self._check_stderr:
            if self._verify_stderr_empty and self._raw_stderr:
                self._add_test_failure(f'Stderr was not empty: {self._raw_stderr}')
            else:
                for entry in self._exp_stderr:
                    if entry not in self._raw_stderr:
                        self._add_test_failure(f'Unable to locate {entry} in stderr')
                for entry in self._excl_stderr:
                    if entry in self._raw_stderr:
                        self._add_test_failure(f'Found excluded entry {entry} in stderr')
        # Exit code
        if self._check_exit_code:
            if self._exp_exit_code != exit_code:
                self._add_test_failure(f'Expected exit code ({self._exp_exit_code}) '
                                       f'does not match actual exit code ({exit_code})')
    # pylint: enable=too-many-branches

    def _validate_usage(self) -> None:
        """Validate test author's usage.

        Verify the test author hasn't neglected to make a mandatory function call.

        Args:
            None

        Returns:
            None

        Raises:
            None.  Calls self.fail() instead.
        """
        # Command list
        if not self._cmd_list:
            self.fail(self._test_error.format('No command list was found.  '
                                              'Call self.set_command_list()'))
        # Check stdout
        if self._exp_stdout and self._verify_stdout_empty:
            self.fail(self._test_error.format('Decide whether or not you want stdout'))
        # Check stderr
        if self._exp_stderr and self._verify_stderr_empty:
            self.fail(self._test_error.format('Decide whether or not you want stderr'))

    def _validate_verbosity(self) -> None:
        """Validate self._verbosity."""
        self._validate_type(self._verbosity, 'TediousFuncTest._verbosity', param_type=Verbosity)
# pylint: enable=too-many-instance-attributes
