"""Do Bad Code maths."""


def divide_it(numerator: int, denominator: int) -> float:
    """Find the quotient."""
    if not isinstance(numerator, int):
        raise TypeError('numerator must be an int')
    if not isinstance(denominator, int):
        raise TypeError('denominator must be an int')
    if denominator == 0:
        raise ValueError('You may not divide by zero')
    return numerator / denominator
