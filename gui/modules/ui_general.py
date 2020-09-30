"""
Author:  Chris Lawson
Contact: clawso21@une.edu.au
Source:  U-Infuse
Purpose: General UI functions for the UI.
"""
import os
from PyQt5 import QtCore, QtWidgets, QtGui
import qimage2ndarray
import class_preview
import class_report
import class_annotate
import general
import general_error
import general_image
import config

# Variables
previewThread = None
reportThread = None
xmlThread = None

def OpenDialogues(self):
    """
    Checks to see if any dialogues are visible.
    Returns True if there are visible dialogues, and False if there are not.
    """
    openDialogues = False

    # Check train dialogue 1
    if self.trainDialogue1.isVisible():
        openDialogues = True

    # Check train dialogue 2
    if openDialogues is False:
        if self.trainDialogue2.isVisible():
            openDialogues = True

    # Check auto-annotate dialogue
    if openDialogues is False:
        if self.autoAnnotateDialogue.isVisible():
            openDialogues = True

    # Check preview inference dialogue
    if openDialogues is False:
        if self.previewInferenceDialogue.isVisible():
            openDialogues = True

    # Check run inference dialogue
    if openDialogues is False:
        if self.runInferenceDialogue.isVisible():
            openDialogues = True

    return openDialogues

def GetReportErrors(self):
    """
    Return report errors.
    """
    reportErrors = []
    errorMsg = None

    try:
        if self.generateReport:
            global reportThread
            if reportThread is not None:
                if len(reportThread.errors) > 0:
                    for errorItem in reportThread.errors:
                        reportErrors.append(errorItem)
    except Exception as e:
        errorMsg = str(e)

    return reportErrors, errorMsg

def SetSelectedClasses(self):
    """
    Sets pre-selected classes.
    """
    errorMsg = None

    try:
        if len(self.chosenClasses) > 0:
            for className in self.chosenClasses:
                classItems = self.trainDialogue1.classesList.findItems(className, QtCore.Qt.MatchFixedString)
                for item in classItems:
                    item.setSelected(True)
    except Exception as e:
        errorMsg = str(e)

    return errorMsg

def SetSelectedDatasets(self):
    """
    Sets pre-selected datasets.
    """
    errorMsg = None

    try:
        if len(self.chosenDataSets) > 0:
            for dataset in self.chosenDataSets:
                datasetItems = self.trainDialogue1.foldersList.findItems(dataset, QtCore.Qt.MatchFixedString)
                for item in datasetItems:
                    item.setSelected(True)

            # Set focus
            self.trainDialogue1.foldersList.setFocus()
    except Exception as e:
        errorMsg = str(e)

    return errorMsg

def SelectPretrainedModel(self):
    """
    Sets the pretrained model.
    """
    # Set pretrained model in dialogue
    try:
        modelIndex = self.trainDialogue2.dataSetsComboBox.findText(self.pretrainedModel, QtCore.Qt.MatchFixedString)
        if modelIndex > -1:
            self.trainDialogue2.dataSetsComboBox.setCurrentIndex(modelIndex)
    except Exception as e:
        self.textEdit.append("Could not set pretrained model. Reason: " + str(e))

def SetTrainSettings(self):
    """
    Sets train settings if a settings file exists.
    """
    epochs, batchSize, negative, pretrainedModel, datasets, negativeDatasets, classes, fileExists, backgroundOption, previewScroll, errorMsg = general.LoadTrainSettings()

    if errorMsg is None:
        if fileExists:
            self.epochs = epochs
            self.batchSize = batchSize
            self.negative = negative
            self.pretrainedModel = pretrainedModel
            self.chosenDataSets = datasets
            self.negativeChosenDataSets = negativeDatasets
            self.chosenClasses = classes
            self.chosenBackground = backgroundOption
            self.previewScroll = previewScroll
    else:
        errorMessage = "There was an error loading settings file: " + errorMsg
        self.textEdit.append(errorMessage)

