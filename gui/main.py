"""
Author:  Chris Lawson
Contact: clawso21@une.edu.au
Source:  U-Infuse
Purpose: Main Window for U-Infuse.
"""
import sys
from pathlib import Path
from PyQt5 import QtWidgets, uic, QtGui, QtCore
import ui_main
import ui_train
import ui_ri
import ui_pi
import ui_aa
import ui_settings
import ui_about
import ui_general

# Enable High DPI
if hasattr(QtCore.Qt, "AA_EnableHighDpiScaling"):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

if hasattr(QtCore.Qt, "AA_UseHighDpiPixmaps"):
    QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

class UInfuse(QtWidgets.QMainWindow):
    """
    Main GUI class for U-Infuse.
    """
    def __init__(self):
        super(UInfuse, self).__init__()
        mainUI = "main.ui"
        trainUI1 = "dialogue_train1.ui"
        trainUI2 = "dialogue_train2.ui"
        runInferenceUI = "dialogue_ri.ui"
        previewInferenceUI = "dialogue_pi.ui"
        autoAnnotateUI = "dialogue_aa.ui"
        settingsUI = "dialogue_settings.ui"
        aboutUI = "dialogue_about.ui"

        # Change location if frozen
        if getattr(sys, 'frozen', False):
            mainUI = Path(sys._MEIPASS) / mainUI
            trainUI1 = Path(sys._MEIPASS) / trainUI1
            trainUI2 = Path(sys._MEIPASS) / trainUI2
            runInferenceUI = Path(sys._MEIPASS) / runInferenceUI
            previewInferenceUI = Path(sys._MEIPASS) / previewInferenceUI
            autoAnnotateUI = Path(sys._MEIPASS) / autoAnnotateUI
            settingsUI = Path(sys._MEIPASS) / settingsUI
            aboutUI = Path(sys._MEIPASS) / aboutUI

        uic.loadUi(mainUI, self)
        self.trainDialogue1 = uic.loadUi(trainUI1)
        self.trainDialogue2 = uic.loadUi(trainUI2)
        self.runInferenceDialogue = uic.loadUi(runInferenceUI)
        self.previewInferenceDialogue = uic.loadUi(previewInferenceUI)
        self.autoAnnotateDialogue = uic.loadUi(autoAnnotateUI)
        self.settingsDialogue = uic.loadUi(settingsUI)
        self.aboutDialogue = uic.loadUi(aboutUI)

        # Set icons
        QtGui.QIcon("icon.png")
        self.setWindowIcon(QtGui.QIcon("icon.png"))
        self.trainDialogue1.setWindowIcon(QtGui.QIcon("icon.png"))
        self.trainDialogue2.setWindowIcon(QtGui.QIcon("icon.png"))
        self.runInferenceDialogue.setWindowIcon(QtGui.QIcon("icon.png"))
        self.previewInferenceDialogue.setWindowIcon(QtGui.QIcon("icon.png"))
        self.autoAnnotateDialogue.setWindowIcon(QtGui.QIcon("icon.png"))
        self.settingsDialogue.setWindowIcon(QtGui.QIcon("icon.png"))
        self.aboutDialogue.setWindowIcon(QtGui.QIcon("icon.png"))

        # Settings variables
        self.backgroundOptions = ["Striped", "Average Colour", "None"]
        self.chosenBackground = "Striped"
        self.previewScroll = True

        # Training variables
        self.highlightColour = None
        self.negative = True
        self.negativeErrors = []
        self.chosenDataSets = []
        self.negativeChosenDataSets = []
        self.availableClasses = []
        self.chosenClasses = []
        self.csvFiles = False
        self.pretrainedModel = "pretrained_COCO.h5"
        self.epochs = 30
        self.steps = 1
        self.batchSize = 2
        self.trainCorrect = False
        self.trainInProgress = False
        self.generatingCsv = False

        # Inference dialogues variables
        self.testImagesPath = None
        self.previewImagesNum = 10
        self.confThresh = 50
        self.confThreshConverted = 0.5
        self.deleteModels = True
        self.newModelName = "model_name"
        self.selectedSnapshot = None
        self.nameCounter = 0
        self.generateReport = True
        self.generateReportRi = True
        self.showImages = True
        self.cancelPreview = False
        self.mapPath = None
        self.reportTitle = "report_title"
        self.piWidgetsEnabled = True
        self.inferenceInProgress = False

        # Auto-annotate dialogue variables
        self.chosenAnnotator = "single_class_annotator.h5"
        self.multiClassCheckBox = False
        self.singleClassName = "Single class name"
        self.annotateClassesSet = {}
        self.generateXML = False

        # Load training settings
        ui_general.SetTrainSettings(self)

        # Main Window events
        self.startButton.clicked.connect(lambda: ui_main.StartButton(self))
        self.stopButton.clicked.connect(lambda: ui_main.StopButton(self))
        self.actionTrainConfig.triggered.connect(lambda: ui_train.TrainingDialogue1(self))
        self.actionTrainSettings.triggered.connect(lambda: ui_train.TrainingDialogue2(self))
        self.actionRunInference.triggered.connect(lambda: ui_ri.RunInferenceDialogue(self))
        self.actionModelPreview.triggered.connect(lambda: ui_pi.PreviewInferenceDialogue(self))
        self.actionAnnotate.triggered.connect(lambda: ui_aa.AutoAnnotateDialogue(self))
        self.actionExit.triggered.connect(lambda: ui_main.ExitUInfuse(self))
        self.actionAbout.triggered.connect(lambda: ui_about.AboutDialogue(self))
        self.actionSettings.triggered.connect(lambda: ui_settings.SettingsDialogue(self))

        # Settings Dialogue events
        self.settingsDialogue.yesButton.rejected.connect(lambda: ui_general.CancelButton(self, self.settingsDialogue))
        self.settingsDialogue.yesButton.accepted.connect(lambda: ui_settings.SaveSettings(self))
        self.settingsDialogue.previewScrollCheckBox.stateChanged.connect(lambda: ui_settings.PreviewScrollCheckBox(self))

        # About Dialogue events
        self.aboutDialogue.closeButton.clicked.connect(lambda: ui_about.CloseButton(self))

        # Training Configuration Dialogue events
        self.trainDialogue1.yesButton.accepted.connect(lambda: ui_train.Train1YesButton(self))
        self.trainDialogue1.yesButton.rejected.connect(lambda: ui_general.CancelButton(self, self.trainDialogue1))
        self.trainDialogue2.yesButton.accepted.connect(lambda: ui_train.Train2YesButton(self))
        self.trainDialogue2.yesButton.rejected.connect(lambda: ui_general.CancelButton(self, self.trainDialogue2))
        self.trainDialogue1.foldersList.itemSelectionChanged.connect(lambda: ui_train.FoldersListClicked(self))
        self.trainDialogue1.negativeFoldersList.itemSelectionChanged.connect(lambda: ui_train.NegativeFoldersListClicked(self))
        self.trainDialogue1.classesList.itemSelectionChanged.connect(lambda: ui_train.ClassesListClicked(self))
        self.trainDialogue1.negativeCheckBox.stateChanged.connect(lambda: ui_train.NegativeCheckBox(self))

        # Preview Inference Dialogue events
        self.previewInferenceDialogue.selectTestImagesButton.clicked.connect(lambda dialogue: ui_general.GetPreviewImagesCount(self, self.previewInferenceDialogue))
        self.previewInferenceDialogue.exportModelButton.clicked.connect(lambda: ui_pi.ExportModelButton(self))
        self.previewInferenceDialogue.previewPerformanceButton.clicked.connect(lambda: ui_pi.PreviewPerformanceButton(self))
        self.previewInferenceDialogue.cancelButton.clicked.connect(lambda: ui_general.CancelButton(self, self.previewInferenceDialogue))
        self.previewInferenceDialogue.deleteModelsCheckBox.stateChanged.connect(lambda: ui_pi.DeleteModels(self))
        self.previewInferenceDialogue.confidenceThresholdNum.textChanged.connect(lambda thresh: ui_general.UpdateConfThresh(self, self.previewInferenceDialogue, thresh))
        self.previewInferenceDialogue.modelName.textChanged.connect(lambda name: ui_pi.UpdateModelName(self, name))
        self.previewInferenceDialogue.previewImagesNum.textChanged.connect(lambda intString: ui_general.GetPreviewImagesNum(self, intString))

        # Run Inference Dialogue events
        self.runInferenceDialogue.selectTestImagesButton.clicked.connect(lambda dialogue: ui_ri.GetRunImagesCount(self, True))
        self.runInferenceDialogue.runInferenceButton.clicked.connect(lambda: ui_ri.RunInferenceButton(self))
        self.runInferenceDialogue.openReportButton.clicked.connect(lambda: ui_ri.OpenReport(self))
        self.runInferenceDialogue.cancelButton.clicked.connect(lambda: ui_general.CancelButton(self, self.runInferenceDialogue))
        self.runInferenceDialogue.showImagesCheckBox.stateChanged.connect(lambda dialogue: ui_general.ShowImagesCheckBox(self, self.runInferenceDialogue))
        self.runInferenceDialogue.reportCheckBox.stateChanged.connect(lambda: ui_ri.ReportCheckBox(self))
        self.runInferenceDialogue.confidenceThresholdNum.textChanged.connect(lambda thresh: ui_general.UpdateConfThresh(self, self.runInferenceDialogue, thresh))
        self.runInferenceDialogue.previewImagesNum.textChanged.connect(lambda intString: ui_general.GetPreviewImagesNum(self, intString))
        self.runInferenceDialogue.reportTitle.textChanged.connect(lambda newTitle: ui_ri.UpdateReportVariable(self, newTitle))

        # Auto-Annotate Dialogue events
        self.autoAnnotateDialogue.showImagesCheckBox.stateChanged.connect(lambda dialogue: ui_general.ShowImagesCheckBox(self, self.autoAnnotateDialogue))
        self.autoAnnotateDialogue.confidenceThresholdNum.textChanged.connect(lambda thresh: ui_general.UpdateConfThresh(self, self.autoAnnotateDialogue, thresh))
        self.autoAnnotateDialogue.multiClassCheckBox.stateChanged.connect(lambda: ui_aa.MultiClassCheckBox(self))
        self.autoAnnotateDialogue.singleClassName.textChanged.connect(lambda newName: ui_aa.UpdateClassNameVariable(self, newName))
        self.autoAnnotateDialogue.runAnnotationButton.clicked.connect(lambda: ui_aa.RunAnnotationButton(self))
        self.autoAnnotateDialogue.confidenceThresholdNum.textChanged.connect(lambda thresh: ui_general.UpdateConfThresh(self, self.autoAnnotateDialogue, thresh))
        self.autoAnnotateDialogue.cancelButton.clicked.connect(lambda: ui_general.CancelButton(self, self.autoAnnotateDialogue))
        self.autoAnnotateDialogue.editAnnotationsButton.clicked.connect(lambda: ui_aa.OpenLabelImg(self))

        # Main Progress Bar
        self.mainProgressBar.setValue(0)
        self.mainProgressBarMaxValue = 100

        # Dialogues Progress Bars
        self.previewInferenceDialogue.progressBar.setValue(0)
        self.runInferenceDialogue.progressBar.setValue(0)
        self.autoAnnotateDialogue.progressBar.setValue(0)
        self.inferenceProgressBarMaxValue = 100
        self.inferenceProgressBarCount = 0

        # Make cursor invisible
        self.textEdit.setCursorWidth(0)

        # Show U-Infuse main window
        self.show()
        welcomeMsg = "Welcome to U-Infuse"
        self.textEdit.append(welcomeMsg)

    def closeEvent(self, event):
        """
        Override closeEvent to provide a messagebox for when the "X" button is
        clicked.
        """
        exitMessage = QtWidgets.QMessageBox.Yes

        # Check if training is in progress
        if self.trainInProgress:
            exitMessage = QtWidgets.QMessageBox.information(self, "Training in progress", "Training is in progress. Are you sure you would like to exit?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)

        # Exit if training isn't in progress, or "Yes" was chosen in popup message
        if exitMessage == QtWidgets.QMessageBox.Yes:
            event.accept()
            sys.exit()
        else:
            event.ignore()

app = QtWidgets.QApplication(sys.argv)
app.setStyle("Fusion")
Window = UInfuse()
app.exec_()
