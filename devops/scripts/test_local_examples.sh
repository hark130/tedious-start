#!/bin/bash

# This script automates the execution of the TEDIOUS START (TEST) example code.
# The verbosity of these tests is controlled by the TEST_VERBOSITY_LEVEL environment variable.
# This script controls the value of that environment variable with the UNITTEST_VERBOSITY variable.
# 
# This script uses the following exit codes:
#   0 on success
#   1 if any Python command exits with a non-zero value

# GLOBAL VARIABLES
# Supported Verbosity Values
# 0 (quiet): Prints the total numbers of tests executed and the global result.
# 1 (standard): Same output as quiet with single characters (dot or F) for test cases.
# 2 (verbose): Prints the help string of every test and the result.
UNITTEST_VERBOSITY=0       # Verbosity level for the test cases to execute with
EXIT_CODE=0                # Exit code used by this script
ORIGINAL_DIRECTORY=$(pwd)  # Starting directory for this script


# SETUP
export TEST_VERBOSITY_LEVEL=$UNITTEST_VERBOSITY


# TEST IT
echo "TEDIOUS START EXAMPLE USAGE"
# TediousStart Examples
python3 -m test.example_test_start
if [ $? -eq 0 ]
then
    echo -e "[✓] Example TediousStart test cases\n"
else
    echo -e "[X] Example TediousStart test cases\n"
    EXIT_CODE=1
fi

# TediousUnitTest Examples
python3 -m test.unit_tests.example_test_unittest
if [ $? -eq 0 ]
then
    echo -e "[✓] Example TediousUnitTest test cases\n"
else
    echo -e "[X] Example TediousUnitTest test cases\n"
    EXIT_CODE=1
fi

# TediousFuncTest Examples
python3 -m test.functional_tests.example_test_functest
if [ $? -eq 0 ]
then
    echo -e "[✓] Example TediousFuncTest test cases\n"
else
    echo -e "[X] Example TediousFuncTest test cases\n"
    EXIT_CODE=1
fi


# DONE
cd $ORIGINAL_DIRECTORY
unset TEST_VERBOSITY_LEVEL
echo ""
exit $EXIT_CODE
