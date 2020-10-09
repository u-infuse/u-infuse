"""
Author:  Chris Lawson
Contact: clawso21@une.edu.au
Source:  U-Infuse
Purpose: Functions for the Auto-Annotate Dialogue.
"""
import os
from PyQt5 import QtWidgets, QtCore
import config
import ui_general
import general
import general_image
import general_error

def StartToggleAaWidgets(self):
    """
    Timer set to toggle widgets.
    """
    # Set inference in progress to True
    self.inferenceInProgress = True

    # Disable widgets
    DisableAaWidgets(self)

    # Set timer
    self.aaTimer = QtCore.QTimer()
    self.aaTimer.timeout.connect(lambda: ToggleAaWidgets(self))
    self.aaTimer.start(1000)

def EnableAaWidgets(self):
    """
    Enable widgets.
    """
    self.autoAnnotateDialogue.dataSetsComboBox.setDisabled(False)
    self.autoAnnotateDialogue.dataSetsComboBox.setStyleSheet("color: black;")
    self.autoAnnotateDialogue.multiClassCheckBox.setDisabled(False)
    self.autoAnnotateDialogue.multiClassCheckBox.setStyleSheet("color: black;")
    self.autoAnnotateDialogue.singleClassName.setDisabled(False)
    self.autoAnnotateDialogue.singleClassName.setStyleSheet("color: black;")
    self.autoAnnotateDialogue.annotatorComboBox.setDisabled(False)
    self.autoAnnotateDialogue.annotatorComboBox.setStyleSheet("color: black;")
    self.autoAnnotateDialogue.confThreshLabel1.setDisabled(False)
    self.autoAnnotateDialogue.confThreshLabel1.setStyleSheet("color: black;")
    self.autoAnnotateDialogue.confidenceThresholdNum.setDisabled(False)
    self.autoAnnotateDialogue.confidenceThresholdNum.setStyleSheet("color: black;")
    self.autoAnnotateDialogue.showImagesCheckBox.setDisabled(False)
    self.autoAnnotateDialogue.showImagesCheckBox.setStyleSheet("color: black;")
    self.autoAnnotateDialogue.runAnnotationButton.setDisabled(False)
    self.autoAnnotateDialogue.runAnnotationButton.setStyleSheet("color: black;")
    self.autoAnnotateDialogue.editAnnotationsButton.setDisabled(False)
    self.autoAnnotateDialogue.editAnnotationsButton.setStyleSheet("color: black;")

def DisableAaWidgets(self):
    """
    Disable widgets.
    """
    self.autoAnnotateDialogue.dataSetsComboBox.setDisabled(True)
    self.autoAnnotateDialogue.dataSetsComboBox.setStyleSheet("color: gray;")
    self.autoAnnotateDialogue.multiClassCheckBox.setDisabled(True)
    self.autoAnnotateDialogue.multiClassCheckBox.setStyleSheet("color: gray;")
    self.autoAnnotateDialogue.singleClassName.setDisabled(True)
    self.autoAnnotateDialogue.singleClassName.setStyleSheet("color: gray;")
    self.autoAnnotateDialogue.annotatorComboBox.setDisabled(True)
    self.autoAnnotateDialogue.annotatorComboBox.setStyleSheet("color: gray;")
    self.autoAnnotateDialogue.confThreshLabel1.setDisabled(True)
    self.autoAnnotateDialogue.confThreshLabel1.setStyleSheet("color: gray;")
    self.autoAnnotateDialogue.confidenceThresholdNum.setDisabled(True)
    self.autoAnnotateDialogue.confidenceThresholdNum.setStyleSheet("color: gray;")
    self.autoAnnotateDialogue.showImagesCheckBox.setDisabled(True)
    self.autoAnnotateDialogue.showImagesCheckBox.setStyleSheet("color: gray;")
    self.autoAnnotateDialogue.runAnnotationButton.setDisabled(True)
    self.autoAnnotateDialogue.runAnnotationButton.setStyleSheet("color: gray;")
    self.autoAnnotateDialogue.editAnnotationsButton.setDisabled(True)
    self.autoAnnotateDialogue.editAnnotationsButton.setStyleSheet("color: gray;")

def StopToggleAaWidgets(self):
    """
    Cancel toggle timer.
    """
    # Stop timer
    try:
        self.aaTimer.stop()
    except Exception:
        pass

    # Enable widgets
    EnableAaWidgets(self)

def ToggleAaWidgets(self):
    """
    Toggles widgets.
    """
    if self.inferenceInProgress is False:
        StopToggleAaWidgets(self)

