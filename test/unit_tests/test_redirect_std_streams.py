"""Unit test the RedirectStdStreams.communicate() method.

Run the test cases defined in this module using any of the example commands below:

    Usage:
    python -m unittest                                   # Run *ALL* test cases
    python -m unittest -k TestRedirectStdStreams         # Match this test class
    python -m test.unit_tests                            # Run all unit tests
    python -m test.unit_tests.test_redirect_std_streams  # Run just these tests
"""

# Standard Imports
from typing import Any
import io
import os
import random
import string
import sys
import unittest
# Third Party Imports
from hobo.disk_operations import find_path_to_dir
from hobo.validation import validate_string, validate_type
# Local Imports
from tediousstart.redirect_std_streams import RedirectStdStreams
from tediousstart.tediousstart import execute_test_cases
from tediousstart.tediousunittest import TediousUnitTest


MB = 1048576  # Size of 1 MB


def loud_function(std_out: str, std_err: str) -> None:
    """A function that prints to facilitate testing of RedirectStdStreams().

    Args:
        std_out: Print this string to stdout.
        std_err: Print this string to stderr.

    Raises:
        TypeError for a non-string.  (We're not testing loud_function() here so, don't.)
    """
    # INPUT VALIDATION
    validate_string(std_out, 'std_out', can_be_empty=True)
    validate_string(std_err, 'std_err', can_be_empty=True)

    # BE LOUD
    print(std_out, file=sys.stdout)
    print(std_err, file=sys.stderr)


def salt_actual_output(actual_output: str, salt_len: int = 10) -> str:
    """Prepend and append random values to actual output.

    Args:
        actual_output: A string, empty or otherwise, to prepend and append with random values.
        sal_len: Optional; Length of the salt to prepend and append.  Value must be 0 or greater.
            A value of 0 will result in no salt and actual_output will be returned.

    Returns:
        actual_output but prepended and appended by random values.

    Raises:
        TypeError: Bad data type
        ValueError: Invalid salt_len
    """
    # LOCAL VARIABLES
    salted_output = actual_output                           # Salted output
    available_chars = string.printable.replace('\r', '\n')  # See Special 16

    # INPUT VALIDATION
    validate_string(actual_output, 'actual_output', can_be_empty=True)
    validate_type(salt_len, 'salt_len', int)
    if salt_len < 0:
        raise ValueError(f'Invalid salt length of {salt_len}')

    # SALT IT
    if salt_len > 0:
        salted_output = ''.join(random.choices(available_chars, k=salt_len)) \
                        + actual_output + ''.join(random.choices(available_chars, k=salt_len))

    # DONE
    return salted_output


def stringify(begin: int, end: int) -> str:
    """Concatenate a range of integers and their character values into a string.

    The format of the string will be str(ordinal) + ' ' + chr(ordinal) for each number in range.

    Args:
        begin: The start of the range.  Must be a number greater than -1 and less than 0x110000.
            Must also be less than or equal to end.
        end: The end of the range, inclusive.  Must be a number greater than -1 and less than
            0x110000.  Must also be greater than or equal to end.

    Returns:
        A string containing the str(ordinal) + chr(ordinal) for each inclusive character within
        range begin to end.  Other than spaces, for readability, no additional whitespace wil be
        added to the string.

    Raises:
        TypeError: Bad data type.
        ValueError: End is greater than begin.
        OverflowError: A value is outside the supported range.
    """
    # LOCAL VARIABLES
    ret_val = ''  # The string of ordinals and their character values

    # INPUT VALIDATION
    validate_type(begin, 'begin', int)
    validate_type(end, 'end', int)
    if begin >= 0x110000 or end >= 0x110000:
        raise OverflowError('Range value too large')
    if begin < 0 or end < 0:
        raise OverflowError('Range value too small')
    if begin > end:
        raise ValueError('begin can not be greater than end')

    # STRINGIFY IT
    for ordinal in range(begin, end + 1):
        ret_val = ret_val + str(ordinal) + ' ' + chr(ordinal) + ' '

    # DONE
    return ret_val


