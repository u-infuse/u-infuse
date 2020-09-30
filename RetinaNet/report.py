"""
Author: Andrew Shepley
Contact: asheple2@une.edu.au
Source: U-Infuse
Purpose: Class for defining and generating inference reports
Methods  
a) __init__
b) about_object_detector
c) sort_empty
d) get_class_distribution
e) get_summary_empty_positive
f) write_detailed_report
g) write_summary_report
h) write_report
"""

import json
from json2table import *

class Report():

    #initialisation variables
    title = "../reports/"
    model_name = ""
    path_to_images = ""
    confidence_threshold = 0

    #processing variables
    processed_images = []

    def __init__(self, title, model_name, path_to_images, confidence_threshold):
        """
        Parameters:
           title: name of report. It will appear in the header and the name of the saved csv file
           model_name: string name of model used for inference
           path_to_images: path to dir containing inference images
           confidence_threshold: all bounding boxes with confidence scores at or above this threshold are included in the report
        """
        self.title = self.title+title
        self.model_name = model_name
        self.path_to_images = path_to_images
        self.confidence_threshold = confidence_threshold

    def about_object_detector(self):
        """
        Function: returns data about the object detector used
        Returns: 
           list containing info on model used, and confidence threshold
        """
        info_object_detector = []
        info_object_detector.append(self.model_name)
        info_object_detector.append(str(self.confidence_threshold)+"%")
        return info_object_detector

    def sort_empty(self):
        """
        Function: sorts empty images (no bounding boxes) from those with detected objects
        Returns:
           empty_images: a list of all image objects containing no bounding boxes
           positive_images: a list of all image objects containing bounding boxes
        """
        empty_images = []
        positive_images = []
        for each_image in self.processed_images:
            if len(each_image.all_detections)==0:
                empty_images.append(each_image)
            else:
                positive_images.append(each_image)
        return empty_images, positive_images

    def get_class_distribution(self):
        """
        Function: determines the class distribution for the entire image dataset
        Returns: 
           a dictionary mapping class names to object count
        """
        class_distribution = dict()
        for each_image in self.processed_images:
            for each_object in each_image.all_detections:
                class_label = each_object[0]
                if class_label in class_distribution:
                    class_distribution[class_label]+=1
                else:
                    class_distribution.update({class_label:1})
        return class_distribution

    def get_summary_empty_positive(self):
        """
        Function: summarises stats re: empty, not empty images
        Returns:
           number of positive images
           number of empty images
           percentage of total images that are empty
           percentage of total images that are positive
        """
        empty_images, positive_images = self.sort_empty()
        num_empty = len(empty_images)
        num_positive = len(positive_images)
        percentage_empty = round((num_empty/(num_empty+num_positive))*100)
        percentage_positive = round((num_positive/(num_empty+num_positive))*100)
        return len(positive_images), len(empty_images), percentage_empty, percentage_positive

    def write_detailed_report(self,positive_images, empty_images):
        """
          Function: write detailed report in JSON format
        """
        detailed_report = {}
        for each_image in positive_images:
            detailed_report[str(each_image.name)]=[]
            for each_object in each_image.all_detections:
                detailed_report[str(each_image.name)].append({
                    'path':str(each_image.path),
                    'class':str(each_object[0]),
                    'confidence':round(((each_object[1]).item())*100,2),
                    'bounding box':[each_object[2][0].item(),each_object[2][1].item(),each_object[2][2].item(),each_object[2][3].item()]
                })
        for each_image in empty_images:
            detailed_report[str(each_image.name)]=[]
            detailed_report[str(each_image.name)].append({
                'path':str(each_image.path)
            })
        with open(self.title+'_detailed_report.json', 'w') as outfile:
            json.dump(detailed_report, outfile, indent=4)
        return 

    def write_summary_report(self):
        """
          Function: write summary report in JSON format
        """
        summary_report = {}
        summary_report[(self.title).split("/")[2]]=[]
        summary_report['About Object Detector']=[]
        summary_report['Object Detection Information']=[]
        summary_report['Class Distribution']=[]
       
        summary_report['About Object Detector'].append({
            'Model': self.about_object_detector()[0],
            'Confidence Threshold': self.about_object_detector()[1]
        })
        positive, empty, percent_empty, percent_pos = self.get_summary_empty_positive()
        class_dist = self.get_class_distribution()
        summary_report['Object Detection Information'].append({
            'Total Images':positive+empty,
            'Positive Images':str(positive)+' ('+str(percent_pos)+'%)',
            'Empty Images':str(empty)+' ('+str(percent_empty)+'%)'
        })
        class_dict = {}
        for each_class in class_dist:
            class_dict.update({str(each_class):str(class_dist[each_class])})

        summary_report['Class Distribution']=[class_dict]

        with open(self.title+'_summary_report.json', 'w') as outfile:
            json.dump(summary_report, outfile, indent=4)
        return
             

    def write_report(self, detailed_report=True, empty_report=True):
        """
        Function: writes the csv report
        Input:
          detailed_report: user sets to true or false. If true, generate the detailed report.
        """
        empty_images, positive_images = self.sort_empty()

        if detailed_report == True:
            self.write_detailed_report(positive_images, empty_images)
        self.write_summary_report()
        if empty_report == True:
            empty = {}
            for each_empty in empty_images:
                empty[str(each_empty.name)]=[]
                empty[str(each_empty.name)].append({
                    'path':str(each_empty.path)
            })
            with open(self.title+'_empty_images.json', 'w') as outfile:
                json.dump(empty, outfile, indent=4)
        

       # with open(self.title+"_empty_images.csv", 'w') as f:
       #     for each_empty in empty_images:
       #         f.write('{}\n'.format(each_empty.name))


            
    def convert_to_html(self,json_file):
        json2table.convert(json_file)
        return 

