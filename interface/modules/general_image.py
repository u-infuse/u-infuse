"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: Functions to be used for image processing.
"""
import os
import numpy as np
import cv2

def ImageToBackground(returnImg, resizedImage, inputSizes):
    """
    Add resized image to background.
    """
    errorMsg = None

    try:
        # Add existing image to centre of background image
        yCo = (inputSizes[0] - resizedImage.shape[0]) // 2
        xCo = (inputSizes[1] - resizedImage.shape[1]) // 2
        returnImg[yCo:yCo+resizedImage.shape[0], xCo:xCo+resizedImage.shape[1]] = resizedImage
    except Exception as e:
        errorMsg = str(e)

    return returnImg, errorMsg

def MakeAverageColour(resizedImage):
    """
    Create background with average colour.
    """
    errorMsg = None
    imgColour = (255, 255, 255)

    try:
        imgColourRow = np.average(resizedImage, axis=0)
        imgColour = np.average(imgColourRow, axis=0)
    except Exception as e:
        errorMsg = str(e)

    return imgColour, errorMsg

def StripedColour(imgDir, imgName, inputSizes):
    """
    Creates striped background image.
    """
    imgColour = (255, 255, 255)
    errorMsg = None

    try:
        newImgLoc = os.path.join(imgDir, imgName)
        newImg = cv2.imread(newImgLoc, 1)
        newImg = cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB)
        colourImage = cv2.resize(newImg, (inputSizes[1], inputSizes[0]), interpolation=cv2.INTER_AREA)
        imgColours, colourCount = np.unique(colourImage, axis=0, return_counts=True)
        imgColour = imgColours[colourCount.argmax()]
    except Exception as e:
        errorMsg = str(e)

    return imgColour, errorMsg

def StripedColourTurned(imgDir, imgName, inputSizes):
    """
    Creates striped background image but rotated.
    """
    imgColour = (255, 255, 255)
    errorMsg = None

    try:
        newImgLoc = os.path.join(imgDir, imgName)
        newImg = cv2.imread(newImgLoc, 1)
        newImg = cv2.cvtColor(newImg, cv2.COLOR_BGR2RGB)
        newImg = cv2.rotate(newImg, cv2.ROTATE_90_CLOCKWISE)
        colourImage = cv2.resize(newImg, (inputSizes[1], inputSizes[0]), interpolation=cv2.INTER_AREA)
        imgColours, colourCount = np.unique(colourImage, axis=0, return_counts=True)
        imgColour = imgColours[colourCount.argmax()]
    except Exception as e:
        errorMsg = str(e)

    return imgColour, errorMsg

def MakeBackgroundImage(inputSizes, imgColour, rotateImg):
    """
    Creates background image with selected colour.
    """
    returnImg = None
    errorMsg = None

    try:
        # Create background image
        returnImg = np.full((inputSizes[0], inputSizes[1], inputSizes[4]), imgColour, dtype=np.uint8)

        # Rotate image if required
        if rotateImg:
            # Create background image
            returnImg = cv2.rotate(returnImg, cv2.ROTATE_90_COUNTERCLOCKWISE)
            returnImg = cv2.resize(returnImg, (inputSizes[1], inputSizes[0]), interpolation=cv2.INTER_AREA)

        # Decrease brightness of background
        returnImg = cv2.add(returnImg, np.array([25.0]))

    except Exception as e:
        errorMsg = str(e)

    return returnImg, errorMsg

def MakeBackground(inputSizes, imgName, imgDir, fullWidth, fullHeight, resizedImage, backgroundOption):
    """
    Creates background for image to be placed on.
    """
    errorMsg = None
    backgroundCreated = False
    rotateImg = False

    try:
        # Determine background colour
        imgColour = (255, 255, 255)

        # Create background image
        returnImg = np.full((inputSizes[0], inputSizes[1], inputSizes[4]), imgColour, dtype=np.uint8)

        # Background None option
        if "None" in backgroundOption:
            backgroundCreated = True

        # Change background for images with Striped option
        if "Striped" in backgroundOption:
            if fullWidth and (fullHeight is False):
                backgroundCreated = True

                # Get background colour
                imgColour, errorMsg = StripedColour(imgDir, imgName, inputSizes)
            else:
                if fullHeight and (fullWidth is False):
                    backgroundCreated = True
                    rotateImg = True

                    # Get background colour
                    imgColour, errorMsg = StripedColourTurned(imgDir, imgName, inputSizes)

        # Create average colour background
        if backgroundCreated is False:
            imgColour, errorMsg = MakeAverageColour(resizedImage)

        if errorMsg is None:
            returnImg, errorMsg = MakeBackgroundImage(inputSizes, imgColour, rotateImg)

    except Exception as e:
        if errorMsg is None:
            errorMsg = str(e)
        else:
            errorMsg += "\n" + str(e)

    return returnImg, errorMsg

def ResizedImage(inputSizes, inputImg):
    """
    Takes in an image and resizes it.
    """
    errorMsg = None

    # For image background
    fullWidth = False
    fullHeight = False

    # Resize images if the dimensions support this
    try:
        # Images that are both smaller in height and width do not need to be resized
        if (inputSizes[2] < inputSizes[0]) and (inputSizes[3] < inputSizes[1]):
            resizedImage = inputImg
        else:
            scalingFactor = 1
            if inputSizes[2] > inputSizes[3]:
                scalingFactor = inputSizes[0] / inputSizes[2]
                fullHeight = True
            else:
                if inputSizes[3] > inputSizes[2]:
                    scalingFactor = inputSizes[1] / inputSizes[3]
                    fullWidth = True

            reducedHeight = round(inputSizes[2] * scalingFactor)
            reducedWidth = round(inputSizes[3] * scalingFactor)

            # Correction for dimensions not scaled
            if reducedHeight > inputSizes[0]:
                reducedHeight = inputSizes[0]
                fullHeight = True
            if reducedWidth > inputSizes[1]:
                reducedWidth = inputSizes[1]
                fullWidth = True

            # Resize image
            resizedImage = cv2.resize(inputImg, (reducedWidth, reducedHeight), interpolation=cv2.INTER_AREA)
    except Exception as e:
        errorMsg = "Could not resize image. Reason: " + str(e)

    return resizedImage, fullWidth, fullHeight, errorMsg

def ResizeImage(inputImg, inputSizes, imgName, imgDir, backgroundOption):
    """
    Takes in an image and resizes the image to the required coordinates by
    adding a border to keep the aspect ratio.
    """
    resizedImage = None
    returnImg = inputImg
    errorMsg = None

    # Resize image
    resizedImage, fullWidth, fullHeight, errorMsg = ResizedImage(inputSizes, inputImg)

    # Make background
    if errorMsg is None:
        returnImg, errorMsg = MakeBackground(inputSizes, imgName, imgDir, fullWidth, fullHeight, resizedImage, backgroundOption)

    # Add resized image to background image
    if errorMsg is None:
        returnImg, errorMsg = ImageToBackground(returnImg, resizedImage, inputSizes)

    return returnImg, errorMsg

def ProcessImages(imageDir):
    """
    Counts images in a directory and returns list of fils in a directory that
    are images.
    """
    counter = 0
    imgFormats = ["jpg", "jpeg", "png", "tif", "tiff"]
    imgList = []
    errorMsg = None

    # Count images and genrate image list
    try:
        for imgFormat in imgFormats:
            for img in os.listdir(imageDir):
                if img.lower().endswith(imgFormat):
                    counter += 1
                    imgList.append(img)
    except Exception as e:
        errorMsg = str(e)

    return counter, imgList, errorMsg

def EnoughImages(imageDir, imgMin):
    """
    Counts images in a directory.
    Return True if greater than or equal to imgMin and False if not enough
    images in directory.
    Returns image count in the directory.
    """
    enoughImages = False
    counter, imgList, errorMsg = ProcessImages(imageDir)

    # Check counter is greater than or equal to imgMin
    try:
        if counter >= imgMin:
            enoughImages = True
    except Exception as e:
        errorMsg = "Could not compare values: " + str(e)

    return enoughImages, counter, errorMsg
