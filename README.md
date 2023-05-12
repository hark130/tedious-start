# tedious-start

TEDIOUS START (TEST): A package of common-use test functionality based on Python3's unittest module.

## TEST TEDIOUS START

- clone
- `pip3 install lib/hobo-1.2.0-py3-none-any.whl`
- Execute all test code: `./devops/scripts/test_local.sh`

## RELEASE TEDIOUS START

### 1. On `dev` branch

- Verify CHANGELOG.md updated
    - Update "[Unreleased]" with new version and release date
    - Add a new "[Unreleased]" section above it
    - Update the "[Unreleased]" link at the bottom
    - Add a new version link at the bottom
- Update setup.py with new version
- Code review dev branch
	- `pycodestyle --max-line-length=100 ./`
	- `find . -type f -name "*.py" | xargs pylint --score=no --disable=duplicate-code`
	- `find ./tediousstart/ -type f -name "*.py" | xargs pylint --score=no`
	- Execute the TEST test code (see: TEST TEDIOUS START)
- Merge dev into main

### 2. On `main` branch

- `python3 setup.py bdist_wheel --dist-dir='dist'`
- Manually test wheel
	- Install new wheel (see: INSTALL TEDIOUS START)
	- Execute basic stand-alone test code using TEST: `./devops/scripts/test_installation.sh`
- Source control new wheel
- Tag main

## INSTALL TEDIOUS START

- If applicable, release a new version (see: RELEASE TEDIOUS START)
- `pip3 install lib/hobo-1.2.0-py3-none-any.whl`
- `pip3 install dist/test-X.Y.Z-py3-none-any.whl`
- Profit
