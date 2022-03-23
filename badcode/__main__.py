"""Permits the Bad Code package to be executed.

    Usage: python3 -m badcode <integer> <integer>  # This should be enough
"""

# Standard Imports
import sys
# Third Party Imports
# Local Imports
from badcode.main import main


def execute(args: list) -> int:
    """Execute the Bad Code package.

    Args:
        args: A list of arguments, as strings, from the command line
    """
    return main(args)


if __name__ == '__main__':
    # NOTE: From pydocs...
    # Most systems require [sys.exit([arg])'s optional argument arg] to
    #   be in the range 0–127, and produce undefined results otherwise.
    sys.exit(execute(sys.argv))
