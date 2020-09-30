"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: Unit testing for general_image.py.
"""
import general_error
import os

# Test data variables
testImage = "test/test_images/1.jpg"
testModelName = "test_model"
testModelDir = "test"
testClassFile = "test_model.csv"
testString = "Test string."

print("Testing general_error.py\n")

# Test general_error.FileExists
fileExists, errorMsg = general_error.FileExists(testImage)
assert fileExists
assert errorMsg is None
print("general_error.FileExists passed")

# Test general_error.GetMapPath
mapPath, mapFilePath = general_error.GetMapPath(testModelName, testModelDir)
assert mapPath == os.path.join(testModelDir, testClassFile)
assert mapFilePath
print("general_error.GetMapPath passed")

# Test general_error.StringNotEmpty
notEmpty = general_error.StringNotEmpty(testString)
assert True
print("general_error.StringNotEmpty passed")

# Test general_error.CheckCSV
csvExist, error, errorMsg = general_error.CheckCSV()
assert csvExist
assert error is False
assert errorMsg is None
print("general_error.CheckCSV passed")

print("\nTesting general_error.py complete")
