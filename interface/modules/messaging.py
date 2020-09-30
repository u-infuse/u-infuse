"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: Messaging functions for the GUI.
"""

def BannedWords(output):
    """
    Remove output that contains words and phrases that should not be printed.
    """
    # Variables
    bannedWords = ["UserWarning", "Parsing annotations"]

    try:
        for bWord in bannedWords:
            if bWord in newOutput:
                output = ""
                break
    except Exception:
        pass

    return output

def PreprocessOutput(output):
    """
    Preprocesses train.py output.
    """
    deleteLast = False

    try:
        # Skip if output is empty
        if output != "":
            # Preprocess output - First step
            if "ETA: " in output:
                # Remove TensorFlow out of memory error
                if "out of memory" in output:
                    if " 1/" in output:
                        output = "\n"
                    else:
                        output = ""
                else:
                    tempOutput = output.split("[")
                    output = "STEP1[" + tempOutput[1]
                    if " 1/" not in tempOutput[0]:
                        deleteLast = True

                    # Remove newlines, trailing spaces
                    output = output.replace("\n", "")
                    output = output.strip()

            # Preprocess output - Running network
            if "Running network" in output:
                if "(2 of" in output:
                    tempOutput = output.replace("ETA:  ", "ETA: ")
                    tempOutput = tempOutput.split("|")
                    output = "RN1Running Network" + tempOutput[2]

            # Change classification_loss to classification loss
            if "classification_loss" in output:
                output = output.replace("classification_loss", "classification loss")

            # Change regression_loss to regression loss
            if "regression_loss" in output:
                output = output.replace("regression_loss", "regression loss")
    except Exception:
        pass

    return output, deleteLast

def KeywordChange(output):
    """
    Changes output.
    """
    # Variables
    newOutput = None

    try:
        # Change output if it is not blank
        if output != "":
            # Add message about CPU training
            if "cudart64_101.dll not found" in output:
                newOutput = "You are currently training on CPU. Training on CPU is very slow and does not result in optimal learning. For best results, train only on a system with GPU.\n"

            # Change ReduceLROnPlateau on message
            if newOutput is None:
                if "ReduceLROnPlateau" in output:
                    newOutput =  output.replace("ReduceLROnPlateau", "Reduce Learning Rate on Plateau. You may now terminate training: ")

            # Remove step keyword
            if newOutput is None:
                if "STEP1" in output:
                    newOutput = output.replace("STEP1", "")

            # Print epoch message
            if newOutput is None:
                if "Epoch" in output:
                    newOutput = output

            # Remove RN1 keyword
            if newOutput is None:
                if "RN1" in output:
                    newOutput = output.replace("RN1", "")

            # Print mAP message
            if newOutput is None:
                if "mAP" in output:
                    newOutput = output

            # Print average precision message
            if newOutput is None:
                if "average precision" in output:
                    newOutput = output

            # Print "Unable to open file" error message
            if newOutput is None:
                if "Unable to open file" in output:
                    newOutput = "The pretrained model you have chosen is incompatible with training. Please select a different model and try again.\n"

            # Print training failed message
            if newOutput is None:
                if "Failed" in output:
                    newOutput = output

            # Print "FileNotFoundError" error message
            if newOutput is None:
                if "FileNotFoundError" in output:
                    newOutput = output
    except Exception:
        pass

    return newOutput
