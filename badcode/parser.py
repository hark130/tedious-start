"""Parse Bad Code command line arguments."""


def parse_arguments(args: list) -> str:
    """Parse the command line arguments and return a single arg.

    Args:
        args: A list of arguments, as strings, from the command line

    Returns: The first command line argument

    Raises:
        TypeError: Bad type found
        ValueError: Bad value found
        RuntimeError: Wrong number of arguments
    """
    # LOCAL VARIABLES
    arg1 = 0  # First argument as an int
    arg2 = 0  # Second argument as an int

    # INPUT VALIDATION
    _validate_parameters(args)

    # CONVERSION
    arg1 = _convert_it(args[1])
    arg2 = _convert_it(args[2])

    # GET ARGUMENT
    return tuple((arg1, arg2))


def _convert_it(numstr: str) -> int:
    """Convert a string to an int.

    Args:
        numstr: The string representation of a number

    Returns: The numstr converted to an int

    Raises:
        ValueError: Invalid literal
    """
    # LOCAL VARIABLES
    numint = 0  # Store conversion here

    # CONVERT IT
    numint = int(numstr)

    # DONE
    return numint


def _validate_parameters(args: list) -> None:
    """
    Purpose - Validated parameters on behalf of parse_arguments()
    Param
        args - A list of arguments from the command line
    Exceptions
        TypeError if a bad data type is detected
        ValueError if a bad value is detected
        RuntimeError on usage error
    Returns
        None
    """
    # INPUT VALIDATION
    if not isinstance(args, list):
        raise TypeError(f'Invalid "args" data type of {type(args)}')
    if not args:
        raise ValueError('The "args" parameter may not be empty')
    if len(args) < 3:
        raise RuntimeError('Invalid usage: Not enough arguments')
    if len(args) > 3:
        raise RuntimeError('Invalid usage: Too many arguments')
    for arg in args:
        if not isinstance(arg, str):
            raise TypeError(f'Invalid data type of {type(arg)} found in '
                            '"args"')
        if not arg:
            raise ValueError('Empty parameter found in "args"')
