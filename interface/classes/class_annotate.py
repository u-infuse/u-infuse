"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: Class interfaces with the auto-annotate class.
"""
import threading
from auto_annotation import RetinaNet_Auto_Annotator

class AnnotateImage(threading.Thread):
    """
    Used to annotate images.
    """
    def __init__(self, imgDir, confThresh):
        threading.Thread.__init__(self)
        self.imgDir = imgDir
        self.confThresh = confThresh
        self.errors = []

    def run(self):
        """
        Clear variables.
        """
        self.errors = []

    def CreateXML(self, imgName, objData, imgDims):
        """
        Creates an RetinaNet_Auto_Annotator class object and the annotation file
        for the image.
        """
        imgObj = None

        try:
            imgObj = RetinaNet_Auto_Annotator(self.imgDir, imgName, objData, imgDims, self.confThresh)
        except Exception as e:
            errorMsg = "There was an error with auto_annotation.RetinaNet_Auto_Annotator(): " + str(e)
            self.errors.append(errorMsg)

        try:
            imgObj.write_xml_file()
        except Exception as e:
            errorMsg = "There was an error with auto_annotation.write_xml_file(): " + str(e)
            self.errors.append(errorMsg)

    def ReturnErrors(self):
        """
        Return error messages.
        """
        errors = None
        if len(self.errors) > 0:
            errors = self.errors
            self.errors = []

        return errors
