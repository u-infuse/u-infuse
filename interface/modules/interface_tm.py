"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: Module interfaces with train_main.
"""
from train_main import generate_training_scripts, set_training_parameters

def TrainingParameters(pretrainedModelIn, batchSizeIn, epochsIn):
    """
    Returns training parrameters.
    """
    error = False
    errorMsg = ""
    pretrainedModel = ""
    batchSize = 0
    steps = 0
    epochs = 0

    try:
        pretrainedModel, batchSize, steps, epochs = set_training_parameters(pretrainedModelIn, batchSizeIn, epochsIn)
    except Exception as e:
        error = True
        errorMsg = str(e)

    return pretrainedModel, batchSize, steps, epochs, error, errorMsg

def GenerateScripts(chosenDataSets, chosenClasses, negative, negativeChosenDataSets):
    """
    Used to called generate_training_scripts()
    """
    errorMsg = None
    setChosenClasses = set(chosenClasses)

    # Call generate_training_scripts()
    try:
        generate_training_scripts(chosenDataSets, setChosenClasses, negative, negativeChosenDataSets)
    except Exception as e:
        errorMsg = str(e)

    return errorMsg
