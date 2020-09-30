"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: Unit testing for general.py.
"""
import general

# Test data variables
testModelFile = "test_model.h5"
testModelDir = "test"
testClassFile = "test_model.csv"
testChosenClasses = ['test']

print("Testing general.py\n")

# Test general.GetCSVName
error, errorMsg, csvName = general.GetCSVName(testModelFile)
assert error is False
assert errorMsg == ""
assert csvName == testClassFile
print("general.GetCSVName passed")

# Test general.CreateClassString
error, errorMsg = general.CreateClassString(testModelFile, testModelDir, testChosenClasses)
assert error is False
assert errorMsg == ""
print("general.CreateClassString passed")

print("\nTesting general.py complete")
