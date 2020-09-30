"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose:
Class that generates training scripts.
"""
import threading
import interface_tm

class Generate(threading.Thread):
    """
    Used to generate training scripts.
    """
    def __init__(self, chosenDataSets, chosenClasses, negative, negativeChosenDataSets):
        threading.Thread.__init__(self)

        # Variables
        self.chosenDataSets = chosenDataSets
        self.negativeChosenDataSets = negativeChosenDataSets
        self.chosenClasses = chosenClasses
        self.negative = negative
        self.errorMsg = []

    def run(self):
        """
        Interface with get_all_datasets().
        """
        self.errorMsg = []
        negativeChosenDataSets = self.negativeChosenDataSets

        # Send across no negaive classes if negative option is False
        if self.negative is False:
            negativeChosenDataSets = []

        # Call generate_training_scripts()
        errorMsg = interface_tm.GenerateScripts(self.chosenDataSets, self.chosenClasses, self.negative, negativeChosenDataSets)

        self.errorMsg.append(errorMsg)
