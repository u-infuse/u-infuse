"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose:
Class interface for the trian.py file used to train RetinaNet models.
"""
import threading
import subprocess
import sys
import io
import config

class RetinaNetTrain(threading.Thread):
    """
    Used to train RetinaNet models.
    """
    def __init__(self, snapshots, pretrainedModel, batchSize, steps, epochs):
        threading.Thread.__init__(self)

        # Variables
        self.snapshots = snapshots
        self.pretrainedModel = pretrainedModel
        self.batchSize = batchSize
        self.steps = steps
        self.epochs = epochs
        self.error = []
        self.output = []
        self.exit = False

    def run(self):
        """
        Train RetinaNet model.
        """
        self.output = []
        self.exit = False

        # Pipe command to terminal
        try:
            p = None

            # Change location if frozen
            if getattr(sys, 'frozen', False):
                p = subprocess.Popen(["retinanet", "--freeze-backbone", "--snapshot-path", self.snapshots, "--weights", self.pretrainedModel, "--random-transform", "--batch-size", str(self.batchSize), "--steps", str(self.steps), "--epochs", str(self.epochs), "csv", config.trainCSV, config.classesCSV, "--val-annotations", config.valCSV], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)
            else:
                p = subprocess.Popen([config.pythonName, config.retinaNet, "--freeze-backbone", "--snapshot-path", self.snapshots, "--weights", self.pretrainedModel, "--random-transform", "--batch-size", str(self.batchSize), "--steps", str(self.steps), "--epochs", str(self.epochs), "csv", config.trainCSV, config.classesCSV, "--val-annotations", config.valCSV], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=False)

            # Get output from terminal
            for line in io.TextIOWrapper(p.stdout, encoding="utf-8"):
                try:
                    # Exit thread if training is cancelled
                    if self.exit:
                        p.terminate()
                        sys.exit()
                    else:
                        # Append output string, if valid
                        if isinstance(line, str):
                            self.output.append(line)

                except Exception as e:
                    self.error.append(str(e))

        except Exception as e:
            self.error.append(str(e))

        # Indicate thread has finished
        self.exit = True
        sys.exit()

    def CloseThread(self):
        """
        Closes the thread.
        """
        self.exit = True
