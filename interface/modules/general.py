"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: General functions to be used with the UI and interface.
"""
import os
import json
from json2html import *
import config

def ConvertJSONNew(filePath):
    """
    Loads, converts a JSON file to HTML, and opens the file.
    """
    data = ""
    htmlTable = ""
    errorMsg = None
    reportFile = "report.html"

    # HTML start
    # White
    htmlStart = "<html><head><style>table {font-family: Ariel, sans-serif; text-align: center; border-spacing: 20px; border: 3px solid; border-color: gray;}</style></head><body>"

    # Grey
    #htmlStart = "<html><head><style>table {text-align: left; border-spacing: 20px; border: 3px solid; border-color: gray; background-color: #d3d3d3;}</style></head><body>"

    # Original
    #htmlStart = "<html><body><head><style>table {padding-left: 0px; padding-right: 0px; border: 5px transparent solid; border-collapse: separate; border-spacing: 20px; padding: 1px;}</style></head>"


    # HTML end
    htmlEnd = "</body></html>"

    # Load JSON file
    try:
        with open(filePath) as jsonFile:
            data = json.load(jsonFile)
    except Exception as e:
        errorMsg = str(e)

    # Get values from JSON data
    reportTitle = "Not set"
    modelName = "Not set"
    confThresh = "Not set"
    totalImages = "Not set"
    positiveImages = "Not set"
    emptyImages = "Not set"
    try:

        # Report Title Data
        reportData = data["report_title"]

        for item in reportData:
            reportTitle = item.pop("report_title")

        # About Object Detector Data
        aboutData = data["About Object Detector"]

        for item in aboutData:
            modelName = item.pop("Model")
            confThresh = item.pop("Confidence Threshold")

        # Object Detection Data
        detectionData = data["Object Detection Information"]

        for item in detectionData:
            totalImages = item.pop("Total Images")
            positiveImages = item.pop("Positive Images")
            emptyImages = item.pop("Empty Images")
    except Exception as e:
        print("Could not get JSON data. Reason: " + str(e)) # DEBUG

    # Construct summary report string
    reportString = "Unable to create summary report."
    try:
        reportString = "\n\nSummary Report\n\nReport Title: " + reportTitle + "\n\nAbout Object Detector"
        reportString += "\nModel Name: " + modelName + "\nConfidence Threshold: " + confThresh + "\n\nObject Detection Information"
        reportString += "\nTotal Images: " + str(totalImages) + "\nPositive Images: " + positiveImages + "\nEmpty Images: " + emptyImages
        print(reportString) # DEBUG
    except Exception as e:
        print("Could not create summary report. Reason: " + str(e)) # DEBUG

    # Create HTML table

    # Construct HTMl file
    html = htmlStart + htmlTable + htmlEnd

    # Save temp HTML file
    if errorMsg is None:
        try:
            htmlSave = open(reportFile, "w")
            htmlSave.write(html)
            htmlSave.close()
        except Exception as e:
            errorMsg = str(e)

    return reportFile, reportString, errorMsg

def ConvertJSON(filePath):
    """
    Loads, converts a JSON file to HTML, and opens the file.
    """
    data = ""
    htmlTable = ""
    errorMsg = None
    reportFile = "report.html"

    # HTML start
    # New
    htmlStart = "<html><head><style>table {min-width: 500px; box-shadow: 0 0 20px rgba(0, 0, 0, 0.15); margin: 25px 0; font-family: Ariel, sans-serif; text-align: left; border-spacing: 20px; border-bottom: 1px solid; border-color: black;}</style></head><body>"
    # White
    #htmlStart = "<html><head><style>table {font-family: Ariel, sans-serif; text-align: center; border-spacing: 20px; border: 3px solid; border-color: gray;}</style></head><body>"

    #htmlStart = "<html><head><style>table {text-align: left; border-spacing: 20px; border: 3px solid; border-color: gray; background-color: #d3d3d3;}</style></head><body>"

    # Original
    #htmlStart = "<html><body><head><style>table {padding-left: 0px; padding-right: 0px; border: 5px transparent solid; border-collapse: separate; border-spacing: 20px; padding: 1px;}</style></head>"


    # HTML end
    htmlEnd = "</body></html>"

    # Load JSON file
    try:
        with open(filePath) as jsonFile:
            data = json.load(jsonFile)
    except Exception as e:
        errorMsg = str(e)

    # Convert JSON data to HTML
    if errorMsg is None:
        try:
            #htmlTable = json2html.convert(json=data)
            htmlTable = json2html.convert(json=data, table_attributes="id=\"summary-report\"")
        except Exception as e:
            errorMsg = str(e)

    # Construct HTMl file
    html = htmlStart + htmlTable + htmlEnd

    # Save temp HTML file
    if errorMsg is None:
        try:
            htmlSave = open(reportFile, "w")
            htmlSave.write(html)
            htmlSave.close()
        except Exception as e:
            errorMsg = str(e)

    return reportFile, errorMsg

def ValidConfInt(intIn):
    """
    Ensure that the integer value is between 0 - 100.
    """
    validInt = False

    try:
        if (intIn >= 0) and (intIn <= 100):
            validInt = True
    except Exception:
        validInt = False

    return validInt

def IsAnInt(thresh):
    """
    Checks if confidence threshold is a valid number.
    """
    errorMsg = None
    intVal = 0

    try:
        if thresh != "": # Treat a blank value as 0
            intVal = int(thresh)
    except Exception as e:
        errorMsg = str(e)

    return errorMsg, intVal

def ConvertConfThresh(confThreshIn):
    """
    Converts confidence threshold.
    """
    errorMsg = None
    confThresh = 0

    try:
        confThresh = confThreshIn / 100
    except Exception as e:
        errorMsg = str(e)

    return confThresh, errorMsg

def ModelNames(modelDir):
    """
    Returns model names from a directory.
    """
    # Variables
    modelList = []
    errorMsg = None

    # Supported model types
    modelTypes = ["h5"]

    # Append supported file types
    try:
        for root, dirs, files in os.walk(modelDir):
            for fileName in files:
                for modelType in modelTypes:
                    if fileName.endswith(modelType):
                        modelList.append(fileName)
    except Exception as e:
        errorMsg = str(e)

    return modelList, errorMsg

def LoadTrainSettings():
    """
    Load training settings.
    """
    # Variables
    dataString = ""
    errorMsg = None
    fileExists = False
    epochs = 0
    batch = 0
    negative = True
    datasets = []
    negativeDatasets = []
    classes = []
    pretrainedModel = ""
    backgroundOption = ""
    previewScroll = True

    # Check if file exists
    try:
        if os.path.exists(config.settingsPath):
            fileExists = True
    except Exception as e:
        errorMsg = str(e)

    # Load data string
    if errorMsg is None:
        if fileExists:
            try:
                settingsOpen = open(config.settingsPath, "r")
                dataString = settingsOpen.read()
                settingsOpen.close()
                dataString = dataString.split("\n")
            except Exception as e:
                errorMsg = str(e)

    # Set varaibles
    if errorMsg is None:
        if fileExists:
            try:
                for setData in dataString:
                    # Set epochs
                    if "Epochs: " in setData:
                        epochs = setData.replace("Epochs: ", "")
                        epochs = epochs.replace(" ", "")
                        epochs = int(epochs)

                    # Set batch size
                    if "Batch-Size: " in setData:
                        batch = setData.replace("Batch-Size: ", "")
                        batch = batch.replace(" ", "")
                        batch = int(batch)

                    # Set negative images
                    if "Negative-Images: " in setData:
                        tempNegative = setData.replace("Negative-Images: ", "")
                        tempNegative = tempNegative.lower()

                        if "false" in tempNegative:
                            negative = False
                        else:
                            negative = True

                    # Set pretrained model
                    if "Pretrained Model: " in setData:
                        pretrainedModel = setData.replace("Pretrained Model: ", "")
                        pretrainedModel = pretrainedModel.strip()

                    # Set datasets
                    if "Datasets: " in setData:
                        tempDatasets = setData.replace("Datasets: ", "")
                        tempDatasets = tempDatasets.strip()
                        tempDatasets = tempDatasets.split(",")

                        for dataset in tempDatasets:
                            datasets.append(dataset)

                    # Set negative datasets
                    if "Negative Datasets: " in setData:
                        tempDatasets = setData.replace("Negative Datasets: ", "")
                        tempDatasets = tempDatasets.strip()
                        tempDatasets = tempDatasets.split(",")

                        for negativeDataset in tempDatasets:
                            negativeDatasets.append(negativeDataset)

                    # Set classes
                    if "Classes: " in setData:
                        tempClasses = setData.replace("Classes: ", "")
                        tempClasses = tempClasses.strip()
                        tempClasses = tempClasses.split(",")

                        for className in tempClasses:
                            classes.append(className)

                    # Set background option
                    if "Background: " in setData:
                        tempBackground = setData.replace("Background: ", "")
                        backgroundOption = tempBackground.strip()

                    # Set preview scroll option
                    if "Preview-Scroll: " in setData:
                        tempPreviewScroll = setData.replace("Preview-Scroll: ", "")
                        tempPreviewScroll = tempPreviewScroll.lower()

                        if "false" in tempPreviewScroll:
                            previewScroll = False
                        else:
                            previewScroll = True

            except Exception as e:
                errorMsg = str(e)

    return epochs, batch, negative, pretrainedModel, datasets, negativeDatasets, classes, fileExists, backgroundOption, previewScroll, errorMsg

def SaveTrainSettings(epochs, batch, negative, pretrainedModel, datasets, negativeDatasets, classes, backgroundOption, previewScroll):
    """
    Save training settings.
    """
    # Variables
    errorMsg = None
    saveList = ["U-Infuse Settings File"]
    saveString = ""
    saveEpochs = "Epochs: "
    saveBatch = "Batch-Size: "
    saveNegative = "Negative-Images: "
    savePretrainedModel = "Pretrained Model: "
    saveDatasets = "Datasets: "
    saveNegativeDatasets = "Negative Datasets: "
    saveClasses = "Classes: "
    saveBackgroundOption = "Background: "
    savePreviewScroll = "Preview-Scroll: "

    # Add variables to save
    try:
        saveEpochs += str(epochs)
        saveList.append(saveEpochs)
        saveBatch += str(batch)
        saveList.append(saveBatch)
        saveNegative += str(negative)
        saveList.append(saveNegative)
        savePretrainedModel += pretrainedModel
        saveList.append(savePretrainedModel)
        saveBackgroundOption += (backgroundOption)
        savePreviewScroll += str(previewScroll)

        firstDataset = True
        for dataset in datasets:
            if firstDataset:
                firstDataset = False
                saveDatasets += dataset
            else:
                saveDatasets += "," + dataset

        saveList.append(saveDatasets)

        firstNegativeDataset = True
        for negativeDataset in negativeDatasets:
            if firstNegativeDataset:
                firstNegativeDataset = False
                saveNegativeDatasets += negativeDataset
            else:
                saveNegativeDatasets += "," + negativeDataset

        saveList.append(saveNegativeDatasets)

        firstClass = True
        for className in classes:
            if firstClass:
                firstClass = False
                saveClasses += className
            else:
                saveClasses += "," + className

        saveList.append(saveClasses)
        saveList.append(saveBackgroundOption)
        saveList.append(savePreviewScroll)

    except Exception as e:
        errorMsg = str(e)

    # Combine list to create string
    if errorMsg is None:
        try:
            for entry in saveList:
                saveString += entry + "\n"
        except Exception as e:
            errorMsg = str(e)

    # Save settings file
    if errorMsg is None:
        try:
            settingsSave = open(config.settingsPath, "w")
            settingsSave.write(saveString)
            settingsSave.close()
        except Exception as e:
            errorMsg = str(e)

    return errorMsg

def OpenLabelImg(imageDir, classFile):
    """
    Opens labelImg if it is installed.
    """
    error = False
    errorMsg = ""
    try:
        os.system("start labelimg " + imageDir + " " + classFile)
    except Exception as e:
        error = True
        errorMsg = str(e)

    return error, errorMsg

def GetCSVName(modelName):
    """
    Takes in a model name and returns CSV name for model.
    """
    error = False
    errorMsg = ""
    csvName = ""

    # Get CSV file name
    try:
        csvName = os.path.splitext(modelName)[0] + ".csv"
    except Exception as e:
        error = True
        errorMsg = str(e)

    return error, errorMsg, csvName

def CreateClassString(chosenModel, modelDir, chosenClasses):
    """
    Creates string for class file.
    """
    error = False
    errorMsg = ""
    firstName = True
    csvFileName = ""
    nameString = ""

    # Get CSV file name
    try:
        error, errorMsg, csvFileName = GetCSVName(chosenModel)
    except Exception as e:
        error = True
        errorMsg += " " + str(e)

    # Create string with names
    if error is False:
        try:
            for name in chosenClasses:
                # Remove spaces
                name = name.strip()
                name = name.replace(" ", "_")
                if firstName:
                    firstName = False
                    nameString = name
                else:
                    nameString += "\n" + name
        except Exception as e:
            error = True
            errorMsg = str(e)

    # Write file
    if error is False:
        try:
            savePath = os.path.join(modelDir, csvFileName)
            csvSave = open(savePath, "w")
            csvSave.write(nameString)
        except Exception as e:
            error = True
            errorMsg = str(e)

    return error, errorMsg

def SetProgressBar(epochs, steps):
    """
    Sets progress bar values.
    """
    maxVal = 0
    count = 0
    errorMsg = None

    try:
        maxVal = epochs * steps
    except Exception as e:
        errorMsg = str(e)
    return maxVal, count, errorMsg

def ReturnDirNames(dirIn):
    """
    Returns list of subdirectories.
    """
    fileList = []
    errorMsg = None

    try:
        for root, dirs, files in os.walk(dirIn):
            for foundDir in dirs:
                fileList.append(foundDir)
    except Exception as e:
        errorMsg = str(e)

    return fileList, errorMsg