def OpenLabelImg(self):
    """
    Opens labelimg.
    """
    # Define current datasets directory to annotate
    dataSet = self.autoAnnotateDialogue.dataSetsComboBox.currentText()
    imgDir = os.path.join(config.datasets, dataSet)
    modelName = ""
    modelDir = ""
    errorMsg = None

    # Set variables
    try:
        if self.multiClassCheckBox:
            modelName = self.autoAnnotateDialogue.annotatorComboBox.currentText()
            modelDir = config.snapshots
        else:
            modelName = config.classesCSV
            modelDir = ""

    except Exception as e:
        print("Could not get classes path. Reason: " + str(e)) #DEBUG

    # Set classes file path
    mapPath, mapFileFound = general_error.GetMapPath(modelName, modelDir)

    if mapFileFound:
        errorMsg = general.OpenLabelImg(imgDir, mapPath)

    if errorMsg is not None:
        errorMessage = "Could not open labelImg. Reason: " + errorMsg
        self.autoAnnotateDialogue.textEdit.append(errorMessage)

def RunAnnotationButton(self):
    """
    Runs when the RunAnnotationButton is clicked.
    """
    # Set generate XML variable
    self.generateXML = True

    # If the multiclass option is set
    if self.multiClassCheckBox:
        # Set model directory
        self.modelDir = config.snapshots

        # Get currently selected model name
        self.selectedModel = self.autoAnnotateDialogue.annotatorComboBox.currentText()

        # Set map path
        mapPath, mapFileFound = general_error.GetMapPath(config.classesCSV, "")
        if mapFileFound:
            self.mapPath = mapPath

        # Set model directory
        self.modelDir = config.snapshots
    else:
        # Set model directory
        self.modelDir = config.pretrainedModels

        # Set single class annotator model as default model
        self.selectedModel = "single_class_annotator.h5"

        # Set map path
        mapPath, mapFileFound = general_error.GetMapPath(self.selectedModel, self.modelDir)
        if mapFileFound:
            self.mapPath = mapPath

        # Create classes CSV file
        error, errorMsg = general.CreateClassString(self.selectedModel, config.pretrainedModels, self.annotateClassesSet)
        if error:
            errorMessage = "There was an error with creating CSV file: " + errorMsg
            self.autoAnnotateDialogue.textEdit.append(errorMessage)

    # Set self.cancelPreview value
    self.cancelPreview = False

    # Set first preview image variable for messaging
    self.firstPreviewImage = True

    # Chosen dataset
    dataSet = self.autoAnnotateDialogue.dataSetsComboBox.currentText()
    self.testImagesPath = os.path.join(config.datasets, dataSet)

    # Set image count
    enoughImages, imageCount, errorMessage = general_image.EnoughImages(self.testImagesPath, 0)
    if errorMessage is not None:
        self.autoAnnotateDialogue.textEdit.append(errorMessage)

    self.previewImagesNum = imageCount

    # Set progress bar max value
    self.inferenceProgressBarMaxValue = self.previewImagesNum

    # Reset progress bar
    self.autoAnnotateDialogue.progressBar.setValue(0)

    # Set progress bar
    ui_general.SetProgressBar(self, self.autoAnnotateDialogue)

    # Start preview images thread
    ui_general.StartPreviewThread(self, self.autoAnnotateDialogue)

    # Disable widgets while processing images
    StartToggleAaWidgets(self)

def InsertAnnotateModels(dialogue, dataSets):
    """
    Inserts models into the datasets combobox.
    """
    error = False
    errorMsg = ""
    try:
        if dialogue is not None:
            # Clear old items
            dialogue.annotatorComboBox.clear()

            # Add new items
            if isinstance(dataSets, (list, dict, tuple, set)):
                for name in dataSets:
                    dialogue.annotatorComboBox.addItem(name)
            else:
                if isinstance(dataSets, str):
                    dialogue.annotatorComboBox.addItem(name)
    except Exception as e:
        error = True
        errorMsg = str(e)

    return error, errorMsg

def ToggleSingleClassName(self):
    """
    Disable/enable the single class name QLineEdit.
    """
    if self.multiClassCheckBox:
        self.autoAnnotateDialogue.singleClassName.setReadOnly(True)
        self.autoAnnotateDialogue.singleClassName.setStyleSheet("color: gray;")
    else:
        self.autoAnnotateDialogue.annotatorComboBox.addItem("single_class_annotator.h5")
        self.autoAnnotateDialogue.singleClassName.setReadOnly(False)
        self.autoAnnotateDialogue.singleClassName.setStyleSheet("color: black;")

def UpdateClassNameVariable(self, newName):
    """
    Updates the single class name variable when it is changed.
    """
    try:
        # Set single class name
        self.singleClassName = newName

        # Update classes set
        self.annotateClassesSet = {newName}

    except Exception as e:
        print("There was an error setting class name: " + str(e)) #DEBUG

def UpdateClassName(self):
    """
    Displays the chosen report name in the reportTitle QLineEdit.
    """
    self.autoAnnotateDialogue.singleClassName.setText(self.singleClassName)

