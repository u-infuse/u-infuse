"""
Author:  Chris Lawson
Contact: clawso21@une.edu.au
Source:  U-Infuse
Purpose: Functions for the Preview Inference Dialogue.
"""
from PyQt5 import QtCore, QtWidgets
import ui_general
import interface_inference
import general
import general_error
import general_image
import config

def StartUpdateTimer(self):
    """
    Starts update combo box.
    """
    self.updateTimer = QtCore.QTimer()
    self.updateTimer.timeout.connect(lambda: UpdateCombo(self))
    self.updateTimer.start(1000)

def UpdateCombo(self):
    """
    Updates combo box when directory changes.
    """
    # Load snapshots
    dataSets, errorMsg = general.ModelNames(config.snapshots)
    if errorMsg is not None:
        errorMessage = "There was an error with preprocessing.get_all_files(). Reason: " + errorMsg
        self.previewInferenceDialogue.textEdit.append(errorMessage)

    if dataSets != self.updatePIDatasets:
        self.updatePIDatasets = dataSets

        # Insert snapshots
        error, errorMsg = ui_general.InsertModels(self, self.previewInferenceDialogue, dataSets)
        if error:
            errorMessage = "Could not add datasets to dialogue. Reason: " + errorMsg
            self.previewInferenceDialogue.textEdit.append(errorMessage)

def StartTogglePiWidgets(self):
    """
    Timer set to toggle widgets.
    """
    # Set inference in progress to True
    self.inferenceInProgress = True

    # Disable widgets
    DisablePiWidgets(self)

    # Set timer
    self.piTimer = QtCore.QTimer()
    self.piTimer.timeout.connect(lambda: TogglePiWidgets(self))
    self.piTimer.start(1000)

def EnablePiWidgets(self):
    """
    Enable widgets.
    """
    self.previewInferenceDialogue.selectTestImagesButton.setDisabled(False)
    self.previewInferenceDialogue.selectTestImagesButton.setStyleSheet("color: black;")
    self.previewInferenceDialogue.dataSetsComboBox.setDisabled(False)
    self.previewInferenceDialogue.dataSetsComboBox.setStyleSheet("color: black;")
    self.previewInferenceDialogue.previewImagesNumLabel1.setDisabled(False)
    self.previewInferenceDialogue.previewImagesNumLabel1.setStyleSheet("color: black;")
    self.previewInferenceDialogue.previewImagesNum.setDisabled(False)
    self.previewInferenceDialogue.previewImagesNum.setStyleSheet("color: black;")
    self.previewInferenceDialogue.confThreshLabel1.setDisabled(False)
    self.previewInferenceDialogue.confThreshLabel1.setStyleSheet("color: black;")
    self.previewInferenceDialogue.confidenceThresholdNum.setDisabled(False)
    self.previewInferenceDialogue.confidenceThresholdNum.setStyleSheet("color: black;")
    self.previewInferenceDialogue.previewPerformanceButton.setDisabled(False)
    self.previewInferenceDialogue.previewPerformanceButton.setStyleSheet("color: black;")
    self.previewInferenceDialogue.modelName.setDisabled(False)
    self.previewInferenceDialogue.modelName.setStyleSheet("color: black;")
    self.previewInferenceDialogue.deleteModelsCheckBox.setDisabled(False)
    self.previewInferenceDialogue.deleteModelsCheckBox.setStyleSheet("color: black;")
    self.previewInferenceDialogue.exportModelButton.setDisabled(False)
    self.previewInferenceDialogue.exportModelButton.setStyleSheet("color: black;")

