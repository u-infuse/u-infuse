"""
Author:  Chris Lawson
Contact: clawso21@une.edu.au
Source:  U-Infuse
Purpose: Functions for the Run Inference Dialogue (AKA Object Detection Dialogue).
"""
from pathlib import Path
from PyQt5 import QtWidgets, QtCore
import config
import ui_general
import general
import general_error
import general_image

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
    # Load models
    dataSets, errorMsg = general.ModelNames(config.pretrainedModels)
    if errorMsg is not None:
        errorMessage = "There was an error with preprocessing.get_all_files(). Reason: " + errorMsg
        self.previewInferenceDialogue.textEdit.append(errorMessage)

    if dataSets != self.updateRIDatasets:
        self.updateRIDatasets = dataSets

        # Insert models
        error, errorMsg = ui_general.InsertModels(self, self.runInferenceDialogue, dataSets)
        if error:
            errorMessage = "Could not add datasets to dialogue. Reason: " + errorMsg
            self.previewInferenceDialogue.textEdit.append(errorMessage)

def StartToggleRiWidgets(self):
    """
    Timer set to toggle widgets.
    """
    # Set inference in progress to True
    self.inferenceInProgress = True

    # Disable widgets
    DisableRiWidgets(self)

    # Set timer
    self.riTimer = QtCore.QTimer()
    self.riTimer.timeout.connect(lambda: ToggleRiWidgets(self))
    self.riTimer.start(1000)

def EnableRiWidgets(self):
    """
    Enable widgets.
    """
    self.runInferenceDialogue.dataSetsComboBox.setDisabled(False)
    self.runInferenceDialogue.dataSetsComboBox.setStyleSheet("color: black;")
    self.runInferenceDialogue.selectTestImagesButton.setDisabled(False)
    self.runInferenceDialogue.selectTestImagesButton.setStyleSheet("color: black;")
    self.runInferenceDialogue.previewImagesNumLabel1.setDisabled(False)
    self.runInferenceDialogue.previewImagesNumLabel1.setStyleSheet("color: black;")
    self.runInferenceDialogue.previewImagesNum.setDisabled(False)
    self.runInferenceDialogue.previewImagesNum.setStyleSheet("color: black;")
    self.runInferenceDialogue.confThreshLabel1.setDisabled(False)
    self.runInferenceDialogue.confThreshLabel1.setStyleSheet("color: black;")
    self.runInferenceDialogue.confidenceThresholdNum.setDisabled(False)
    self.runInferenceDialogue.confidenceThresholdNum.setStyleSheet("color: black;")
    self.runInferenceDialogue.showImagesCheckBox.setDisabled(False)
    self.runInferenceDialogue.showImagesCheckBox.setStyleSheet("color: black;")
    self.runInferenceDialogue.reportCheckBox.setDisabled(False)
    self.runInferenceDialogue.reportCheckBox.setStyleSheet("color: black;")
    self.runInferenceDialogue.reportTitle.setDisabled(False)
    self.runInferenceDialogue.reportTitle.setStyleSheet("color: black;")
    self.runInferenceDialogue.runInferenceButton.setDisabled(False)
    self.runInferenceDialogue.runInferenceButton.setStyleSheet("color: black;")
    self.runInferenceDialogue.openReportButton.setDisabled(False)
    self.runInferenceDialogue.openReportButton.setStyleSheet("color: black;")
    self.runInferenceDialogue.chooseDetectorLabel.setDisabled(False)
    self.runInferenceDialogue.chooseDetectorLabel.setStyleSheet("color: black;")

def DisableRiWidgets(self):
    """
    Disable widgets.
    """
    self.runInferenceDialogue.dataSetsComboBox.setDisabled(True)
    self.runInferenceDialogue.dataSetsComboBox.setStyleSheet("color: gray;")
    self.runInferenceDialogue.selectTestImagesButton.setDisabled(True)
    self.runInferenceDialogue.selectTestImagesButton.setStyleSheet("color: gray;")
    self.runInferenceDialogue.previewImagesNumLabel1.setDisabled(True)
    self.runInferenceDialogue.previewImagesNumLabel1.setStyleSheet("color: gray;")
    self.runInferenceDialogue.previewImagesNum.setDisabled(True)
    self.runInferenceDialogue.previewImagesNum.setStyleSheet("color: gray;")
    self.runInferenceDialogue.confThreshLabel1.setDisabled(True)
    self.runInferenceDialogue.confThreshLabel1.setStyleSheet("color: gray;")
    self.runInferenceDialogue.confidenceThresholdNum.setDisabled(True)
    self.runInferenceDialogue.confidenceThresholdNum.setStyleSheet("color: gray;")
    self.runInferenceDialogue.showImagesCheckBox.setDisabled(True)
    self.runInferenceDialogue.showImagesCheckBox.setStyleSheet("color: gray;")
    self.runInferenceDialogue.reportCheckBox.setDisabled(True)
    self.runInferenceDialogue.reportCheckBox.setStyleSheet("color: gray;")
    self.runInferenceDialogue.reportTitle.setDisabled(True)
    self.runInferenceDialogue.reportTitle.setStyleSheet("color: gray;")
    self.runInferenceDialogue.runInferenceButton.setDisabled(True)
    self.runInferenceDialogue.runInferenceButton.setStyleSheet("color: gray;")
    self.runInferenceDialogue.openReportButton.setDisabled(True)
    self.runInferenceDialogue.openReportButton.setStyleSheet("color: gray;")
    self.runInferenceDialogue.chooseDetectorLabel.setDisabled(True)
    self.runInferenceDialogue.chooseDetectorLabel.setStyleSheet("color: gray;")

