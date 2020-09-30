"""
Author: Andrew Shepley
Contact: asheple2@une.edu.au
Source: U-Infuse
Purpose: Functions for inference and visualisation
Methods
a) __init__
b) get_classes
c) get_object_count
d) get_average_confidence
e) get_class_distribution
"""


class Inference_Image:

    #initialisation variables
    name = ""
    path = ""
    all_detections = []
    

    def __init__(self, name, path, all_detections):
        """
        Parameters:
           name: name of image
           path: path to inference dir
           all_detections: list of all object labels and confidence scores
        """
        self.name = name
        self.path = path
        self.all_detections = all_detections
    
    def get_classes(self):
        """
        Function: determines nature of objects present in image
        Returns:
           set of classes
        """
        classes = set()
        for each_object in self.all_detections:
            classes.add(each_object[0])
        return classes

    def get_object_count(self):
        """
        Returns: number of objects in the image
        """
        object_count = len(self.all_detections)
        return object_count

    def get_average_confidence(self):
        """
        Function: used to gauge average detector confidence in classification labels
        Returns the average confidence of all objects in the image
        """
        average_confidence = 0
        sum_confidence=0
        for each_object in self.all_detections:
            sum_confidence+=each_object[1]
        if self.get_object_count()==0:
            return 
        average_confidence = sum_confidence/(self.get_object_count())
        return average_confidence

    def get_class_distribution(self):
        """
        Function: determines distribution of objects in the image
        Returns: dictionary containing mapping of class names to number of objects
        """
        class_distribution = dict()
        for each_object in self.all_detections:
            class_label = each_object[0]
            if class_label in class_distribution:
                class_distribution[class_label]+=1
            else:
                class_distribution.update({class_label:1})
        return class_distribution

