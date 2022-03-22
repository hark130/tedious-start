"""Bad Code exists solely to test the Tedious Start (TEST) test code.

    Typical usage example:

    TO DO: DON'T DO NOW... Put some instructions here
"""

# Standard Imports
# Third Party Imports
from hobo.misc import print_exception
# Local Imports
from badcode.parser import parse_arguments
from badcode.maths import divide_it


def main(args: list) -> int:
    """Executes Bad Code.

    1. Reads the numbers provided at the CLI
    2. Divides the first by the second
    3. Prints the result

    Args:
        args: A list of arguments, as strings, from the command line

    Returns:
        0 on success
        1 on bad argument(s)
        2 on failed execution

    Raises:
        None
    """
    # LOCAL VARIABLES
    cli_num = 0   # Command line numerator
    cli_den = 0   # Command line denominator
    quotient = 0  # cli_num / cli_den
    success = 0   # 0 on success, 1 on bad argument, 2 on failed execution

    # PARSE ARGUMENTS
    try:
        (cli_num, cli_den) = parse_arguments(args)
    except (TypeError, ValueError, RuntimeError) as err:
        print_exception(err)
        success = 1

    # DO IT
    else:
        try:
            quotient = divide_it(cli_num, cli_den)
        except (TypeError, ValueError) as err:
            print_exception(err)
            success = 2

    # PRINT IT
    if success == 0:
        print(f'{cli_num} / {cli_den} = {quotient}')

    # DONE
    return success
