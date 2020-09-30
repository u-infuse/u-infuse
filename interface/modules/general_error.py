"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: Functions to be used for error catching and processing.
"""
import os

def FileExists(filePath):
    """
    Check if file exists.
    """
    fileExists = False
    errorMsg = None

    # Check if csv file exists
    try:
        if os.path.exists(filePath):
            fileExists = True
    except Exception as e:
        errorMsg = str(e)

    return fileExists, errorMsg

def OpenFile(filePath):
    """
    Opens file, if it exists.
    """
    openedFile = False
    errorMsg = None

    # Check if file exists
    fileExists, errorMsg = FileExists(filePath)

    # Open file
    if fileExists:
        try:
            os.startfile(filePath)
            openedFile = True
        except Exception as e:
            errorMsg = str(e)

    return openedFile, errorMsg

def GetMapPath(modelName, modelLoc):
    """
    Returns map name if it exists.
    """
    error = False
    mapFileFound = False
    mapPath = ""
    mapName = ""

    # Get map file name
    try:
        mapName = os.path.splitext(modelName)[0] + ".csv"
    except Exception:
        error = True

    # Create map file path
    if error is False:
        try:
            mapPath = os.path.join(modelLoc, mapName)
        except Exception:
            error = True

    # Check that map file exists
    if error is False:
        try:
            if os.path.exists(mapPath):
                mapFileFound = True
        except Exception:
            pass

    return mapPath, mapFileFound

def StringNotEmpty(stringIn):
    """
    Returns True if string is not empty, false if it is empty or None.
    """
    notEmpty = True

    try:
        if stringIn is None:
            notEmpty = False
        else:
            testString = stringIn.strip()
            if not testString:
                notEmpty = False
    except Exception:
        notEmpty = False

    return notEmpty

def CheckCSV():
    """
    Checks to ensure CSV files have been created.
    """
    error = False
    errorMsg = None
    csvExists = True
    csvFiles = ["validation.csv", "training.csv", "classes.csv"]

    # Check CSV files exist
    try:
        for file in csvFiles:
            if not os.path.exists(file):
                csvExists = False
            else:
                # Check if file is empty
                if os.stat(file) == 0:
                    csvExists = False
    except Exception as e:
        error = True
        errorMsg = str(e)

    return csvExists, error, errorMsg

def CheckTrainVars(pretrainedModel, datasets, classes):
    """
    Checks training variables for errors. Returns false if there are no errors.
    """
    error = False
    errorMsg = ""
    listList = []

    # Ensure pretrained model is set
    try:
        if pretrainedModel is None:
            error = True
    except Exception as e:
        error = True
        errorMsg += str(e)

    # Ensure datasets lists aren't empty
    try:
        listList = [datasets, classes]
        for listName in listList:
            if len(listName) == 0:
                error = True
    except Exception as e:
        error = True
        errorMsg += str(e)

    return error, errorMsg

def TrainErrorCheck(pretrainedModel, datasets, classes):
    """
    Checks if there are any errors with training files and settings.
    """
    errors = False
    errorMsg = ""

    csvExist, csvError, csvErrorMsg = CheckCSV()
    valError, valErrorMsg = CheckTrainVars(pretrainedModel, datasets, classes)

    # If CSV files don't exist or there was an error
    if (csvExist is False) or csvError:
        errors = True
        errorMsg = "CSV training files don't exist. "
        if csvErrorMsg is not None:
            errorMsg += csvErrorMsg

    # If variables are empty
    if valError:
        errors = True
        errorMsg += "\nThere was an error with training variables: Model training variables are empty. "
        errorMsg += valErrorMsg

    return errors, errorMsg