def SetPretrainedModel(self):
    """
    Sets pretrained training model when called.
    """
    try:
        self.pretrainedModel = self.trainDialogue2.dataSetsComboBox.currentText()
    except Exception as e:
        errorMessage = "There was an error with setting pretrained model. Reason: " + str(e)
        self.textEdit.append(errorMessage)

def DefaultButton(dialogue):
    """
    Sets default button for a dialogue
    """
    # Default button for all dialogues is the cancel button
    try:
        dialogue.cancelButton.setDefault(True)
    except Exception as e:
        errorMessage = "There was an error setting the default button. Reason: " + str(e)
        dialogue.textEdit.append(errorMessage)

def ShowImagesCheckBox(self, dialogue):
    """
    Changes value if the checkbox is checked/unchecked.
    """
    if dialogue.showImagesCheckBox.isChecked() is False:
        self.showImages = False
    else:
        self.showImages = True

def CancelButton(self, dialogue):
    """
    Cancels the class preview thread and closes the dialogue.
    """
    # Send exit message to preview thread
    global previewThread
    if previewThread is not None:
        previewThread.CloseThread()

    # Set cancel preview variable to True
    self.cancelPreview = True

    # Stop combobox update timer
    StopUpdateTimer(self)

    # Close the dialogue
    dialogue.reject()

def StopUpdateTimer(self):
    """
    Stops combo box update timer.
    """
    try:
        self.updateTimer.stop()
    except Exception:
        pass

def SetPreviewImagesNum(self, dialogue):
    """
    Set the number of preview images.
    """
    try:
        dialogue.previewImagesNum.setText(str(self.previewImagesNum))
    except Exception as e:
        errorMessage = "Could not update preview images number in the preview inference dialogue. Reason: " + str(e)
        dialogue.textEdit.append(errorMessage)

def GetPreviewImagesNum(self, intString):
    """
    Get the number of preview images.
    """
    try:
        stringNotEmpty = general_error.StringNotEmpty(intString)

        if stringNotEmpty:
            numInt = int(intString)
            self.previewImagesNum = numInt

    except Exception as e:
        errorMessage = "Could not update number of test images in preview inference dialogue. Reason: " + str(e)
        self.textEdit.append(errorMessage)