def StopToggleRiWidgets(self):
    """
    Cancel toggle timer.
    """
    # Stop timer
    try:
        self.riTimer.stop()
    except Exception:
        pass

    # Enable widgets
    EnableRiWidgets(self)

def ToggleRiWidgets(self):
    """
    Toggles widgets.
    """
    if self.inferenceInProgress is False:
        StopToggleRiWidgets(self)

def GetRunImagesCount(self, selectDir):
    """
    Gets the preview images count.
    """
    # Set test images path
    if selectDir:
        ui_general.TestImagesPath(self, self.runInferenceDialogue)

    # Set image count
    enoughImages, imageCount, errorMessage = general_image.EnoughImages(self.testImagesPath, self.previewImagesNum)
    if errorMessage is not None:
        self.runInferenceDialogue.textEdit.append(errorMessage)

    # Set image count
    self.previewImagesNum = imageCount

    # Update preview images number
    ui_general.SetPreviewImagesNum(self, self.runInferenceDialogue)

def OpenReport(self):
    """
    Opens report, if it exists.
    """
    if self.generateReport:
        # Variables
        openedFile = False
        reportFile = self.reportTitle + "_summary_report.json"
        reportPath = Path(config.reports) / reportFile
        errorMsg = None

        #general.MakeSummaryTable(reportPath)
        # Convert report to HTML
        convertedReportFile, errorMsg = general.ConvertJSON(reportPath)
        #self.runInferenceDialogue.textEdit.append(reportString) #DEBUG

        if errorMsg is None:
            openedFile, errorMsg = general_error.OpenFile(convertedReportFile)

        # Print error messages if they exist.
        if errorMsg is None:
            reportErrors, reportErrorMsg = ui_general.GetReportErrors(self)

            if reportErrorMsg is not None:
                errorMessage = "There was an error reading report errors: " + reportErrorMsg
                self.runInferenceDialogue.textEdit.append(reportErrorMsg)
            else:
                for errorItem in reportErrors:
                    errorMessage = "There was an error with the report: " + errorItem
                    self.runInferenceDialogue.textEdit.append(errorMessage)

        if openedFile is False:
            # Display error message, if generated
            QtWidgets.QMessageBox.information(self.runInferenceDialogue, "Report Not Found", "Report file has not yet been generated.", QtWidgets.QMessageBox.Ok)

def ToggleReportTitle(self):
    """
    Disable/enable the report title QLineEdit.
    """
    if self.generateReport:
        self.runInferenceDialogue.reportTitle.setReadOnly(False)
        self.runInferenceDialogue.reportTitle.setStyleSheet("color: black;")
        self.runInferenceDialogue.openReportButton.setDisabled(False)
        self.runInferenceDialogue.openReportButton.setStyleSheet("color: black;")
    else:
        self.runInferenceDialogue.reportTitle.setReadOnly(True)
        self.runInferenceDialogue.reportTitle.setStyleSheet("color: gray;")
        self.runInferenceDialogue.openReportButton.setDisabled(True)
        self.runInferenceDialogue.openReportButton.setStyleSheet("color: gray;")

def ReportCheckBox(self):
    """
    Changes value if the checkbox is checked/unchecked.
    """
    if self.runInferenceDialogue.reportCheckBox.isChecked() is False:
        self.generateReport = False
        self.generateReportRi = self.generateReport
    else:
        self.generateReport = True
        self.generateReportRi = self.generateReport

    # Disable/enable report title
    ToggleReportTitle(self)

def UpdateReportVariable(self, newTitle):
    """
    Updates the report variable when it is changed.
    """
    try:
        self.reportTitle = newTitle
    except Exception as e:
        errorMessage = "There was an error setting the report title: " + str(e)
        self.runInferencDialogue.textEdit.append(errorMessage)

def UpdateReportTitle(self):
    """
    Displays the chosen report name in the reportTitle QLineEdit.
    """
    self.runInferenceDialogue.reportTitle.setText(self.reportTitle)

