"""Setup script to distribute Tedious Start (TEST).

This script was written to help facilitate an easy way to release TEST as a wheel.
Project-specific macros are defined at the top of the file.  'TEST_VERSION' should be updated
for each new release.  'TEST_REQUIRES' will need to be updated if TEST ever imports additional
third-party libraries.

    Typical usage example:

    python3 setup.py bdist_wheel --dist-dir='dist'
"""

# Standard Imports
import setuptools
# Third Party Imports
# Local Imports
from hobo.disk_operations import destroy_dir, find_path_to_dir, read_file
from hobo.misc import print_exception

TEST_NAME = 'test'
TEST_VERSION = '1.0.0'
TEST_AUTHOR = 'Dev Crew Team Happy Aku'
TEST_EMAIL = 'nunya@biz.ns'  # https://iiwiki.us/wiki/.ns
TEST_DESCRIPTION = 'Common functionality used for unit and functional testing.'
TEST_URL = 'https://github.com/hark130/tedious-start'
TEST_PYTHON = '>=3.8'  # See: setuptools.setup(python_requires)
TEST_REQUIRES = ['hobo>=1.0']  # See: setuptools.setup(install_requires)


def main() -> None:
    """Builds the TEST package.

    Gathers and prepares information to include in the package.  Then builds the package.

    Args:
        None

    Raises:
        OSError: The repo directory or the input files (e.g., README.md, CHANGELOG.md) were not
        found.  Also if any of them weren't what they were expected to be
        (e.g., README.md is a directory).
    """
    try:
        # LOCAL VARIABLES
        repo_dir = _find_repo_dir('tedious-start')       # Abs path to the top-level repo directory
        long_description = _build_description(repo_dir)  # README.md + CHANGELOG.md

        # SETUP
        setuptools.setup(
            name=TEST_NAME,
            version=TEST_VERSION,
            author=TEST_AUTHOR,
            author_email=TEST_EMAIL,
            maintainer=TEST_AUTHOR,
            maintainer_email=TEST_EMAIL,
            description=TEST_DESCRIPTION,
            long_description=long_description,
            long_description_content_type='text/markdown',
            url=TEST_URL,
            # Hard-coded the package name in case we define supporting packages (e.g., testing)
            packages=['tediousstart'],
            classifiers=[
                # Taken from: https://pypi.org/pypi?%3Aaction=list_classifiers
                'Programming Language :: Python :: 3',
                'Intended Audience :: Developers',
                'Natural Language :: English',
                'Operating System :: OS Independent',
                'Topic :: Software Development :: Testing',
            ],
            python_requires=TEST_PYTHON,
            install_requires=TEST_REQUIRES,
        )

        # CLEAN UP
        destroy_dir(f'{TEST_NAME}.egg-info')
        destroy_dir('build')

    # pylint: disable=broad-except
    except Exception as err:
        print_exception(err)
    # pylint: enable=broad-except


#############################
# INTERNAL HELPER FUNCTIONS #
#############################


def _build_description(repo_dir: str) -> str:
    """Builds the TEST description.

    Builds a long description for TEST by concatenating the README.md and CHANGELOG.md.  Input
    validation handled by internal helper functions.

    Args:
        repo_dir: The absolute path to the TEST directory.

    Returns:
        A string containing the concatenated contents of README.md and CHANGELOG.md.

    Raises:
        FileNotFoundError: repo_dir, README.md, or CHANGELOG.md is not found.
        OSError: README.md or CHANGELOG.md is not a file or repo_dir is not a directory.
        TypeError: Invalid data type.
        ValueError: Empty repo_dir string.
    """
    # LOCAL VARIABLES
    long_description = ''  # Long description for TEST

    # BUILD IT
    long_description = _get_readme(repo_dir) + '\n\n' + _get_changelog(repo_dir)

    # DONE
    return long_description


def _find_repo_dir(repo_dir_name: str) -> str:
    """Finds the TEST directory.

    Finds the root-level TEST directory starting at the current working directory.  It calls
    hobo.disk_operations.find_path_to_dir() under the hood.

    Args:
        repo_dir_name: The name of the top-level TEST repo directory.

    Returns:
        A string containing the absolute path to hollow-boomer.

    Raises:
        OSError: hollow-boomer isn't found.
    """
    return find_path_to_dir(dir_to_find=repo_dir_name)


def _get_changelog(repo_dir: str) -> str:
    """Reads the TEST CHANGELOG.

    Reads the TEST CHANGELOG.md and returns it as a string.  Input validation handled by
    hobo.read_file().

    Args:
        repo_dir: The absolute path to the TEST directory.

    Returns:
        A string containing the contents of CHANGELOG.md.

    Raises:
        FileNotFoundError: repo_dir or CHANGELOG.md is not found.
        OSError: repo_dir is not a directory or CHANGELOG.md is not a file.
        TypeError: Invalid data type.
        ValueError: Empty string.
    """
    return read_file(repo_dir, 'CHANGELOG.md')  # Contents of the CHANGELOG.md


def _get_readme(repo_dir: str) -> str:
    """Reads the TEST README.

    Reads the TEST README.md and returns it as a string.  Input validation handled by
    hobo.read_file().

    Args:
        repo_dir: The absolute path to the TEST directory.

    Returns:
        A string containing the contents of README.md.

    Raises:
        FileNotFoundError: repo_dir or README.md is not found.
        OSError: repo_dir is not a directory or README.md is not a file.
        TypeError: Invalid data type.
        ValueError: Empty string.
    """
    return read_file(repo_dir, 'README.md')  # Contents of the README.md


if __name__ == '__main__':
    main()
