"""
Author:  Chris Lawson
Contact: clawso21@une.edu.au
Source:  U-Infuse
Purpose: Functions for the Training Dialogues.
"""
from PyQt5 import QtWidgets, QtCore
import config
import general
import general_error
import ui_general
import class_datasets
import class_classes
import class_generate

# Variables
datasetsThread = None
classesThread = None
generateThread = None

def StartUpdateCombo(self):
    """
    Starts update combo box.
    """
    self.updateTimer = QtCore.QTimer()
    self.updateTimer.timeout.connect(lambda: UpdateCombo(self))
    self.updateTimer.start(1000)

def StartUpdateClasses(self):
    """
    Timer that updates classes in seperate thread.
    """
    self.classesTimer = QtCore.QTimer()
    self.classesTimer.timeout.connect(lambda: UpdateClasses(self))
    self.classesTimer.start(100)
    self.availableClasses = []

def StopUpdateClasses(self):
    """
    Stops the update classes timer.
    """
    global classesThread
    classesThread = None
    self.classesTimer.stop()

    # Set selected classes
    errorMsg = ui_general.SetSelectedClasses(self)

    # Print error message if it exists
    if errorMsg is not None:
        errorMessage = "There was an error with setting classes: " + errorMsg
        self.textEdit.append(errorMessage)

    # Remove Processing...
    RemoveClassesProcessing(self)

def StopUpdateDatasets(self):
    """
    Stops the update datasets timer.
    """
    # Stop datasetsTimer
    self.datasetsTimer.stop()

    # Set selected datasets
    errorMsg = ui_general.SetSelectedDatasets(self)

    if errorMsg is None:
        # Start classes update
        if len(self.chosenDataSets) > 0:
            StartUpdateClasses(self)
    else:
        errorMessage = "There was an error with setting datasets: " + errorMsg
        self.textEdit.append(errorMessage)

def UpdateClasses(self):
    """
    Updates the datasets and classes widgets.
    """
    # Start RetinaNet training
    global classesThread
    if classesThread is None:
        # Add message to widget
        self.trainDialogue1.classesList.addItem("Processing...")

        # Instantiate classes object
        classesThread = class_classes.Classes(self.chosenDataSets)
        classesThread.setDaemon(True)
        classesThread.start()
    else:
        if classesThread.errorMsg is None:
            if classesThread.classesList is not None:
                self.trainDialogue1.classesList.clear()
                while len(classesThread.classesList) > 0:
                    classEntry = classesThread.classesList.pop()
                    self.trainDialogue1.classesList.addItem(classEntry)

                # Stop adding classes
                StopUpdateClasses(self)
        else:
            errorMessage = "There was an error with update_available_classes(). Reason: " + classesThread.errorMsg
            self.textEdit.append(errorMessage)
            StopUpdateClasses(self)

def StartUpdateDatasets(self):
    """
    Timer that updates datasets in seperate thread.
    """
    # Clear previous thread, if it exists to allow for directory updates.
    global datasetsThread
    if datasetsThread is not None:
        datasetsThread = None
        self.trainDialogue1.foldersList.clear()
        self.trainDialogue1.negativeFoldersList.clear()

    # Create timer
    self.datasetsTimer = QtCore.QTimer()
    self.datasetsTimer.timeout.connect(lambda: UpdateDatasets(self))
    self.datasetsTimer.start(100)

def RemoveClassesProcessing(self):
    """
    Removes the "Processing..." message from the classes list.
    """
    try:
        if len(self.chosenClasses) > 0:
            processingString = "Processing..."
            processingItems = self.trainDialogue1.classesList.findItems(processingString, QtCore.Qt.MatchFixedString)
            for item in processingItems:
                self.trainDialogue1.classesList.takeItem(self.trainDialogue1.classesList.row(item))
    except Exception as e:
        errorMessage = "Could not remove item from classes list. Reason: " + str(e)
        self.textEdit.append(errorMessage)

