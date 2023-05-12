#!/bin/bash

# DESCRIPTION:
# This script automates the execution of the TEDIOUS START (TEST) example code and TEST test
# code: functional tests, unit tests.  The verbosity of these tests is controlled by the
# TEST_VERBOSITY_LEVEL environment variable.  This script controls the value of that environment
# variable with the UNITTEST_VERBOSITY variable.
#
# USAGE EXAMPLES:
# 1. Default verbosity
#   $ ./devops/scripts/test_local.sh
# 2. Override default verbosity
#   $ export TEST_VERBOSITY_LEVEL=2
#   $ ./devops/scripts/test_local.sh
#   $ unset TEST_VERBOSITY_LEVEL
#
# EXIT CODES:
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
UNSET_VAR=0                                                         # 0 false, 1 true


# SETUP
if [[ -z "${TEST_VERBOSITY_LEVEL}" ]]
then
    export TEST_VERBOSITY_LEVEL=$UNITTEST_VERBOSITY
    UNSET_VAR=1
fi


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
if [ $UNSET_VAR -ne 0 ]
then
    # This script exported it so this script unsets it
    unset TEST_VERBOSITY_LEVEL
fi
echo ""
exit $EXIT_CODE
