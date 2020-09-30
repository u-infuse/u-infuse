"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose:
Class that returns classes.
"""
import threading
from train_main import update_available_classes
import config

class Classes(threading.Thread):
    """
    Used to return classes.
    """
    def __init__(self, selectedDatasets):
        threading.Thread.__init__(self)

        # Variables
        self.selectedDatasets = selectedDatasets
        self.classesList = []
        self.errorMsg = None

    def run(self):
        """
        Interface with update_available_classes().
        """

        # Set variables
        self.classesList = None
        self.errorMsg = None

        # Get class list
        try:
            dataSetDir = config.datasets
            annotationsDir = config.annotations
            self.classesList = update_available_classes(dataSetDir, annotationsDir, self.selectedDatasets)
        except Exception as e:
            self.errorMsg = str(e)
