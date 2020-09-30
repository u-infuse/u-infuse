"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: Module interfaces with inference.py.
"""
from inference import export_model, inference_per_image, choose_inference_model, get_preview_images

def PreviewPerformance(imgDir, modelName, imgName, classesCSV, confThresh):
    """
    Previews performance one image at a time.
    """
    img = None
    objData = None
    errorMsg = None

    try:
        img, objData = inference_per_image(imgDir, modelName, imgName, classesCSV, confThresh)
    except Exception as e:
        errorMsg = "There was an error with inference.inference_per_image(): " + str(e)

    return img, objData, errorMsg

def ConvertModel(snapshotsDir, modelName):
    """
    Converts a model.
    """
    convertedModel = None

    try:
        convertedModel = choose_inference_model(snapshotsDir, modelName)
    except Exception as e:
        print("There was an error with inference.choose_inference_model(): " + str(e))

    return convertedModel

def GetPreviewImageNames(imgDir, imgTotal):
    """
    Returns list of randomly selected image file names to use from a directory.
    """
    imageList = []

    # Get image name list
    try:
        imageList = get_preview_images(imgDir, imgTotal)
    except Exception as e:
        print("There was an error with inference.get_preview_images(): " + str(e))

    return imageList

def ExportModel(oldName, newName, deleteModels):
    """
    Saves export model.
    """
    error = False
    errorMsg = ""

    try:
        export_model(oldName, newName, deleteModels)
    except Exception as e:
        error = True
        errorMsg = str(e)

    return error, errorMsg