class TestRedirectStdStreams(TediousUnitTest):
    """TestRedirectStdStreams unit test class.

    This class provides base functionality to run NEBS unit tests for
    RedirectStdStreams.communicate().
    """

    # CORE CLASS METHODS
    # Methods listed in call order
    def __init__(self, *args, **kwargs) -> None:
        """TediousUnitTest ctor.

        TediousUnitTest constructor.  Initializes attributes after constructing the parent
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

        self._defined_test_input = True  # Setting the test input is optional here
        self._stdout_arg = None          # The stdout arg to pass to the RedirectStdStreams ctor
        self._stderr_arg = None          # The stderr arg to pass to the RedirectStdStreams ctor
        self._loud_stdout = ''           # The stdout for loud_function() to print
        self._loud_stderr = ''           # The stderr for loud_function() to print
        self._test_file_output_dir = ''  # Output directory for test files

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

        self._test_file_output_dir = os.path.join(find_path_to_dir('tedious-start'),
                                                  'test', 'unit_tests', 'test_output')
        self._validate_directory(self._test_file_output_dir, 'unit test file output directory',
                                 must_exist=True)
        self._delete_files(self._test_file_output_dir, exempt=['.placeholder'])

    def tearDown(self) -> None:
        """Cleanup after the Test Case.

        Automate any cleanup necessary before the Test Case completes.
        """
        super().tearDown()
        self._delete_files(self._test_file_output_dir, exempt=['.placeholder'])

    def call_callable(self) -> Any:
        """Calls TediousStart.fail_test_case().

        Overrides the parent method.  Defines the way to call RedirectStdStreams.communicate().

        Args:
            None

        Returns:
            Return value of RedirectStdStreams.communicate()

        Raises:
            Exceptions raised by RedirectStdStreams.communicate() are bubbled up and handled by
            TediousUnitTest
        """
        # LOCAL VARIABLES
        actual_ret = None  # Return value from the call to communicate()

        # CALL IT
        with RedirectStdStreams(stdout=self._stdout_arg, stderr=self._stderr_arg) as test_obj:
            loud_function(std_out=self._loud_stdout, std_err=self._loud_stderr)
            actual_ret = test_obj.communicate()

        # DONE
        return actual_ret

    def set_actual_stderr(self, std_err: str) -> None:
        """Choose the stderr output to be redirected by RedirectStdStreams()."""
        self._validate_string(std_err, 'std_err', can_be_empty=True)
        self._loud_stderr = std_err

    def set_actual_stdout(self, std_out: str) -> None:
        """Choose the stdout output to be redirected by RedirectStdStreams()."""
        self._validate_string(std_out, 'std_out', can_be_empty=True)
        self._loud_stdout = std_out

    def set_stderr_arg(self, std_err_arg: Any) -> None:
        """Set the argument being used by RedirectStdStreams(stderr=???).

        This method is optional.  Default value is already None which is valid input for the ctor.
        """
        self._stderr_arg = std_err_arg

    def set_stdout_arg(self, std_out_arg: Any) -> None:
        """Set the argument being used by RedirectStdStreams(stdout=???).

        This method is optional.  Default value is already None which is valid input for the ctor.
        """
        self._stdout_arg = std_out_arg

    def validate_return_value(self, return_value: Any) -> None:
        """Validate TediousStart.fail_test_case() return value.

        Overrides the parent method.  Defines how the test framework validates the return value
        of a completed call.

        Args:
            return_value: This is ignored.  self.fail_test_case() should return None, if ever.
        """
        # Type
        if not isinstance(return_value, type(self._exp_return)):
            self._add_test_failure(f'Expected type {type(self._exp_return)} '
                                   f'but it was of type {type(return_value)}')
        # Value
        elif len(return_value) != len(self._exp_return):
            self._add_test_failure(f'Expected length of "{len(self._exp_return)}" '
                                   f'but received length of "{len(return_value)}" instead')
        else:
            for exp_entry, actual_entry in zip(self._exp_return, return_value):
                if exp_entry not in actual_entry:
                    self._add_test_failure(f'Unable to find expected entry "{exp_entry}" '
                                           f'in actual entry "{actual_entry}"')


class NormalTestRedirectStdStreams(TestRedirectStdStreams):
    """Normal Test Cases.

    Organize the Normal Test Cases.
    """

    def test_normal_01(self):
        """Actual stdout, actual stderr, no stdout stream, no stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        # Not in this test case
        # TEST IT
        self.expect_return(tuple((actual_stdout, actual_stderr)))
        self.run_test()

    def test_normal_02(self):
        """Actual stdout, actual stderr, file-based stdout stream, file-based stderr stream.

        Salting these file-based streams was causing intermittent failures so I explicitly
        added a special test case to investigate that.  That's why this actual output isn't
        being salted.
        """
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        std_out_file = os.path.join(self._test_file_output_dir, 'normal_02_stdout.txt')
        std_err_file = os.path.join(self._test_file_output_dir, 'normal_02_stderr.txt')
        with open(std_out_file, 'w+', encoding='utf-8') as local_stdout_stream, \
             open(std_err_file, 'w+', encoding='utf-8') as local_stderr_stream:
            self.set_stdout_arg(local_stdout_stream)
            self.set_stderr_arg(local_stderr_stream)
            # TEST IT
            self.expect_return(tuple((actual_stdout, actual_stderr)))
            self.run_test()

    def test_normal_03(self):
        """Actual stdout, actual stderr, local stdout stream, local stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO()
        local_stderr_stream = io.StringIO()
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        self.expect_return(tuple((actual_stdout, actual_stderr)))
        self.run_test()

    def test_normal_04(self):
        """Actual stdout, actual stderr, sys.stdout stdout stream, sys.stderr stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('Ignore this stdout.', salt_len=0)
        actual_stderr = salt_actual_output('Ignore this stderr.', salt_len=0)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        self.set_stdout_arg(sys.stdout)
        self.set_stderr_arg(sys.stderr)
        # TEST IT
        self.expect_return(tuple(('', '')))  # The sys.std* streams have already consumed the data
        self.run_test()

    def test_normal_05(self):
        """No stdout, No stderr, no stdout stream, no stderr stream."""
        # SET ACTUAL OUTPUT
        # Not in this test case
        # SET ARG STREAMS
        # Not in this test case
        # TEST IT
        self.expect_return(tuple(('', '')))
        self.run_test()

    def test_normal_06(self):
        """No stdout, No stderr, file-based stdout stream, file-based stderr stream."""
        # SET ACTUAL OUTPUT
        # Not in this test case
        # SET ARG STREAMS
        std_out_file = os.path.join(self._test_file_output_dir, 'normal_06_stdout.txt')
        std_err_file = os.path.join(self._test_file_output_dir, 'normal_06_stderr.txt')
        with open(std_out_file, 'w+', encoding='utf-8') as local_stdout_stream, \
             open(std_err_file, 'w+', encoding='utf-8') as local_stderr_stream:
            self.set_stdout_arg(local_stdout_stream)
            self.set_stderr_arg(local_stderr_stream)
            # TEST IT
            self.expect_return(tuple(('', '')))
            self.run_test()

    def test_normal_07(self):
        """No stdout, No stderr, local stdout stream, local stderr stream."""
        # SET ACTUAL OUTPUT
        # Not in this test case
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO()
        local_stderr_stream = io.StringIO()
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        self.expect_return(tuple(('', '')))
        self.run_test()

    def test_normal_08(self):
        """No stdout, No stderr, sys.stdout stdout stream, sys.stderr stderr stream."""
        # SET ACTUAL OUTPUT
        # Not in this test case
        # SET ARG STREAMS
        self.set_stdout_arg(sys.stdout)
        self.set_stderr_arg(sys.stderr)
        # TEST IT
        self.expect_return(tuple(('', '')))
        self.run_test()

    def test_normal_09(self):
        """Actual stdout, No stderr, no stdout stream, no stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        self.set_actual_stdout(actual_stdout)
        # SET ARG STREAMS
        # Not in this test case
        # TEST IT
        self.expect_return(tuple((actual_stdout, '')))
        self.run_test()

    def test_normal_10(self):
        """Actual stdout, No stderr, file-based stdout stream, file-based stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        self.set_actual_stdout(actual_stdout)
        # SET ARG STREAMS
        std_out_file = os.path.join(self._test_file_output_dir, 'normal_10_stdout.txt')
        std_err_file = os.path.join(self._test_file_output_dir, 'normal_10_stderr.txt')
        with open(std_out_file, 'w+', encoding='utf-8') as local_stdout_stream, \
             open(std_err_file, 'w+', encoding='utf-8') as local_stderr_stream:
            self.set_stdout_arg(local_stdout_stream)
            self.set_stderr_arg(local_stderr_stream)
            # TEST IT
            self.expect_return(tuple((actual_stdout, '')))
            self.run_test()

    def test_normal_11(self):
        """Actual stdout, No stderr, local stdout stream, local stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        self.set_actual_stdout(actual_stdout)
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO()
        local_stderr_stream = io.StringIO()
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        self.expect_return(tuple((actual_stdout, '')))
        self.run_test()

    def test_normal_12(self):
        """Actual stdout, No stderr, sys.stdout stdout stream, sys.stderr stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('Ignore this stdout.', salt_len=0)
        self.set_actual_stdout(actual_stdout)
        # SET ARG STREAMS
        self.set_stdout_arg(sys.stdout)
        self.set_stderr_arg(sys.stderr)
        # TEST IT
        self.expect_return(tuple(('', '')))  # The sys.std* streams have already consumed the data
        self.run_test()

    def test_normal_13(self):
        """No stdout, actual stderr, no stdout stream, no stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        # Not in this test case
        # TEST IT
        self.expect_return(tuple(('', actual_stderr)))
        self.run_test()

    def test_normal_14(self):
        """No stdout, actual stderr, file-based stdout stream, file-based stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        std_out_file = os.path.join(self._test_file_output_dir, 'normal_14_stdout.txt')
        std_err_file = os.path.join(self._test_file_output_dir, 'normal_14_stderr.txt')
        with open(std_out_file, 'w+', encoding='utf-8') as local_stdout_stream, \
             open(std_err_file, 'w+', encoding='utf-8') as local_stderr_stream:
            self.set_stdout_arg(local_stdout_stream)
            self.set_stderr_arg(local_stderr_stream)
            # TEST IT
            self.expect_return(tuple(('', actual_stderr)))
            self.run_test()

    def test_normal_15(self):
        """No stdout, actual stderr, local stdout stream, local stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO()
        local_stderr_stream = io.StringIO()
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        self.expect_return(tuple(('', actual_stderr)))
        self.run_test()

    def test_normal_16(self):
        """No stdout, actual stderr, sys.stdout stdout stream, sys.stderr stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stderr = salt_actual_output('Ignore this stderr.', salt_len=0)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        self.set_stdout_arg(sys.stdout)
        self.set_stderr_arg(sys.stderr)
        # TEST IT
        self.expect_return(tuple(('', '')))  # The sys.std* streams have already consumed the data
        self.run_test()