def SetPreviewImage(self, dialogue):
    """
    Converts an np image to QImage and adds the image  to the textEdit widget.
    """
    qImage = None
    global previewThread

    # Stop preview timer if dialogue is closed/cancelled
    if self.cancelPreview:
        self.cancelPreview = False
        self.previewTimer.stop()
        self.inferenceInProgress = False

        # Enable settings menu
        self.menuSettings.setDisabled(False)

    # Convert image
    try:
        if len(previewThread.previewImages) > 0:
            imgData = previewThread.previewImages.pop(0)
            if  imgData is not None:
                if imgData[3] is False:
                    # Save data to be used for the report
                    previewThread.processedImages.append(imgData)

                    # Convert to QImage
                    npImage = imgData[0]

                    # Clear widget if it is the first image
                    if self.firstPreviewImage:
                        self.firstPreviewImage = False
                        dialogue.textEdit.clear()

                    # Get numpy array dimensions
                    dialogueHeight = 480
                    dialogueWidth = 640
                    height, width, channel = npImage.shape
                    dialogueShape = [dialogueHeight, dialogueWidth, height, width, channel]
                    npImage, errorMsg = general_image.ResizeImage(npImage, dialogueShape, imgData[2], imgData[4], self.chosenBackground)

                    # Print errors to dialogue if they exist
                    if errorMsg is not None:
                        errorMessage = "Image could not be resized. Reason: " + errorMsg
                        dialogue.textEdit.append(errorMessage)

                    # Create QImage
                    qImage = qimage2ndarray.array2qimage(npImage)
                    # Uncomment below for an alternative to the qimage2ndarray package
                    #bytesPerLine = 3 * npImage.shape[1]
                    #qImage = QtGui.QImage(npImage, npImage.shape[1], npImage.shape[0], bytesPerLine, QtGui.QImage.Format_RGB888)

                    # If auto-annotation is active
                    if self.generateXML:
                        global xmlThread
                        xmlThread.CreateXML(imgData[2], imgData[1], npImage.shape)
                        xmlErrors = xmlThread.ReturnErrors()
                        if xmlErrors is not None:
                            for errorMsg in xmlErrors:
                                errorMessage = "There was an error with auto_annotation.py: " + errorMsg
                                dialogue.textEdit.append(errorMessage)
            else:
                self.previewTimer.stop()
                self.inferenceInProgress = False
                dialogue.textEdit.append("Inference complete")

                # Enable settings menu
                self.menuSettings.setDisabled(False)

                # Generate report, if option selected.
                if self.generateReport:
                    global reportThread
                    processedImages = previewThread.ProcessedImages()
                    reportThread = class_report.ReportInterface(self.reportTitle, self.selectedModel, self.testImagesPath, self.confThresh, processedImages)
                    reportThread.setDaemon(True)
                    reportThread.start()
    except Exception as e:
        errorMessage = "Could not convert np to QImage. Reason: " + str(e)
        dialogue.textEdit.append(errorMessage)

    # Add image to textedit
    try:
        if qImage is not None:
            if self.showImages:
                self.nameCounter += 1
                imageUrl = QtCore.QUrl("image" + str(self.nameCounter))
                dialogue.textEdit.document().addResource(QtGui.QTextDocument.ImageResource, imageUrl, QtCore.QVariant(qImage))
                imageInsert = QtGui.QTextImageFormat()

                # Insert image
                imageInsert.setWidth(dialogueWidth)
                imageInsert.setHeight(dialogueHeight)
                imageInsert.setName(imageUrl.toString())
                dialogue.textEdit.textCursor().insertImage(imageInsert)

                # Move curser to the end
                if self.previewScroll:
                    dialogue.textEdit.moveCursor(QtGui.QTextCursor.End)

            # Increment progress bar
            self.inferenceProgressBarCount += 1
            if self.inferenceProgressBarCount <= self.inferenceProgressBarMaxValue:
                dialogue.progressBar.setValue(self.inferenceProgressBarCount)
    except Exception as e:
        errorMessage = "Could not add QImage. Reason: " + str(e)
        dialogue.textEdit.append(errorMessage)

    # Display thread error messages if there are any
    errorMessages = previewThread.GetErrors()
    try:
        for msg in errorMessages:
            dialogue.textEdit.append(msg)
    except Exception as e:
        errorMsg = "Could not add error message to dialogue. Reason: " + str(e)
        dialogue.textEdit.append(errorMsg)

def StartPreviewThread(self, dialogue):
    """
    Starts the preview thread to process images.
    """
    try:
        # Call thread to process images
        global previewThread
        previewThread = class_preview.PreviewImages(self.testImagesPath, self.selectedModel, self.mapPath, self.modelDir, self.confThreshConverted, self.previewImagesNum)
        previewThread.setDaemon(True)
        previewThread.start()

        # Generate auto-annotate thread
        if self.generateXML:
            global xmlThread
            xmlThread = class_annotate.AnnotateImage(self.testImagesPath, self.confThresh)
            xmlThread.setDaemon(True)
            xmlThread.start()

        # Create timer to call function that processes and adds images 1 by 1 until list is empty
        self.previewTimer = QtCore.QTimer()
        self.previewTimer.timeout.connect(lambda: SetPreviewImage(self, dialogue))
        self.previewTimer.start(1000)

        # Disable settings menu
        self.menuSettings.setDisabled(True)

    except Exception as e:
        errorMessage = "Could not start preview thread. Reason: " + str(e)
        dialogue.textEdit.append(errorMessage)

def SetProgressBar(self, dialogue):
    """
    When called sets the dialogue progress bar.
    """
    try:
        dialogue.progressBar.setMaximum(self.previewImagesNum)
        self.inferenceProgressBarCount = 0
        dialogue.progressBar.setValue(0)
    except Exception as e:
        errorMessage = "Could not set dialogue progress bar. Reason: " + str(e)
        dialogue.textEdit.append(errorMessage)

def SetModel(self, dialogue):
    """
    When called sets the model name to the self.selectedModel variable.
    """
    try:
        self.selectedModel = dialogue.dataSetsComboBox.currentText()
    except Exception as e:
        errorMessage = "Could not get item from pretrained models list. Reason: " + str(e)
        dialogue.append(errorMessage)