def DisablePiWidgets(self):
    """
    Disable widgets.
    """
    self.previewInferenceDialogue.selectTestImagesButton.setDisabled(True)
    self.previewInferenceDialogue.selectTestImagesButton.setStyleSheet("color: gray;")
    self.previewInferenceDialogue.dataSetsComboBox.setDisabled(True)
    self.previewInferenceDialogue.dataSetsComboBox.setStyleSheet("color: gray;")
    self.previewInferenceDialogue.previewImagesNumLabel1.setDisabled(True)
    self.previewInferenceDialogue.previewImagesNumLabel1.setStyleSheet("color: gray;")
    self.previewInferenceDialogue.previewImagesNum.setDisabled(True)
    self.previewInferenceDialogue.previewImagesNum.setStyleSheet("color: gray;")
    self.previewInferenceDialogue.confThreshLabel1.setDisabled(True)
    self.previewInferenceDialogue.confThreshLabel1.setStyleSheet("color: gray;")
    self.previewInferenceDialogue.confidenceThresholdNum.setDisabled(True)
    self.previewInferenceDialogue.confidenceThresholdNum.setStyleSheet("color: gray;")
    self.previewInferenceDialogue.previewPerformanceButton.setDisabled(True)
    self.previewInferenceDialogue.previewPerformanceButton.setStyleSheet("color: gray;")
    self.previewInferenceDialogue.modelName.setDisabled(True)
    self.previewInferenceDialogue.modelName.setStyleSheet("color: gray;")
    self.previewInferenceDialogue.deleteModelsCheckBox.setDisabled(True)
    self.previewInferenceDialogue.deleteModelsCheckBox.setStyleSheet("color: gray;")
    self.previewInferenceDialogue.exportModelButton.setDisabled(True)
    self.previewInferenceDialogue.exportModelButton.setStyleSheet("color: gray;")

def StopTogglePiWidgets(self):
    """
    Cancel toggle timer.
    """
    # Stop timer
    try:
        self.piTimer.stop()
    except Exception:
        pass

    # Enable widgets
    EnablePiWidgets(self)

def TogglePiWidgets(self):
    """
    Toggles widgets.
    """
    if self.inferenceInProgress is False:
        StopTogglePiWidgets(self)

def PreviewPerformanceButton(self):
    """
    Get preview images list when the previewPerformanceButton is pushed.
    """
    # Set self.cancelPreview value
    self.cancelPreview = False

    # Update show images variable
    self.showImages = True

    # Update generate report variable
    self.generateReport = False

    # Reset progress bar
    self.previewInferenceDialogue.progressBar.setValue(0)

    # Set first preview image variable for messaging
    self.firstPreviewImage = True

    # Set snapshot name
    ui_general.SetModel(self, self.previewInferenceDialogue)

    # Ensure name is not empty
    modelNotEmpty = general_error.StringNotEmpty(self.selectedModel)

    # Ensure test images dir has been selected
    imagesDirNotEmpty = general_error.StringNotEmpty(self.testImagesPath)

    # Ensure image count is less than image dir image count.
    enoughImages, imageCount, errorMessage = general_image.EnoughImages(self.testImagesPath, self.previewImagesNum)
    if errorMessage is not None:
        self.previewInferenceDialogue.textEdit.append(errorMessage)

    if enoughImages is False:
        self.previewImagesNum = imageCount

        # Update preview images number
        ui_general.SetPreviewImagesNum(self, self.previewInferenceDialogue)

    # Set progress bar max value
    self.inferenceProgressBarMaxValue = self.previewImagesNum

    # Set progress bar
    ui_general.SetProgressBar(self, self.previewInferenceDialogue)

    # Set model directory
    self.modelDir = config.snapshots

    # Set map path
    mapPath, mapFileFound = general_error.GetMapPath(config.classesCSV, "")
    if mapFileFound:
        self.mapPath = mapPath

    # Create thread to process images
    if modelNotEmpty and imagesDirNotEmpty and mapFileFound:
        ui_general.StartPreviewThread(self, self.previewInferenceDialogue)

        # Disable widgets while processing images
        StartTogglePiWidgets(self)

        # Update dialogue
        self.previewInferenceDialogue.textEdit.append("Commencing inference.")
    else:
        if modelNotEmpty is False:
            QtWidgets.QMessageBox.information(self.previewInferenceDialogue, "No model found", "Please select a model first.", QtWidgets.QMessageBox.Ok)
        if imagesDirNotEmpty is False:
            QtWidgets.QMessageBox.information(self.previewInferenceDialogue, "No image directory selected", "Please select test images directory first.", QtWidgets.QMessageBox.Ok)
        if mapFileFound is False:
            QtWidgets.QMessageBox.information(self.previewInferenceDialogue, "No map file found", "The model you have selected does not have a map file containing classes. Please select a different model.", QtWidgets.QMessageBox.Ok)

def CloseDialogue(self):
    """
    Close dialogue window.
    """
    self.previewInferenceDialogue.close()

