#!/bin/bash

# This script automates the stand-alone testing of a TEDIOUS START (TEST) installation.  This
# script copies the test code and the "test local" shell script to the TEMP_DIR directory to
# avoid the pollution of local package pollution.  This script then executes the "test local"
# shell script there to verify the TEST installation.
# 
# This script uses the following exit codes:
#   0 on success
#   1 if any command fails

# GLOBAL VARIABLES
TEMP_DIR=/tmp/test_TEST    # Temporary directory to execute stand-alone TEST tests
EXIT_CODE=0                # Exit code used by this script
ORIGINAL_DIRECTORY=$(pwd)  # Starting directory for this script


# VERIFY
# Verify TEDIOUS START is installed
if [ $EXIT_CODE -eq 0 ]
then
	python -c "import test" 2> /dev/null
	if [ $? -eq 0 ]
	then
	    echo -e "[✓] Verified TEDIOUS START is installed"
	else
	    echo -e "[X] TEDIOUS START is not installed"
	    EXIT_CODE=1
	fi
fi


# SETUP
# Create temp dir
if [ $EXIT_CODE -eq 0 ]
then
	mkdir -p $TEMP_DIR
	if [ $? -eq 0 ]
	then
	    echo -e "[✓] Successfully created temp working directory: $TEMP_DIR"
	else
	    echo -e "[X] Failed to create $TEMP_DIR"
	    EXIT_CODE=1
	fi
fi
# Copy files
if [ $EXIT_CODE -eq 0 ]
then
	# Necessary shell script
	cp ./devops/scripts/test_local_examples.sh $TEMP_DIR
	if [ $? -ne 0 ]
	then
	    EXIT_CODE=1
	fi
	# Test code
	cp --recursive test/ $TEMP_DIR
	if [ $? -ne 0 ]
	then
	    EXIT_CODE=1
	fi
	# Bad code (to test)
	cp --recursive badcode/ $TEMP_DIR
	if [ $? -ne 0 ]
	then
	    EXIT_CODE=1
	fi
	# Check it
	if [ $EXIT_CODE -eq 0 ]
	then
	    echo -e "[✓] Successfully copied files"
	else
	    echo -e "[X] Failed to copy files"
	fi
fi
# Change directory
if [ $EXIT_CODE -eq 0 ]
then
	cd $TEMP_DIR
	if [ $? -eq 0 ]
	then
	    echo -e "[✓] Current directory: $TEMP_DIR"
	else
	    echo -e "[X] Failed to change directory to $TEMP_DIR"
	    EXIT_CODE=1
	fi
fi


# TEST IT
if [ $EXIT_CODE -eq 0 ]
then
	./test_local_examples.sh
	if [ $? -eq 0 ]
	then
	    echo -e "[✓] TEDIOUS START (TEST) installation passed testing"
	else
	    echo -e "[X] TEDIOUS START (TEST) installation failed testing"
	    EXIT_CODE=1
	fi
fi


# DONE
cd $ORIGINAL_DIRECTORY
echo ""
exit $EXIT_CODE