def MultiClassCheckBox(self):
    """
    Changes value if the checkbox is checked/unchecked.
    """
    if self.autoAnnotateDialogue.multiClassCheckBox.isChecked() is False:
        self.multiClassCheckBox = False

        # Remove pretrained models
        dataSets = []
        error, errorMsg = InsertAnnotateModels(self.autoAnnotateDialogue, dataSets)
        if error:
            errorMessage = "Could not add datasets to dialogue. Reason: " + errorMsg
            self.autoAnnotateDialogue.textEdit.append(errorMessage)
    else:
        # Update multi class checkbox value
        self.multiClassCheckBox = True

        # Reset classes set
        self.annotateClassesSet = {}

        # Load pretrained models
        dataSets, errorMsg = general.ModelNames(config.snapshots)
        if errorMsg is not None:
            errorMessage = "There was an error with preprocessing.get_all_files(). Reason: " + errorMsg
            self.autoAnnotateDialogue.textEdit.append(errorMessage)

        # Insert pretrained models
        error, errorMsg = InsertAnnotateModels(self.autoAnnotateDialogue, dataSets)
        if error:
            errorMessage = "Could not add datasets to dialogue. Reason: " + errorMsg
            self.autoAnnotateDialogue.textEdit.append(errorMessage)

        # Save datasets
        self.updateAAAnnotateDatasets = dataSets

    # Disable/enable single class name
    ToggleSingleClassName(self)

def StartUpdateTimer(self):
    """
    Starts update combo box.
    """
    self.updateTimer = QtCore.QTimer()
    self.updateTimer.timeout.connect(lambda: UpdateCombos(self))
    self.updateTimer.start(1000)

def UpdateCombos(self):
    """
    Updates combo boxes when directory changes.
    """
    # Load datasets
    modelList, errorMsg = general.ReturnDirNames(config.datasets)
    if errorMsg is not None:
        errorMessage = "Could not add pretrained models. Reason: " + errorMsg
        self.autoAnnotateDialogue.textEdit.append(errorMessage)

    if modelList != self.updateAADatasets:
        self.updateAADatasets = modelList

        # Insert pretrained models
        error, errorMsg = ui_general.InsertModels(self, self.autoAnnotateDialogue, modelList)
        if error:
            errorMessage = "Could not add datasets to dialogue. Reason: " + errorMsg
            self.autoAnnotationDialogue.textEdit.append(errorMessage)

    if self.multiClassCheckBox:
        # Load pretrained models
        dataSets, errorMsg = general.ModelNames(config.snapshots)
        if errorMsg is not None:
            errorMessage = "There was an error with preprocessing.get_all_files(). Reason: " + errorMsg
            self.autoAnnotateDialogue.textEdit.append(errorMessage)

        if dataSets != self.updateAAAnnotateDatasets:
            self.updateAAAnnotateDatasets = dataSets

            # Insert pretrained models
            error, errorMsg = InsertAnnotateModels(self.autoAnnotateDialogue, dataSets)
            if error:
                errorMessage = "Could not add datasets to dialogue. Reason: " + errorMsg
                self.autoAnnotateDialogue.textEdit.append(errorMessage)

def AutoAnnotateDialogue(self):
    """
    Load auto-annotate dialogue.
    """
    if self.trainInProgress:
        QtWidgets.QMessageBox.information(self.autoAnnotateDialogue, "Cannot Open Auto-Annotator", "Training is already in progress.", QtWidgets.QMessageBox.Ok)
    else:
        # Load datasets
        #dataSets, error, errorMsg = interface_preprocessing.ReturnDatasets(config.datasets)
        modelList, errorMsg = general.ReturnDirNames(config.datasets)
        if errorMsg is not None:
            errorMessage = "Could not add models. Reason: " + errorMsg
            self.autoAnnotateDialogue.textEdit.append(errorMessage)

        # Insert pretrained models
        error, errorMsg = ui_general.InsertModels(self.autoAnnotateDialogue, modelList)
        if error:
            errorMessage = "Could not add datasets to dialogue. Reason: " + errorMsg
            self.textEdit.append(errorMessage)

        # Add single class name
        self.autoAnnotateDialogue.annotatorComboBox.addItem("single_class_annotator.h5")

        # Save datasets
        self.updateAADatasets = modelList

        # Update showImagesCheckBox
        self.autoAnnotateDialogue.showImagesCheckBox.setChecked(self.showImages)

        # Set confidence threshold
        ui_general.SetConfThresh(self, self.autoAnnotateDialogue)

        # Update delete models checkbox
        self.autoAnnotateDialogue.multiClassCheckBox.setChecked(self.multiClassCheckBox)

        # Update single class name
        UpdateClassName(self)

        # Start update combo timer
        StartUpdateTimer(self)

        # Make dialogue cursor invisible
        self.autoAnnotateDialogue.textEdit.setCursorWidth(0)

        # Set default button
        ui_general.DefaultButton(self.autoAnnotateDialogue)

        # Show dialogue
        self.autoAnnotateDialogue.show()

        # Cancel all if dialogue is rejected (x button is clicked)
        if self.autoAnnotateDialogue.exec_() == QtWidgets.QDialog.Rejected:
            # Cancel threads
            ui_general.CancelButton(self, self.autoAnnotateDialogue)

            # Cancel toggle timer
            StopToggleAaWidgets(self)