def ExportModelButton(self):
    """
    Exports model when export model button is clicked.
    """
    # Set snapshot name
    ui_general.SetModel(self, self.previewInferenceDialogue)

    # Ensure CSV files are already created.
    csvExist, errorMsg = general_error.FileExists(config.classesCSV)

    if errorMsg is not None:
        errorMessage = "Model export stopped because there was a problem with the classes.csv file. Reason: " + errorMsg
        self.previewInferenceDialogue.textEdit.append(errorMessage)

    # Ensure snapshot exists
    notEmpty = general_error.StringNotEmpty(self.selectedModel)

    if csvExist and notEmpty:
        # Export model
        error, errorMsg = interface_inference.ExportModel(self.selectedModel, self.newModelName, self.deleteModels)

        # Read error message if one occurred
        if error:
            errorMessage = "There was an error with inference.export_model(). Reason: " + errorMsg
            self.previewInferenceDialogue.textEdit.append(errorMessage)
        else:
            updateMessage = "Model " + self.newModelName + " has been exported."
            self.previewInferenceDialogue.textEdit.append(updateMessage)
    else:
        if csvExist is False:
            QtWidgets.QMessageBox.information(self.previewInferenceDialogue, "Class names file not found", "A model without class names cannot be exported.", QtWidgets.QMessageBox.Ok)
        if notEmpty is False:
            QtWidgets.QMessageBox.information(self.previewInferenceDialogue, "No snapshots found", "Model training needs to be completed before exporting a model.", QtWidgets.QMessageBox.Ok)

def UpdateModelName(self, nameIn):
    """
    Updates model name variable when changed.
    """
    try:
        name = nameIn
        if isinstance(nameIn, str):
            self.newModelName = name
    except Exception as e:
        errorMessage = "Could not update model name in the preview inference dialogue. Reason: " + str(e)
        self.textEdit.append(errorMessage)

def SetModelName(self):
    """
    Sets model name in dialogue.
    """
    try:
        if isinstance(self.newModelName, str):
            self.previewInferenceDialogue.modelName.setText(self.newModelName)
    except Exception as e:
        errorMessage = "Could not update model name in the preview inference dialogue. Reason: " + str(e)
        self.textEdit.append(errorMessage)

def DeleteModels(self):
    """
    Change value when state is changed.
    """
    if self.previewInferenceDialogue.deleteModelsCheckBox.isChecked() is False:
        self.deleteModels = False
    else:
        self.deleteModels = True

def PreviewInferenceDialogue(self):
    """
    Load preview inference dialogue.
    """
    if self.trainInProgress:
        QtWidgets.QMessageBox.information(self.previewInferenceDialogue, "Cannot Preview Model", "Training is already in progress.", QtWidgets.QMessageBox.Ok)
    else:
        # Set generate XML variable
        self.generateXML = False

        # Load preview images number
        ui_general.SetPreviewImagesNum(self, self.previewInferenceDialogue)

        # Load snapshots
        dataSets, errorMsg = general.ModelNames(config.snapshots)
        if errorMsg is not None:
            errorMessage = "There was an error with preprocessing.get_all_files(). Reason: " + errorMsg
            self.previewInferenceDialogue.textEdit.append(errorMessage)

        # Insert snapshots
        error, errorMsg = ui_general.InsertModels(self.previewInferenceDialogue, dataSets)
        if error:
            errorMessage = "Could not add datasets to dialogue. Reason: " + errorMsg
            self.previewInferenceDialogue.textEdit.append(errorMessage)

        # Save datasets
        self.updatePIDatasets = dataSets

        # Set confidence threshold
        ui_general.SetConfThresh(self, self.previewInferenceDialogue)

        # Update model name
        SetModelName(self)

        # Update delete models checkbox
        self.previewInferenceDialogue.deleteModelsCheckBox.setChecked(self.deleteModels)

        # Make dialogue cursor invisible
        self.previewInferenceDialogue.textEdit.setCursorWidth(0)

        # Enable widgets in dialogue
        EnablePiWidgets(self)

        # Start update combo timer
        StartUpdateTimer(self)

        # Set default button
        ui_general.DefaultButton(self.previewInferenceDialogue)

        # Show dialogue
        self.previewInferenceDialogue.show()

        # Cancel all if dialogue is rejected (x button is clicked)
        if self.previewInferenceDialogue.exec_() == QtWidgets.QDialog.Rejected:
            # Cancel threads
            ui_general.CancelButton(self, self.previewInferenceDialogue)

            # Cancel toggle timer
            StopTogglePiWidgets(self)