def RunInferenceButton(self):
    """
    Run inference on selected model.
    """
    # Set self.cancelPreview value
    self.cancelPreview = False

    # Set first preview image variable for messaging
    self.firstPreviewImage = True

    # Set model name
    ui_general.SetModel(self, self.runInferenceDialogue)

    # Ensure name is not empty
    modelNotEmpty = general_error.StringNotEmpty(self.selectedModel)

    # Ensure test images dir has been selected
    imagesDirNotEmpty = general_error.StringNotEmpty(self.testImagesPath)

    # Ensure image count is less than image dir image count.
    enoughImages, imageCount, errorMessage = general_image.EnoughImages(self.testImagesPath, self.previewImagesNum)
    if errorMessage is not None:
        self.runInferenceDialogue.textEdit.append(errorMessage)

    if enoughImages is False:
        self.previewImagesNum = imageCount

        # Update preview images number
        ui_general.SetPreviewImagesNum(self, self.runInferenceDialogue)

    # Set progress bar max value
    self.inferenceProgressBarMaxValue = self.previewImagesNum

    # Set model directory
    self.modelDir = config.pretrainedModels

    # Set map name
    mapPath, mapFileFound = general_error.GetMapPath(self.selectedModel, config.pretrainedModels)
    if mapFileFound:
        self.mapPath = mapPath

    # Reset progress bar
    self.runInferenceDialogue.progressBar.setValue(0)

    # Set progress bar
    ui_general.SetProgressBar(self, self.runInferenceDialogue)

    # Create thread to process images
    if modelNotEmpty and imagesDirNotEmpty and mapFileFound:
        ui_general.StartPreviewThread(self, self.runInferenceDialogue)

        # Disable widgets while processing images
        StartToggleRiWidgets(self)

        # Update dialogue
        self.runInferenceDialogue.textEdit.append("Commencing inference.")
    else:
        if modelNotEmpty is False:
            QtWidgets.QMessageBox.information(self.runInferenceDialogue, "No model found", "Please select a model first.", QtWidgets.QMessageBox.Ok)
        if imagesDirNotEmpty is False:
            QtWidgets.QMessageBox.information(self.runInferenceDialogue, "No image directory selected", "Please select a test images directory first.", QtWidgets.QMessageBox.Ok)
        if mapFileFound is False:
            QtWidgets.QMessageBox.information(self.runInferenceDialogue, "No map file found", "The model you have selected does not have a map file. Please select a different model.", QtWidgets.QMessageBox.Ok)

def RunInferenceDialogue(self):
    """
    Load run inference dialogue.
    """
    if self.trainInProgress:
        QtWidgets.QMessageBox.information(self, "Object Detection Unavailable", "Training is already in progress.", QtWidgets.QMessageBox.Ok)
    else:
        # Set generate XML variable
        self.generateXML = False

        # Load models
        dataSets, errorMsg = general.ModelNames(config.pretrainedModels)
        if errorMsg is not None:
            errorMessage = "There was an error with preprocessing.get_all_files(). Reason: " + errorMsg
            self.previewInferenceDialogue.textEdit.append(errorMessage)

        # Insert models
        error, errorMsg = ui_general.InsertModels(self.runInferenceDialogue, dataSets)
        if error:
            errorMessage = "Could not add datasets to dialogue. Reason: " + errorMsg
            self.previewInferenceDialogue.textEdit.append(errorMessage)

        # Save datasets
        self.updateRIDatasets = dataSets

        # Set confidence threshold
        ui_general.SetConfThresh(self, self.runInferenceDialogue)

        # Make dialogue cursor invisible
        self.runInferenceDialogue.textEdit.setCursorWidth(0)

        # Update self.generateReport value
        self.generateReport = self.generateReportRi

        # Update showImagesCheckBox
        self.runInferenceDialogue.showImagesCheckBox.setChecked(self.showImages)

        # Update reportCheckBox
        self.runInferenceDialogue.reportCheckBox.setChecked(self.generateReport)

        # Update image count, if directory already previously selected
        if self.testImagesPath is not None:
            GetRunImagesCount(self, False)

        # Update reportTitle
        UpdateReportTitle(self)

        # Disable/enable report title
        ToggleReportTitle(self)

        # Enable widgets in dialogue
        EnableRiWidgets(self)

        # Start update combo timer
        StartUpdateTimer(self)

        # Set default button
        ui_general.DefaultButton(self.runInferenceDialogue)

        # Show dialogue
        self.runInferenceDialogue.show()

        # Close threads, if dialogue is rejected (x button is clicked)
        if self.runInferenceDialogue.exec_() == QtWidgets.QDialog.Rejected:
            ui_general.CancelButton(self, self.runInferenceDialogue)

            # Cancel toggle timer
            StopToggleRiWidgets(self)