def UpdateConfThresh(self, dialogue, thresh):
    """
    Changes stored confidence threshold value.
    """
    intVal = 0
    validInt = False

    # Ensure new value is a number
    errorMsg, intVal = general.IsAnInt(thresh)

    if errorMsg is not None:
        errorMessage = "Threshold value must be a number."
        dialogue.textEdit.append(errorMessage)
    else:
        # Ensure value is only between 0 - 100
        validInt = general.ValidConfInt(intVal)

        if validInt is False:
            errorMessage = "Threshold value must be between 0 - 100."
            dialogue.textEdit.append(errorMessage)
        #else:
        #    # Update self.confThresh
        #    self.confThresh = thresh

    # Convert threshold value from percentage
    if (errorMsg is None) and validInt:
        confThresh, errorMsg = general.ConvertConfThresh(intVal)

    # Set new threshold value
    if errorMsg is None:
        self.confThreshConverted = confThresh
        self.confThresh = thresh

def InsertModels(dialogue, dataSets):
    """
    Inserts models into the datasets combobox.
    """
    error = False
    errorMsg = ""
    try:
        if dialogue is not None:
            # Clear old items
            dialogue.dataSetsComboBox.clear()

            # Add new items
            if isinstance(dataSets, (list, dict, tuple, set)):
                for name in dataSets:
                    dialogue.dataSetsComboBox.addItem(name)
            else:
                if isinstance(dataSets, str):
                    dialogue.dataSetsComboBox.addItem(name)
    except Exception as e:
        error = True
        errorMsg = str(e)

    return error, errorMsg

def SetConfThresh(self, dialogue):
    """
    Set confidence threshold.
    """
    try:
        if dialogue is not None:
            dialogue.confidenceThresholdNum.setText(str(self.confThresh))
    except Exception as e:
        errorMessage = "Could not update the confidence threshold in the dialogue. Reason: " + str(e)
        self.textEdit.append(errorMessage)

def GetTexts(self):
    """
    Returns the current value for the epoch and batch size line text boxes.
    """
    # Get new values
    try:
        self.epochs = int(self.trainDialogue2.epochsText.text())
        self.batchSize = int(self.trainDialogue2.batchSizeText.text())
    except Exception as e:
        errorMsg = "Could not change epochs or batch size. Reason: " + str(e)
        self.textEdit.append(errorMsg)

def GetPreviewImagesCount(self, dialogue):
    """
    Gets the preview images count.
    """
    # Set test images path
    TestImagesPath(self, dialogue)

    # Set image count
    enoughImages, imageCount, errorMessage = general_image.EnoughImages(self.testImagesPath, self.previewImagesNum)
    if errorMessage is not None:
        dialogue.textEdit.append(errorMessage)

    # Set max images, if set to more than available
    if enoughImages is False:
        self.previewImagesNum = imageCount

    # Update preview images number
    SetPreviewImagesNum(self, dialogue)

def TestImagesPath(self, dialogue):
    """
    Sets the self.testImages path.
    """
    selectedDir = SelectDir(self, dialogue)
    error = False
    errorMsg = "No directory selected."

    # Check directory path is set
    try:
        if os.path.exists(selectedDir):
            self.testImagesPath = selectedDir
        else:
            error = True
    except Exception as e:
        error = True
        errorMsg = str(e)

    # Display error message if one is generated
    if error:
        errorMsg = "Could not add test images directory. Reason: " + errorMsg
        dialogue.textEdit.append(errorMsg)

def SelectDir(self, dialogue):
    """
    Calls the QFileDialog and returns the directory path.
    """
    selectedDir = None

    # Get directory name
    try:
        selectedDir = QtWidgets.QFileDialog.getExistingDirectory(dialogue, "Select a folder to add", config.datasets, QtWidgets.QFileDialog.ShowDirsOnly)
    except Exception as e:
        errorMsg = "Could not select directory. Reason: " + str(e)
        self.textEdit.append(errorMsg)

    return selectedDir
