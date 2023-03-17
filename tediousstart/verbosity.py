"""Defines Verbosity Enum class.

The tediousstart.Verbosity class will communicate desired verbosity levels to TediousFuncTest.

    Typical usage example:

    TODO: DON'T DO NOW... Actual TediousFuncTest.run_test() example
"""

# Standard Imports
from enum import Enum
# Third Party Imports
# Local Imports


class Verbosity(Enum):
    DEFAULT=0  # Default behavior: Present terse failure messages on test case failure
    FAIL=1     # Present verbose output on test case failure
    ALL=2      # Always present verbose output regardless of success or failure