def UpdateDatasets(self):
    """
    Updates the datasets and classes widgets.
    """
    # Start RetinaNet training
    global datasetsThread
    if datasetsThread is None:
        # Instantiate datasets object
        datasetsThread = class_datasets.Datasets(config.datasets)
        datasetsThread.setDaemon(True)
        datasetsThread.start()
    else:
        if datasetsThread.errorMsg is None:
            if datasetsThread.datasets is not None:
                while len(datasetsThread.datasets) > 0:
                    datasetEntry = datasetsThread.datasets.pop()
                    self.trainDialogue1.foldersList.addItem(datasetEntry)

                    # Add item to negative list if enabled
                    if self.negative:
                        self.trainDialogue1.negativeFoldersList.addItem(datasetEntry)

                # Stop datasets timer
                StopUpdateDatasets(self)
        else:
            errorMessage = "There was an error with adding dataset folders. Reason: " + datasetsThread.errorMsg
            self.textEdit.append(errorMessage)
            StopUpdateDatasets(self)

def UpdateCombo(self):
    """
    Updates combo box when directory changes.
    """
    # Load pretrained models
    dataSets, errorMsg = general.ModelNames(config.pretrainedModels)
    if errorMsg is not None:
        errorMessage = "There was an error with preprocessing.get_all_files(). Reason: " + errorMsg
        self.textEdit.append(errorMessage)

    if dataSets != self.updateTRDatasets:
        self.updateTRDatasets = dataSets

        # Insert pretrained models
        error, errorMsg = ui_general.InsertModels(self.trainDialogue2, dataSets)
        if error:
            errorMessage = "Could not add datasets to dialogue. Reason: " + errorMsg
            self.textEdit.append(errorMessage)

def StopGenerateTimer(self):
    """
    Stops the generateTimer.
    """
    self.generateTimer.stop()
    global generateThread
    generateThread = None
    self.generatingCsv = False

    # Enable main window start button
    self.startButton.setDisabled(False)

def GenerateCheck(self):
    """
    Checks to see if the training CSV files were generated.
    """
    # Check if CSV files exist
    csvExist, error, errorMsg = general_error.CheckCSV()

    if error is False:
        if csvExist:

            # Update message
            self.textEdit.append("Finished generating training configuration files.")

            # Save settings file
            errorMsg = general.SaveTrainSettings(self.epochs, self.batchSize, self.negative, self.pretrainedModel, self.chosenDataSets, self.negativeChosenDataSets, self.chosenClasses, self.chosenBackground, self.previewScroll)

            if errorMsg is not None:
                errorMessage = "Could not save settings file. Reason: " + errorMsg
                self.textEdit.append(errorMessage)
        else:
            errorMessage = "Could not generate training classes. Reason: " + errorMsg
            self.textEdit.append(errorMessage)

def GenerateTrainScripts(self):
    """
    Generates training scripts.
    """
    global generateThread

    if generateThread is None:
        self.textEdit.append("Generating training configuraton files.")
        generateThread = class_generate.Generate(self.chosenDataSets, self.chosenClasses, self.negative, self.negativeChosenDataSets)
        generateThread.setDaemon(True)
        generateThread.start()
    else:
        try:
            if len(generateThread.errorMsg) > 0:
                errorMsg = generateThread.errorMsg.pop()

                if errorMsg is not None:
                    errorMessage = "There was an error with train_main.generate_training_scripts(). Reason: " + errorMsg
                    self.textEdit.append(errorMessage)
                else:
                    # Ensures CSV files were generated
                    GenerateCheck(self)

                # Stop generate timer
                StopGenerateTimer(self)
        except Exception as e:
            errorMessage = "There was an error with train_main.generate_training_scripts(). Reason: " + str(e)
            self.textEdit.append(errorMessage)

def StartUpdateGenerate(self):
    """
    Starts generate scripts timer.
    """
    self.generateTimer = QtCore.QTimer()
    self.generateTimer.timeout.connect(lambda: GenerateTrainScripts(self))
    self.generateTimer.start(1000)
    self.generatingCsv = True

    # Disable main window start button
    self.startButton.setDisabled(True)

