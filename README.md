# tedious-start
TEDIOUS START (TEST): A package of common-use test functionality based on Python3's unittest module.


## TEST TEDIOUS START

- clone
- pip3 install lib/hobo-1.0.1-py3-none-any.whl
- Execute the example test code:
	- `python3 -m test.example_test_start`
	- `python3 -m test.unit_tests.example_test_unittest`
	- `python3 -m test.functional_tests.example_test_functest`
- Execute the TEST test code: `python3 -m unittest`

## RELEASE TEDIOUS START

- Verify CHANGELOG.md updated
- Update setup.py with new version
- Code review dev branch
	- `pycodestyle --max-line-length=100 ./`
	- `find . -type f -name "*.py" | xargs pylint --score=no`
	- Execute the TEST test code (see: TEST TEDIOUS START)
- Merge dev into main
- `python3 setup.py bdist_wheel --dist-dir='dist'`
- Manually test wheel
	- Install new wheel (see: INSTALL TEDIOUS START)
	- Execute basic stand-alone test code using TEST
	    1. `TediousStart`
		    - `cp test/example_test_start.py /tmp`
		    - `python3 /tmp/example_test_start.py`
		2. `TediousUnitTest`
			- `cp test/unit_tests/example_test_unittest.py /tmp`
			- `cp --recursive badcode/ /tmp`
		3. `TediousFuncTest`
		    - `cp test/functional_tests/example_test_functest.py /tmp`
		    - `cp --recursive badcode/ /tmp`
		    - `python3 /tmp/example_test_functest.py`
- Source control new wheel
- Tag main

## INSTALL TEDIOUS START

- If applicable, release a new version (see: RELEASE TEDIOUS START)
- `pip3 install dist/test-X.Y.Z-py3-none-any.whl`
- Profit

NOTE: HOBO is a dependency for TEST.  You can install HOBO with: `pip3 install lib/hollow-boomer/hobo-1.0.0-py3-none-any.whl`.
