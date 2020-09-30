"""
Author:  Chris Lawson
Contact: clawso21@une.edu.au
Source:  U-Infuse
Purpose: Functions for the Settings Dialogue.
"""
from PyQt5 import QtCore, QtWidgets
import ui_general
import general

def PreviewScrollCheckBox(self):
    """
    Changes self.scrollPreview value when checkbox state is changed.
    """
    try:
        if self.settingsDialogue.previewScrollCheckBox.isChecked() is False:
            self.previewScroll = False
        else:
            self.previewScroll = True
    except Exception as e:
        errorMessage = "There was an error changing preview scroll checkbox value. Reason: " + str(e)
        self.textEdit.append(errorMessage)

def SetSelectedBackgroundOption(self):
    """
    Changes the selected background option.
    """
    try:
        self.chosenBackground = self.settingsDialogue.backgroundComboBox.currentText()
    except Exception as e:
        errorMessage = "There was an error setting the chosen background selection. Reason: " + str(e)
        self.textEdit.append(errorMessage)

def SetBackgroundOptions(self):
    """
    Adds items to the background combobox.
    """
    # Add items to combobox
    try:
        self.settingsDialogue.backgroundComboBox.clear()
        for name in self.backgroundOptions:
            self.settingsDialogue.backgroundComboBox.addItem(name)
    except Exception as e:
        errorMessage = "Could not add background options. Reason: " + str(e)
        self.textEdit.append(errorMessage)

    # Set selected item
    try:
        itemIndex = self.settingsDialogue.backgroundComboBox.findText(self.chosenBackground, QtCore.Qt.MatchFixedString)
        if itemIndex >= 0:
            self.settingsDialogue.backgroundComboBox.setCurrentIndex(itemIndex)
    except Exception as e:
        errorMessage = "Could not set selected background. Reason: " + str(e)
        self.textEdit.append(errorMessage)

def SaveSettings(self):
    """
    Save settings.
    """
    # Save selected background
    SetSelectedBackgroundOption(self)

    # Save settings file
    errorMsg = general.SaveTrainSettings(self.epochs, self.batchSize, self.negative, self.pretrainedModel, self.chosenDataSets, self.negativeChosenDataSets, self.chosenClasses, self.chosenBackground, self.previewScroll)

    if errorMsg is not None:
        errorMessage = "Could not save settings. Reason: " + errorMsg
        self.textEdit.append(errorMessage)

    # Close dialogue
    self.settingsDialogue.reject()

def SettingsDialogue(self):
    """
    Loads the settings dialogue.
    """

    if self.trainInProgress:
        QtWidgets.QMessageBox.information(self.settingsDialogue, "Cannot Change Settings", "Training is already in progress.", QtWidgets.QMessageBox.Ok)
    else:
        # Load background options
        SetBackgroundOptions(self)

        # Update negative checkbox
        self.settingsDialogue.previewScrollCheckBox.setChecked(self.previewScroll)

        # Show dialogue
        self.settingsDialogue.show()

        # Cancel all if dialogue is rejected (x button is clicked)
        if self.settingsDialogue.exec_() == QtWidgets.QDialog.Rejected:
            ui_general.CancelButton(self, self.settingsDialogue)
