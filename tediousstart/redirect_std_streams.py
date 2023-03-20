"""Defines RedirectStdStreams class.

The RedirectStdStreams class will redirect the stdout and stderr of everything executed within
its context to an io.TextIOBase stream.  It was added to TEDIOUS START (TEST) to silence/redirect
stdout and stderr output to the test case itself (instead of the terminal).

RedirectStdStreams has been tested can create its own internal streams but also allows the caller
to utilize their own.  RedirectStdStreams has been successfully tested with the following
io.TextIOBase stream types: file-based, user-instantiated, and sys.std* streams.  There is a
known BUG(?) when using file-based streams with the '\r' (chr(0xD)) character.  The output may
not be exactly as expected so take care when comparing the actual output to the expected output.

    Supported usage examples:

    # To silence a function call by redirecting the standard streams to the OS's devnull...
    with open(os.devnull, 'w', encoding='utf-8') as devnull:  # Shunt for output
        with RedirectStdStreams(stdout=devnull, stderr=devnull):
            loud_function()

    # To save a function call's output by redirecting the standard streams to variables...
    std_out = ''  # Store the stdout output
    std_err = ''  # Store the stderr output
    with RedirectStdStreams() as temp_obj:
        loud_function()
        (std_out, std_err) = temp_obj.communicate()
    print(f'loud_function() tried to output {std_out} and {std_err}')

    # This class also supports local io.StringIO() streams for redirection
    stdout_stream = io.StringIO()  # Stream to redirect stdout to
    stderr_stream = io.StringIO()  # Stream to redirect stdout to
    with RedirectStdStreams(stdout=stdout_stream, stderr=stderr_stream) as temp_obj:
        loud_function()
    stdout_stream.seek(0)
    print(f'loud_function() tried to output {std_out.read()}')
"""

# Standard Imports
from typing import Tuple
import io
import sys
# Third Party Imports
from hobo.validation import validate_type
# Local Imports


class RedirectStdStreams():
    """Temporarily redirect output streams.

    Adapted from: https://stackoverflow.com/a/6796752

    Typical usage examples:
    std_out = ''  # Store the stdout output
    std_err = ''  # Store the stderr output
    with RedirectStdStreams() as temp_obj:
        loud_function()
        (std_out, std_err) = temp_obj.communicate()
    print(f'loud_function() tried to output {std_out} and {std_err}')

    For more details:
        import tediousstart.redirect_std_streams
        help(tediousstart.redirect_std_streams)
    """
    def __init__(self, stdout:io.TextIOBase=None, stderr:io.TextIOBase=None) -> None:
        """RedirectStdStreams class ctor.

        Args:
            stdout: Optional; Text based io stream to replace stdout with.  If not defined, the
                class instantiates an io.TextIOBase object to use as a stream instead.
            stderr: Optional; Text based io stream to replace stderr with.  If not defined, the
                class instantiates an io.TextIOBase object to use as a stream instead.
        """
        # ATTRIBUTES
        self._stdout = None      # Redirect stdout here
        self._stderr = None      # Redirect stderr here
        self._old_stdout = None  # Save the original stdout
        self._old_stderr = None  # Save the original stderr

        # PREPARATION
        # stdout
        if stdout is None:
            self._stdout = io.StringIO("")
        else:
            self._stdout = stdout
        # stderr
        if stderr is None:
            self._stderr = io.StringIO("")
        else:
            self._stderr = stderr

    def _validate(self) -> None:
        """Validates the attributes."""
        validate_type(self._stdout, 'stdout', io.TextIOBase)
        validate_type(self._stderr, 'stderr', io.TextIOBase)

    def __enter__(self) -> object:
        self._validate()
        self._old_stdout, self._old_stderr = sys.stdout, sys.stderr
        self._old_stdout.flush()
        self._old_stderr.flush()
        sys.stdout, sys.stderr = self._stdout, self._stderr
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self._stdout.flush()
        self._stderr.flush()
        sys.stdout = self._old_stdout
        sys.stderr = self._old_stderr

    def communicate(self) -> Tuple[str, str]:
        return tuple((_read_text_stream(self._stdout), _read_text_stream(self._stderr)))


def _read_text_stream(read_this:io.TextIOBase) -> str:
    # LOCAL VARIABLES
    text_from_stream = ''  # Text read from read_this

    # INPUT VALIDATION
    validate_type(read_this, 'read_this', io.TextIOBase)

    # READ IT
    if read_this.seekable():
        read_this.seek(0)  # Rewind the stream
    if read_this.readable():
        text_from_stream = read_this.read()

    # DONE
    return text_from_stream
