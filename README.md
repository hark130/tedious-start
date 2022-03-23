# tedious-start
TEDIOUS START (TEST): A package of common-use test functionality based on Python3's unittest module.


## TEST TEDIOUS START

- clone
- pip3 install lib/hobo-1.0.0-py3-none-any.whl
- Execute the example test code:
	- `python3 -m test.example_test_start`
	- `python3 -m test.unit_tests.example_test_unittest`
	- `python3 -m test.functional_tests.example_test_functest`

## RELEASE TEDIOUS START

- Verify CHANGELOG.md updated
- Update setup.py with new version
- Code review dev branch
	- `pycodestyle --max-line-length=100 ./`
	- `find . -type f -name "*.py" | xargs pylint --score=no`
	- Execute the example test code (see: TEST TEDIOUS START)
- Merge dev into main
- `python3 setup.py bdist_wheel --dist-dir='dist'`
- Manually test wheel
	- Install new wheel
	- Execute basic test code using TEST
		- `cp test/example_test_start.py /tmp`
		- `python3 /tmp/example_test_start.py`
- Source control new wheel
- Tag main

## INSTALL TEDIOUS START

- If applicable, release a new version (see: RELEASE TEDIOUS START)
- `pip3 install dist/test-X.Y.Z-py3-none-any.whl`
- Profit
