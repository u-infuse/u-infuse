"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: Unit testing for general_image.py.
"""
import general_image

# Test data variables
testImageDir = "test/test_images"
testImgMin = 2

print("Testing general_image.py\n")

# Test general_image.ProcessImages
counter, imgList, errorMsg = general_image.ProcessImages(testImageDir, testImgMin)
assert counter > 0
assert len(imgList) > 0
assert errorMsg is None
print("general_image.ProcessImages passed")

# Test general_image.EnoughImages
enoughImages, counter, errorMsg = general_image.EnoughImages(testImageDir, testImgMin)
assert enoughImages
assert counter > 0
assert errorMsg is None
print("general_image.EnoughImages passed")

print("\nTesting general_image.py complete")
