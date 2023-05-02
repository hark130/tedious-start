# Changelog

All notable changes to Tedious Start (TEST) will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

### Changed

### Deprecated

### Fixed

- `TediousFuncTest._print_verbose_output()` type hint (improper formatting caused "type not subscriptable" error)

### Removed

### Security

## [1.2.0] - 2023-03-24

### Added

- `TediousStart.fail_test_case()`
- `TediousFuncTest.verify_stdout_missing()`
- `TediousFuncTest.verify_stderr_missing()`
- New module `tediousstart.vebosity` defines the `Verbosity` `Enum` class
- New module `tediousstart.redirect_std_streams` defines the `RedirectStdStreams` class
- `TediousStart._delete_files()`

### Changed

- `TediousFuncTest` was refactored to add a "verbose" feature
- `TediousFuncTest.run_test()` was refactored with a new optional verbosity argument

### Fixed

- Updated `TediousFuncTest.set_command_list()` docstring

## [1.1.0] - 2022-04-18

### Added

- `TediousFuncTest._execute_cmd()`
- `TediousFuncTest._validate_default_results()`

### Changed

- Refactored `TediousFuncTest._run_test()` into more modular methods
- `TediousFuncTest` stores raw output into attributes
- Updated `TediousFuncTest._validate_expected_output()` docstring and function definition

## [1.0.1] - 2022-04-04

### Changed

- Changed Python version requirement to Python3.7 or higher

## [1.0.0] - 2022-03-25

### Added

- Initial commit of existing functionality: tediousfunctest, tediousstart, tediousunittest.
- README.md initial commit
- CHANGELOG.md initial commit

[Unreleased](https://github.com/hark130/tedious-start/compare/v1.2.0...dev)

[1.2.0](https://github.com/hark130/tedious-start/tree/v1.2.0)

[1.1.0](https://github.com/hark130/tedious-start/tree/v1.1.0)

[1.0.1](https://github.com/hark130/tedious-start/tree/v1.0.1)

[1.0.0](https://github.com/hark130/tedious-start/tree/v1.0.0)