class ErrorTestRedirectStdStreams(TestRedirectStdStreams):
    """Error Test Cases.

    Organize the Error Test Cases.
    """

    def test_error_01(self):
        """Bad data type - stdout is a string."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        bad_stdout_stream = ''
        local_stderr_stream = io.StringIO()
        self.set_stdout_arg(bad_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_error_02(self):
        """Bad data type - stderr is a string."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO()
        bad_stderr_stream = b''
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(bad_stderr_stream)
        # TEST IT
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_error_03(self):
        """Bad data type - stdout is an io.IOBase."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        bad_stdout_stream = io.IOBase('')
        local_stderr_stream = io.StringIO()
        self.set_stdout_arg(bad_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_error_04(self):
        """Bad data type - stderr is an io.IOBase."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO()
        bad_stderr_stream = io.IOBase('')
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(bad_stderr_stream)
        # TEST IT
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_error_05(self):
        """Bad data type - stdout is an io.RawIOBase."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        bad_stdout_stream = io.RawIOBase('')
        local_stderr_stream = io.StringIO()
        self.set_stdout_arg(bad_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_error_06(self):
        """Bad data type - stderr is an io.RawIOBase."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO()
        bad_stderr_stream = io.RawIOBase('')
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(bad_stderr_stream)
        # TEST IT
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_error_07(self):
        """Bad data type - stdout is an io.BufferedIOBase."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        bad_stdout_stream = io.BufferedIOBase('')
        local_stderr_stream = io.StringIO()
        self.set_stdout_arg(bad_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_error_08(self):
        """Bad data type - stderr is an io.BufferedIOBase."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO()
        bad_stderr_stream = io.BufferedIOBase('')
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(bad_stderr_stream)
        # TEST IT
        self.expect_exception(TypeError, 'expected type')
        self.run_test()

    def test_error_09(self):
        """Bad data type - stdout is a binary encoded file-based stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.', salt_len=0)
        actual_stderr = salt_actual_output('This is my stderr.', salt_len=0)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        std_out_file = os.path.join(self._test_file_output_dir, 'normal_02_stdout.txt')
        std_err_file = os.path.join(self._test_file_output_dir, 'normal_02_stderr.txt')
        with open(std_out_file, 'bw+') as bad_stdout_stream, \
             open(std_err_file, 'w+', encoding='utf-8') as local_stderr_stream:
            self.set_stdout_arg(bad_stdout_stream)
            self.set_stderr_arg(local_stderr_stream)
            # TEST IT
            self.expect_exception(TypeError, 'expected type')
            self.run_test()

    def test_error_10(self):
        """Bad data type - stderr is a binary encoded file-based stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.', salt_len=0)
        actual_stderr = salt_actual_output('This is my stderr.', salt_len=0)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        std_out_file = os.path.join(self._test_file_output_dir, 'normal_02_stdout.txt')
        std_err_file = os.path.join(self._test_file_output_dir, 'normal_02_stderr.txt')
        with open(std_out_file, 'w+', encoding='utf-8') as local_stdout_stream, \
             open(std_err_file, 'bw+') as bad_stderr_stream:
            self.set_stdout_arg(local_stdout_stream)
            self.set_stderr_arg(bad_stderr_stream)
            # TEST IT
            self.expect_exception(TypeError, 'expected type')
            self.run_test()


