"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose:
Class that returns datasets.
"""
import os
import threading

class Datasets(threading.Thread):
    """
    Used to return datasets.
    """
    def __init__(self, modelDir):
        threading.Thread.__init__(self)

        # Variables
        self.modelDir = modelDir
        self.datasets = []
        self.errorMsg = None

    def run(self):
        """
        Interface with get_all_datasets().
        """
        self.datasets = None
        self.errorMsg = None

        # Add directories
        try:
            for root, dirs, files in os.walk(self.modelDir):
                for foundDir in dirs:
                    if self.datasets is None:
                        self.datasets = []
                    self.datasets.append(foundDir)
        except Exception as e:
            self.errorMsg = str(e)
