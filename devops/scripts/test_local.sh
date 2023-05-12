#!/bin/bash

# This script automates the execution of the TEDIOUS START (TEST) example code and TEST test
# code: functional tests, unit tests.  The verbosity of these tests is controlled by the
# TEST_VERBOSITY_LEVEL environment variable.  This script controls the value of that environment
# variable with the UNITTEST_VERBOSITY variable.
# 
# This script uses the following exit codes:
#   0 on success
#   1 if any Python command exits with a non-zero value

# GLOBAL VARIABLES
# Supported Verbosity Values
# 0 (quiet): Prints the total numbers of tests executed and the global result.
# 1 (standard): Same output as quiet with single characters (dot or F) for test cases.
# 2 (verbose): Prints the help string of every test and the result.
UNITTEST_VERBOSITY=0                                                # Test case verbosity level
EXIT_CODE=0                                                         # Exit code used by this script
ORIGINAL_DIR=$(pwd)                                                 # Working dir of execution
SCRIPT_DIR="$( cd -- "$(dirname "$0")" >/dev/null 2>&1 ; pwd -P )"  # This scripts directory


# SETUP
export TEST_VERBOSITY_LEVEL=$UNITTEST_VERBOSITY


# TEST IT
# TEDIOUS START (TEST) Examples
$SCRIPT_DIR/test_local_examples.sh
if [ $? -eq 0 ]
then
    echo -e "[✓] TEDIOUS START (TEST) example test cases\n"
else
    echo -e "[X] TEDIOUS START (TEST) example test cases\n"
    EXIT_CODE=1
fi

echo "TEDIOUS START TEST CASES"
python3 -m test
if [ $? -eq 0 ]
then
    echo -e "[✓] TEDIOUS START test cases\n"
else
    echo -e "[X] TEDIOUS START test cases\n"
    EXIT_CODE=1
fi


# DONE
cd $ORIGINAL_DIR
unset TEST_VERBOSITY_LEVEL
echo ""
exit $EXIT_CODE
