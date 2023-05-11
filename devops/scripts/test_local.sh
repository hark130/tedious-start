#!/bin/bash

# 
# This script uses the following exit codes:
#   0 on success
#   1 if any Python command exits with a non-zero value

# GLOBAL VARIABLES
UNITTEST_VERBOSITY=0       # Verbosity level for the test cases to execute with
# Supported Verbosity Values
# 0 (quiet): Prints the total numbers of tests executed and the global result.
# 1 (standard): Same output as quiet with single characters (dot or F) for test cases.
# 2 (verbose): Prints the help string of every test and the result.
EXIT_CODE=0                # Exit code used by this script
ORIGINAL_DIRECTORY=$(pwd)  # Starting directory for this script

# SETUP
export TEST_VERBOSITY_LEVEL=$UNITTEST_VERBOSITY

echo "TEST EXAMPLE USAGE"
# TediousStart Examples
python3 -m test.example_test_start
if [ $? -eq 0 ]
then
    echo "[✓] Example TediousStart test cases"
else
    echo "[X] Example TediousStart test cases"
    EXIT_CODE=1
fi

# TediousUnitTest Examples
python3 -m test.unit_tests.example_test_unittest
if [ $? -eq 0 ]
then
    echo "[✓] Example TediousUnitTest test cases"
else
    echo "[X] Example TediousUnitTest test cases"
    EXIT_CODE=1
fi

# TediousFuncTest Examples
python3 -m test.functional_tests.example_test_functest
if [ $? -eq 0 ]
then
    echo "[✓] Example TediousFuncTest test cases"
else
    echo "[X] Example TediousFuncTest test cases"
    EXIT_CODE=1
fi


echo "TEDIOUS START TEST CASES"
python3 -m unittest
if [ $? -eq 0 ]
then
    echo "[✓] TEDIOUS START (TEST) test cases"
else
    echo "[X] TEDIOUS START (TEST) test cases"
    EXIT_CODE=1
fi


# DONE
cd $ORIGINAL_DIRECTORY
unset TEST_VERBOSITY_LEVEL
echo ""
exit $EXIT_CODE
