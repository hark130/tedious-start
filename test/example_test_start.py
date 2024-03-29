"""Template general unit test module.

Use this module as an example/template to write unit tests for general features.
If you decide to separate your test class and Test Cases into separate modules within this
package, ensure the Test Case module filename begins with `test_`.  The class's module
may be named IAW PEP8 naming standards.

    Usage:
    1. Copy this file and rename it to `test_SOMETHING.py`
    2. Rename all 'SOMETHING' placeholders accordingly
    3. Source-control discretely named file-based test input (if applicable)
    4. Define numbered Test Cases within the NEBS classes whose name begins with `test_<NEBS>`
    5. `python3 -m test.test_SOMETHING` to run your test cases

    Troubleshooting:
    Q1. Why didn't my test cases run when I executed `python3 -m unittest`?
    A1a. Ensure your test case module's filename start with `test_`?
    A1b. Is there at least one method name that starts with `test_`?
    Q2. Why didn't my test cases execute with `python3 -m test.test_SOMETHING`?
    A2. Consider the following:
        - Did you replace the command's 'test_SOMETHING' with the actual name of your module?
        - Did you remove or comment out `execute_test_cases()` or the code block that executes
            `execute_test_cases()`?
        - Did you remove, comment, or modify `execute_test_cases()`'s behavior?
        - Is there at least one Test Case whose name starts with `test_`?
        - Try `python3 -m unittest -k SOMETHING` but replace SOMETHING with a substring related
            to your test cases and/or module
"""
# Standard Imports
# Third Party Imports
# Local Imports
from test.loader import exec_verbose_test_cases
from tediousstart.tediousstart import TediousStart


class TestSOMETHING(TediousStart):
    """SOMETHING test class.

    This class provides base functionality to run NEBS test cases for SOMETHING.
    """

    def __init__(self, *args, **kwargs) -> None:
        """TestSOMETHING ctor.

        Class constructor.
        """
        super().__init__(*args, **kwargs)
        self._placeholder = True  # TD: DDN... Remove


class NormalTestSOMETHING(TestSOMETHING):
    """Normal Test Cases.

    Organize the Normal Test Cases
    """

    def test_normal_01(self):
        """Normal input that's expected to pass."""
        self.assertTrue(self._placeholder)  # TD: DDN

    def test_normal_02(self):
        """More different normal input."""
        self.assertTrue(self._placeholder is not False)  # TD: DDN


class ErrorTestSOMETHING(TestSOMETHING):
    """Error Test Cases.

    Organize the Error Test Cases
    """

    def test_error_01(self):
        """Error input that's expected to fail and/or raise an exception."""
        self.assertFalse(2+2 == 5)  # TD: DDN


class BoundaryTestSOMETHING(TestSOMETHING):
    """Boundary Test Cases.

    Organize the Boundary Test Cases
    """

    def test_boundary_01(self):
        """Boundary input that that tests the lower and upper limits of both good and bad input."""
        self.assertNotAlmostEqual(1, 100)  # TD: DDN


class SpecialTestSOMETHING(TestSOMETHING):
    """Special Test Cases.

    Organize the Special Test Cases
    """

    def test_special_01(self):
        """Special input that that tests an edge case."""
        self.assertIsNot(True, False)  # TD: DDN


if __name__ == '__main__':
    exec_verbose_test_cases()
