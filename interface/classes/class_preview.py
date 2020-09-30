"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: Class interfaces with preview_performance function.
"""
import threading
import sys
import interface_inference

class PreviewImages(threading.Thread):
    """
    Used to get preview images.
    """
    def __init__(self, imgDir, modelName, mapName, modelDir, confThresh, imgTotal):
        threading.Thread.__init__(self)
        self.imgDir = imgDir
        self.modelName = modelName
        self.mapName = mapName
        self.modelDir = modelDir
        self.confThresh = confThresh
        self.imgTotal = imgTotal
        self.previewImages = []
        self.processedImages = []
        self.errors = []
        self.exit = False

    def run(self):
        """
        Retrieves preview images list.
        """
        imageList = []
        convertedModel = None
        error = False

        # Reset variables
        self.previewImages = []
        self.processedImages = []
        self.errors = []
        self.exit = False

        # Get list of image file names
        imageList = interface_inference.GetPreviewImageNames(self.imgDir, self.imgTotal)

        # Convert model
        convertedModel = interface_inference.ConvertModel(self.modelDir, self.modelName)

        # Process images individually
        try:
            for imgName in imageList:
                # Exit if cancelled
                if self.exit:
                    sys.exit()

                # Process image
                error = False
                img, objData, errorMsg = interface_inference.PreviewPerformance(self.imgDir, convertedModel, imgName, self.mapName, self.confThresh)

                # Append error messages
                if errorMsg is not None:
                    error = True
                    self.errors.append(errorMsg)

                # Create data list
                imgData = [img, objData, imgName, error, self.imgDir]

                # Append image data
                self.previewImages.append(imgData)

        except Exception as e:
            errorMsg = ("There was an error with model inference testing: " + str(e))
            self.errors.append(errorMsg)

        # Indicate adding images to list has finished
        self.previewImages.append(None)

    def ProcessedImages(self):
        """
        Returns list of processed images and data.
        """
        return self.processedImages

    def GetErrors(self):
        """
        Retrieves error list.
        """
        errors = self.errors
        self.errors = []

        return errors

    def CloseThread(self):
        """
        Closes the thread.
        """
        self.exit = True