def Train1YesButton(self):
    """
    Yes button option for the training configuration dialogue.
    """
    # Ensure self.chosenDataSets and self.chosenClasses are not empty
    if (len(self.chosenDataSets) > 0) and (len(self.chosenClasses) > 0):
        # Call generate_training_scripts()
        StartUpdateGenerate(self)

        # Close dialogue
        self.trainDialogue1.reject()
    else:
        QtWidgets.QMessageBox.information(self.trainDialogue1, "Cannot save choices", "Please select at least one dataset and one class.", QtWidgets.QMessageBox.Ok)

def Train2YesButton(self):
    """
    Yes button option for the training configuration dialogue.
    """
    # Set epochs and batch size
    ui_general.GetTexts(self)

    # Set pretrained model
    ui_general.SetPretrainedModel(self)

    # Save settings file
    errorMsg = general.SaveTrainSettings(self.epochs, self.batchSize, self.negative, self.pretrainedModel, self.chosenDataSets, self.negativeChosenDataSets, self.chosenClasses, self.chosenBackground, self.previewScroll)

    if errorMsg is not None:
        errorMessage = "Could not save settings file. Reason: " + errorMsg
        self.textEdit.append(errorMessage)

    # Update textEdit widget
    self.textEdit.append("Model training settings updated.")

    # Close dialogue
    self.trainDialogue2.reject()

def TrainingDialogue1(self):
    """
    Load training config dialogue.
    """
    # Ensure that training is not already in progress
    if self.trainInProgress:
        QtWidgets.QMessageBox.information(self.trainDialogue1, "Cannot Edit Training Settings", "Training is already in progress.", QtWidgets.QMessageBox.Ok)
    else:
        # Set generate XML variable
        self.generateXML = False

        # Update negative checkbox
        self.trainDialogue1.negativeCheckBox.setChecked(self.negative)

        # Clear list widgets
        self.trainDialogue1.classesList.clear()

        # Update folders list
        StartUpdateDatasets(self)

        # Load training settings
        ui_general.SetTrainSettings(self)

        # Show training configuration dialogue
        self.trainDialogue1.show()

        # Cancel all if dialogue is rejected (x button is clicked)
        if self.trainDialogue1.exec_() == QtWidgets.QDialog.Rejected:
            ui_general.CancelButton(self, self.trainDialogue1)

def TrainingDialogue2(self):
    """
    Load training config dialogue.
    """
    # Ensure that training is not already in progress
    if self.trainInProgress:
        QtWidgets.QMessageBox.information(self.trainDialogue2, "Cannot Edit Training Settings", "Training is already in progress.", QtWidgets.QMessageBox.Ok)
    else:
        # Set generate XML variable
        self.generateXML = False

        # Set text widgets
        self.trainDialogue2.epochsText.setText(str(self.epochs))
        self.trainDialogue2.batchSizeText.setText(str(self.batchSize))

        # Start update combo timer
        StartUpdateCombo(self)

        # Load pretrained models
        dataSets, errorMsg = general.ModelNames(config.pretrainedModels)
        if errorMsg is not None:
            errorMessage = "There was an error with preprocessing.get_all_files(). Reason: " + errorMsg
            self.textEdit.append(errorMessage)

        # Insert pretrained models
        error, errorMsg = ui_general.InsertModels(self.trainDialogue2, dataSets)
        if error:
            errorMessage = "Could not add datasets to dialogue. Reason: " + errorMsg
            self.textEdit.append(errorMessage)

        # Select pretrained model in train dialogue 2
        ui_general.SelectPretrainedModel(self)

        # Save datasets
        self.updateTRDatasets = dataSets

        #Set framework combobox
        self.trainDialogue2.frameworkComboBox.addItem("RetinaNet")

        # Load training settings
        ui_general.SetTrainSettings(self)

        # Show training configuration dialogue
        self.trainDialogue2.show()

        # Cancel all if dialogue is rejected (x button is clicked)
        if self.trainDialogue2.exec_() == QtWidgets.QDialog.Rejected:
            ui_general.CancelButton(self, self.trainDialogue2)

