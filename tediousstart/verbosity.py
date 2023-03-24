"""Defines Verbosity Enum class.

The tediousstart.Verbosity class will communicate desired verbosity levels to TediousFuncTest.

    Typical usage example:

    class VerboseTestCases(TediousFuncTest):

    def test_special_01(self):
        std_output = 'Verbosity.FAIL only verbosely prints on test case failure'
        self.set_command_list(['echo', '-n', std_output])
        self.expect_stdout([std_output])
        self.verify_stderr_empty()
        self.run_test(Verbosity.FAIL)

    def test_special_02(self):
        std_output = 'Verbosity.ALL always verbosely prints'
        self.set_command_list(['echo', '-n', std_output])
        self.expect_stdout([std_output])
        self.verify_stderr_empty()
        self.run_test(Verbosity.ALL)
"""

# Standard Imports
from enum import Enum
# Third Party Imports
# Local Imports


class Verbosity(Enum):
    """Communicates desired verbosity to TediousFuncTest.run_test().

    Attributes:
        DEFAULT  # Default behavior: Present terse failure messages on test case failure
        FAIL     # Present verbose output on test case failure
        ALL      # Always present verbose output regardless of success or failure
    """
    DEFAULT = 0
    FAIL = 1
    ALL = 2
