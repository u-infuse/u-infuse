"""
Author:  Chris Lawson
Contact: clawso21@une.edu.au
Source:  U-Infuse
Purpose: Functions for the U-Infuse Main Window.
"""
import sys
from PyQt5 import QtWidgets, QtCore, QtGui
import config
import general
import general_error
import ui_general
import interface_tm
import class_rn
import messaging

# Variables
rn = None

def ExitUInfuse(self):
    """
    Closes U-Infuse.
    """
    exitMessage = QtWidgets.QMessageBox.Yes

    # Check if training is in progress
    if self.trainInProgress:
        exitMessage = QtWidgets.QMessageBox.information(self, "Training in progress", "Training is in progress. Are you sure you would like to exit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

    # Exit if training isn't in progress, or "Yes" was chosen in popup message
    if exitMessage == QtWidgets.QMessageBox.Yes:
        sys.exit()

def StartButton(self):
    """
    Called when Start button is clicked.
    """
    # Train
    error, errorMsg = general_error.TrainErrorCheck(self.pretrainedModel, self.chosenDataSets, self.chosenClasses)
    if error:
        errorMessage = "There was an error with training settings: " + errorMsg
        self.textEdit.append(errorMessage)

    #Check if any dialogues are open
    openDialogues = ui_general.OpenDialogues(self)

    if (error is False) and (self.trainInProgress is False) and (openDialogues is False) and (self.generatingCsv is False):
        # Set bool for train in progress
        self.trainInProgress = True

        self.textEdit.append("Starting model training.\n")
        # Set training parameters
        pretrainedModel, batchSize, steps, epochs, error, errorMsg = interface_tm.TrainingParameters(self.pretrainedModel, self.batchSize, self.epochs)

        if error:
            errorMessage = "There was an error with train_main.set_training_parameters(): " + str(errorMsg)
            self.text.append(errorMessage)

        # Set progress bar values
        self.mainProgressBarMaxValue, self.mainProgressBarCount, errorMsg = general.SetProgressBar(epochs, steps)

        if errorMsg is not None:
            errorMessage = "There was an error with setting progress bar values: " + str(errorMsg)
            self.text.append(errorMessage)

        # Set progress bar
        self.mainProgressBar.setMaximum(self.mainProgressBarMaxValue)

        # Timer to update UI
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(lambda: UpdateUI(self))
        self.timer.start(1000)

        # Disable start button
        self.startButton.setDisabled(True)

        # Train
        if error is False:
            # Set main progress bar to 0
            self.mainProgressBar.setValue(0)

            # Start RetinaNet training
            global rn
            rn = class_rn.RetinaNetTrain(config.snapshots, pretrainedModel, batchSize, steps, epochs)
            rn.setDaemon(True)
            rn.start()
        else:
            errorMessage = "There was an error with train_main.set_training_parameters(). Reason: " + errorMsg
            self.textEdit.append(errorMessage)
    else:
        if error:
            self.textEdit.append("Please generate model training files first.")

            # Set training to not in progress
            self.trainInProgress = False

        if openDialogues:
            self.textEdit.append("Please close all dialogue windows before starting model training.")

        if self.generatingCsv:
            self.textEdit.append("Training cannot start until all training files have finished generating.")

def StopButton(self):
    """
    Stop training.
    """
    if self.trainInProgress:
        # Stop training thread
        global rn
        rn.CloseThread()

        # Update train in progress bool
        self.trainInProgress = False

        # Update main window
        self.textEdit.append("\nTraining has been stopped.")
    else:
        # Update main window
        self.textEdit.append("There is no training to stop.")

def UpdateUI(self):
    """
    Update UI during training.
    """
    global rn

    try:
        while len(rn.output) > 0:

            # Error checking for when an incompatible model is loaded
            if len(rn.output) > 1000:
                self.trainInProgress = False
                rn.exit = True
                self.textEdit.append("RetinaNet was unable to load and training cannot continue. Training stopped.")
                break

            # Get output string
            output = rn.output.pop(0)

            # Increment progress bar
            if ("] - ETA:" in output) or ("saving model to" in output):
                self.mainProgressBarCount += 1
                if self.mainProgressBarCount <= self.mainProgressBarMaxValue:
                    self.mainProgressBar.setValue(self.mainProgressBarCount)

            # Remove certain RetinaNet output
            output = messaging.BannedWords(output)

            # Preprocess output
            output, deleteLast = messaging.PreprocessOutput(output)

            if deleteLast:
                textCursor = self.textEdit.textCursor()
                textCursor.movePosition(QtGui.QTextCursor.End)
                textCursor.select(QtGui.QTextCursor.LineUnderCursor)
                textCursor.removeSelectedText()
                textCursor.deletePreviousChar()
                self.textEdit.setTextCursor(textCursor)

            # Change output via keyword searches
            output = messaging.KeywordChange(output)

            # Print modified output
            if output is not None:
                self.textEdit.append(output)

    except Exception as e:
        self.textEdit.append("Could not update main window UI. Reason: " + str(e))

    # Print error message, if exists
    try:
        while len(rn.error) > 0:
            errorMsg = rn.error.pop(0)
            self.textEdit.append("There has been an error with RetinaNet: " + errorMsg)

            # Break if there is a problem with error
            if len(rn.error) > 1000:
                break
    except Exception as e:
        self.textEdit.append("Could not display error message. Reason: " + str(e))

    # Cancel training if thread has finished
    try:
        if rn.exit:
            self.trainInProgress = False
    except Exception as e:
        self.textEdit.append("Thread closing error. Reason: " + str(e))

    # Stop timer if training not in progress
    try:
        if self.trainInProgress is False:
            self.mainProgressBar.setValue(self.mainProgressBarMaxValue)
            self.timer.stop()

            # Enable start button
            self.startButton.setDisabled(False)
    except Exception as e:
        self.textEdit.append("Could not stop training timer. Reason: " + str(e))