class BoundaryTestRedirectStdStreams(TestRedirectStdStreams):
    """Boundary Test Cases.

    Organize the Boundary Test Cases.
    """

    def test_boundary_01(self):
        """Noisy stdout, no stdout stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = ''.join(random.choices(string.ascii_letters + string.digits
                                               + string.punctuation, k=10*MB))
        self.set_actual_stdout(actual_stdout)
        # SET ARG STREAMS
        # Not in this test case
        # TEST IT
        self.expect_return(tuple((actual_stdout, '')))
        self.run_test()

    def test_boundary_02(self):
        """Noisy stderr, no stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stderr = ''.join(random.choices(string.ascii_letters + string.digits
                                               + string.punctuation, k=10*MB))
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        # Not in this test case
        # TEST IT
        self.expect_return(tuple(('', actual_stderr)))
        self.run_test()


class SpecialTestRedirectStdStreams(TestRedirectStdStreams):
    """Special Test Cases.

    Organize the Special Test Cases.
    """

    def test_special_01(self):
        """Mix and match streams: stdout None, stderr file-based."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        std_err_file = os.path.join(self._test_file_output_dir, 'special_01_stderr.txt')
        with open(std_err_file, 'w+', encoding='utf-8') as local_stderr_stream:
            self.set_stderr_arg(local_stderr_stream)
            # TEST IT
            self.expect_return(tuple((actual_stdout, actual_stderr)))
            self.run_test()

    def test_special_02(self):
        """Mix and match streams: stdout file-based, stderr local."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        std_out_file = os.path.join(self._test_file_output_dir, 'special_02_stdout.txt')
        local_stderr_stream = io.StringIO()
        with open(std_out_file, 'w+', encoding='utf-8') as local_stdout_stream:
            self.set_stdout_arg(local_stdout_stream)
            self.set_stderr_arg(local_stderr_stream)
            # TEST IT
            self.expect_return(tuple((actual_stdout, actual_stderr)))
            self.run_test()

    def test_special_03(self):
        """Mix and match streams: stdout local, stderr sys.stderr."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('Ignore this stderr.', salt_len=0)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO()
        local_stderr_stream = sys.stderr
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        # The sys.stderr stream has already consumed the data
        self.expect_return(tuple((actual_stdout, '')))
        self.run_test()

    def test_special_04(self):
        """Mix and match streams: stdout sys.stdout, stderr None."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('Ignore this stdout.', salt_len=0)
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = sys.stdout
        self.set_stdout_arg(local_stdout_stream)
        # TEST IT
        # The sys.stderr stream has already consumed the data
        self.expect_return(tuple(('', actual_stderr)))
        self.run_test()

    def test_special_05(self):
        """Flip flop sys.stdout and sys.stderr for funsies."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('Ignore this stdout.', salt_len=0)
        actual_stderr = salt_actual_output('Ignore this stderr.', salt_len=0)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = sys.stdout
        local_stderr_stream = sys.stderr
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        # The sys.std* streams have already consumed the data
        self.expect_return(tuple(('', '')))
        self.run_test()

    def test_special_06(self):
        """All in one: file-based stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        expected_result = actual_stdout + '\n' + actual_stderr
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        std_out_file = os.path.join(self._test_file_output_dir, 'special_06_all-in-one.txt')
        with open(std_out_file, 'w+', encoding='utf-8') as local_stream:
            self.set_stdout_arg(local_stream)
            self.set_stderr_arg(local_stream)
            # TEST IT
            # This is an odd test because it's possible that the user may want to duplicate
            # the output by using the same stream.
            self.expect_return(tuple((expected_result, expected_result)))
            self.run_test()

    def test_special_07(self):
        """All in one: local stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = salt_actual_output('This is my stderr.')
        expected_result = actual_stdout + '\n' + actual_stderr
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stream = io.StringIO()
        self.set_stdout_arg(local_stream)
        self.set_stderr_arg(local_stream)
        # TEST IT
        # This is an odd test because it's possible that the user may want to duplicate
        # the output by using the same stream.
        self.expect_return(tuple((expected_result, expected_result)))
        self.run_test()

    def test_special_08(self):
        """All in one: sys.stdout stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('stdout.', salt_len=0)
        actual_stderr = salt_actual_output('stderr.', salt_len=0)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stream = sys.stdout
        self.set_stdout_arg(local_stream)
        self.set_stderr_arg(local_stream)
        # TEST IT
        # This is an odd test because it's possible that the user may want to duplicate
        # the output by using the same stream.
        self.expect_return(tuple(('', '')))  # The sys.stdout stream has already consumed the data
        self.run_test()

    def test_special_09(self):
        """All in one: sys.stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('stdout.', salt_len=0)
        actual_stderr = salt_actual_output('stderr.', salt_len=0)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stream = sys.stderr
        self.set_stdout_arg(local_stream)
        self.set_stderr_arg(local_stream)
        # TEST IT
        # This is an odd test because it's possible that the user may want to duplicate
        # the output by using the same stream.
        self.expect_return(tuple(('', '')))  # The sys.stdout stream has already consumed the data
        self.run_test()

    def test_special_10(self):
        """Actual stdout, actual stderr, local stdout 'noisy' stream, local stderr stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.', salt_len=0)
        actual_stderr = salt_actual_output('This is my stderr.', salt_len=0)
        dirty_stream = salt_actual_output('', salt_len=100)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO(dirty_stream)
        local_stderr_stream = io.StringIO()
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        # Actual output overwrites the beginning of the existing 'dirty' stream but the remainder
        # of the 'dirty' stream still exists
        self.expect_return(tuple((actual_stdout + dirty_stream[len(dirty_stream):],
                                  actual_stderr)))
        self.run_test()

    def test_special_11(self):
        """Actual stdout, actual stderr, local stdout stream, local stderr 'noisy' stream."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.', salt_len=0)
        actual_stderr = salt_actual_output('This is my stderr.', salt_len=0)
        dirty_stream = salt_actual_output('', salt_len=100)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO()
        local_stderr_stream = io.StringIO(dirty_stream)
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        # Actual output overwrites the beginning of the existing 'dirty' stream but the remainder
        # of the 'dirty' stream still exists
        self.expect_return(tuple((actual_stdout,
                                  actual_stderr + dirty_stream[len(dirty_stream):])))
        self.run_test()

    def test_special_12(self):
        """Actual stdout, actual stderr, local 'noisy' streams: stdout and stderr."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.', salt_len=0)
        actual_stderr = salt_actual_output('This is my stderr.', salt_len=0)
        dirty_stdout = salt_actual_output('', salt_len=100)
        dirty_stderr = salt_actual_output('', salt_len=100)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        local_stdout_stream = io.StringIO(dirty_stdout)
        local_stderr_stream = io.StringIO(dirty_stderr)
        self.set_stdout_arg(local_stdout_stream)
        self.set_stderr_arg(local_stderr_stream)
        # TEST IT
        # Actual output overwrites the beginning of the existing 'dirty' stream but the remainder
        # of the 'dirty' stream still exists
        self.expect_return(tuple((actual_stdout + dirty_stdout[len(dirty_stdout):],
                                  actual_stderr + dirty_stderr[len(dirty_stderr):])))
        self.run_test()

    def test_special_13(self):
        """Actual stdout with non-printable characters, actual stderr, no streams."""
        # SET ACTUAL OUTPUT
        actual_stdout = stringify(0, 0x1100)
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        # Not in this test case
        # TEST IT
        self.expect_return(tuple((actual_stdout, actual_stderr)))
        self.run_test()

    def test_special_14(self):
        """Actual stdout, actual stderr with non-printable characters, no streams."""
        # SET ACTUAL OUTPUT
        actual_stdout = salt_actual_output('This is my stdout.')
        actual_stderr = stringify(0, 0x1100)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        # Not in this test case
        # TEST IT
        self.expect_return(tuple((actual_stdout, actual_stderr)))
        self.run_test()

    def test_special_15(self):
        """Actual stdout and stderr with non-printable characters, no streams."""
        # SET ACTUAL OUTPUT
        actual_stdout = stringify(0, 0x500)
        actual_stderr = stringify(0x500, 0x1000)
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        # Not in this test case
        # TEST IT
        self.expect_return(tuple((actual_stdout, actual_stderr)))
        self.run_test()

    @unittest.skip('BUG(?): File-based streams result in unexpected output when handling chr(0xD)')
    def test_special_16(self):
        """Whitespace characters are causing intermittent failures for file-based streams.

        Some combination of random.choices(string.printable) and using file-based output streams
        was causing intermittent failures on normal 2.  Turns out it came from string.whitespace.
        This BUG(?) does not appear in any of the other stream formats: None, io.StringIO(), etc.

        The BUG seems to be restricted to the '\r' character.  These test were run on Ubuntu 22.04.
        '\n' is for Unix
        '\r' is for Mac (before OS X)
        '\r\n' is for Windows format
        """
        # SET ACTUAL OUTPUT
        # string.whitespace = ' \t\n\r\x0b\x0c'
        actual_stdout = 'The (\r) character fails this test in Linux.'
        actual_stderr = salt_actual_output('This is my stderr.')
        self.set_actual_stdout(actual_stdout)
        self.set_actual_stderr(actual_stderr)
        # SET ARG STREAMS
        std_out_file = os.path.join(self._test_file_output_dir, 'special_16_stdout.txt')
        std_err_file = os.path.join(self._test_file_output_dir, 'special_16_stderr.txt')
        with open(std_out_file, 'w+', encoding='utf-8') as local_stdout_stream, \
             open(std_err_file, 'w+', encoding='utf-8') as local_stderr_stream:
            self.set_stdout_arg(local_stdout_stream)
            self.set_stderr_arg(local_stderr_stream)
            # TEST IT
            self.expect_return(tuple((actual_stdout, actual_stderr)))
            self.run_test()


if __name__ == '__main__':
    execute_test_cases()
