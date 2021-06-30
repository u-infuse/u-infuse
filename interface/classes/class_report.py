"""
Author: Chris Lawson
Contact: clawso21@une.edu.au
Source: U-Infuse
Purpose: Class interfaces with the report class.
"""
import threading
import os
from pathlib import Path
from report import Report
from inference_image import Inference_Image

class ReportInterface(threading.Thread):
    """
    Used to generate report.
    """
    def __init__(self, reportTitle, modelName, imgDir, confThresh, imgData):
        threading.Thread.__init__(self)
        self.reportTitle = reportTitle
        self.modelName = modelName
        self.imgDir = imgDir
        self.confThresh = confThresh
        self.imgData = imgData
        self.errors = []

    def run(self):
        """
        Generates report.
        """
        report = None
        self.errors = []

        # Instantiate report object
        try:
            report = Report(self.reportTitle, self.modelName, self.imgDir, self.confThresh)

            # Remove previous images if they exist in processed_images list in reporty.py
            if len(report.processed_images) > 0:
                report.processed_images = []
        except Exception as e:
            self.errors.append(str(e))

        # Loop through previously processed images.
        try:
            for data in self.imgData:
                # Get inferred image
                imgPath = os.path.join(self.imgDir, data[2])

                # Change imgPath for Windows
                if os.name == "nt":
                    imgPath = Path(self.imgDir) / data[2]

                objData = data[1]
                inferredImage = Inference_Image(data[2], imgPath, objData)

                # Add inferred image to report object
                report.processed_images.append(inferredImage)
        except Exception as e:
            self.errors.append(str(e))

        # Generate summary report
        try:
            report.write_summary_report()
        except Exception as e:
            self.errors.append(str(e))

        # Generate report
        try:
            report.write_report()
        except Exception as e:
            self.errors.append(str(e))