def PopulateNegativeList(self):
    """
    Populates negative list.
    """
    # Populate list if it has been cleared
    if (self.trainDialogue1.negativeFoldersList.count() == 0) and self.negative:
        try:
            datasetsItems = []
            for index in range(self.trainDialogue1.foldersList.count()):
                datasetsItems.append(self.trainDialogue1.foldersList.item(index).text())

            for item in datasetsItems:
                self.trainDialogue1.negativeFoldersList.addItem(item)
        except Exception as e:
            errorMessage = "Could not add item to negative folders list. Reason: " + str(e)
            self.textEdit.append(errorMessage)

    # Get all negative list items
    negativeItems = []
    try:
        for index in range(self.trainDialogue1.negativeFoldersList.count()):
            negativeItems.append(self.trainDialogue1.negativeFoldersList.item(index))
    except Exception as e:
        errorMessage = "Could not add item to negative folders list. Reason: " + str(e)
        self.textEdit.append(errorMessage)

    # Select opposite of items selected by datasets list
    try:
        self.negativeChosenDataSets = []
        for negativeItem in negativeItems:
            # Set selected negative datasets as the opposite of the selected datasets
            if negativeItem.text() not in self.chosenDataSets:
                if negativeItem.text() in self.negativeChosenDataSets:
                    negativeItem.setSelected(True)
                else:
                    negativeItem.setSelected(True)
            else:
                negativeItem.setSelected(False)
    except Exception as e:
        errorMessage = "Could not add item to negative folders list. Reason: " + str(e)
        self.textEdit.append(errorMessage)

def NegativeFoldersListClicked(self):
    """
    Updates the negativeFoldersList widget.
    """
    # Add or Remove item from list self.chosenDataSets[]
    try:
        selectedItems = self.trainDialogue1.negativeFoldersList.selectedItems()
        self.negativeChosenDataSets = []

        if len(selectedItems) > 0:
            for item in selectedItems:
                if item.text() not in self.chosenDataSets:
                    self.negativeChosenDataSets.append(item.text())
                else:
                    item.setSelected(False)
                    if item.text() not in self.negativeErrors:
                        self.negativeErrors.append(item.text())
                        errorMessage = "Cannot select folder " + item.text() + " because it is already selected on the datasets folder list."
                        self.textEdit.append(errorMessage)
    except Exception as e:
        errorMessage = "Could not add item to negative folders list. Reason: " + str(e)
        self.textEdit.append(errorMessage)

def FoldersListClicked(self):
    """
    Triggered when an item is clicked in the foldersList widget in the train config dialogue window.
    """
    # Clear negative error messages
    self.negativeErrors = []

    # Add or Remove item from list self.chosenDataSets[]
    try:
        selectedItems = self.trainDialogue1.foldersList.selectedItems()
        self.chosenDataSets = []

        if len(selectedItems) > 0:
            for item in selectedItems:
                self.chosenDataSets.append(item.text())
        else:
            self.trainDialogue1.classesList.clear()

    except Exception as e:
        errorMessage = "Could not add item to folders list. Reason: " + str(e)
        self.textEdit.append(errorMessage)

    # Clear negative folder list selections and set opposite to chosen datasets
    PopulateNegativeList(self)

    # Update classes list
    if len(self.chosenDataSets) > 0:
        # Update training classes list
        if len(self.chosenDataSets) > 0:
            StartUpdateClasses(self)

def NegativeCheckBox(self):
    """
    Changes value if the checkbox is checked/unchecked.
    """
    if self.trainDialogue1.negativeCheckBox.isChecked() is False:
        self.negative = False

        # Disable negative QListWidget
        self.trainDialogue1.negativeFoldersList.setDisabled(True)
        self.trainDialogue1.negativeFoldersList.clear()
    else:
        self.negative = True

        # Enable negative QListWidget
        self.trainDialogue1.negativeFoldersList.setDisabled(False)
        PopulateNegativeList(self)

def ClassesListClicked(self):
    """
    Triggered when an item is added to the dataset folder list in the train
    config dialogue window.
    """
    # Add or Remove item from list self.chosenClasses[]
    try:
        selectedItems = self.trainDialogue1.classesList.selectedItems()
        self.chosenClasses = []

        for item in selectedItems:
            self.chosenClasses.append(item.text())
    except Exception as e:
        errorMessage = "Could not add item to classes list. Reason: " + str(e)
        self.textEdit.append(errorMessage)
