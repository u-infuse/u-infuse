"""
Author: Andrew Shepley
Contact: asheple2@une.edu.au
Source: U-Infuse
Purpose: Functions for inference and visualisation
Methods
a) __init__
b) prettify
c) get_labels_boxes
d) create_annotations_dir
e) write_xml_file
"""

from xml.etree import ElementTree
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
from xml.dom import minidom
import os

class RetinaNet_Auto_Annotator():

    #class variables
    dataset_dir = ""
    image_name = ""
    image_dims = []
    annotation_path = "../annotations/"
    confidence_threshold = 0.5
    object_detection_data = []

    def __init__(self, dataset_dir, image_name, object_detection_data, image_dims, confidence_threshold):
        """
        Parameters:
           dataset_dir: dir containing image to annotate
           image_name: name of image
           object_detection_data: annotation info; class label, scores, bounding box (list)
           image_dims: width, height, channels (list)
           confidence_threshold: user preset conf. threshold
        """
        self.dataset_dir = dataset_dir
        self.image_name = image_name
        self.object_detection_data = object_detection_data
        self.image_dims = image_dims
        self.confidence_threshold

    def get_labels_boxes(self):
        """
        Function: returns list of class labels with associated bounding boxes
        """
        boxes = []
        labels = []
        for each in self.object_detection_data:
            labels.append(each[0])
            boxes.append(each[2].tolist())
        return boxes, labels

    def create_annotations_dir(self, folder):
        """
        Parameters: 
          folder: name of folder containing images
        Function: if the annotations_dir doesn't exist, create it
        """
        annotations_dir = os.path.join('../annotations/',folder)
        if os.path.exists(annotations_dir) is False:
            os.mkdir(annotations_dir)
        return

    def prettify(self, elem):
        """
        Function: Return a pretty-printed XML string
        """
        rough_string = ElementTree.tostring(elem, 'utf-8')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")

    def write_xml_file(self):
        """
        Function: writes xml annotation file for image 
        """
        boxes, labels = self.get_labels_boxes()
        folder_name = self.dataset_dir.split("/")[2]
        self.create_annotations_dir(folder_name)

        root = Element( 'annotation' )
        folder = SubElement( root, 'folder' )
        folder.text = folder_name
        filename = SubElement(root, 'filename')
        filename.text = self.image_name
        path = SubElement(root, 'path')
        path.text = self.dataset_dir
        source = SubElement(root, 'source')
        database = SubElement(source, 'database')
        database.text = 'U-Infuse FlickR'
    
        size = SubElement(root, 'size')
        width = SubElement(size, 'width')
        width.text = str(self.image_dims[1])
        height = SubElement(size, 'height')
        height.text = str(self.image_dims[0])
        depth = SubElement(size, 'depth')
        depth.text = str(self.image_dims[2])    
        segmented = SubElement(root, 'segmented')
        segmented.text = str(0)

        for b, each_label in zip(boxes, labels):
            object_ = SubElement(root, 'object')
            name_ = SubElement(object_, 'name')
            name_.text = each_label
            pose = SubElement(object_, 'pose')
            pose.text = 'Unspecified'
            truncated = SubElement(object_, 'truncated')
            truncated.text = '0'
            difficult = SubElement(object_, 'difficult')
            difficult.text = '0'
            bndbox = SubElement(object_, 'bndbox')
            xmin= SubElement(bndbox, 'xmin')
            xmin.text = str(b[0])
            ymin= SubElement(bndbox, 'ymin')
            ymin.text = str(b[1])
            xmax= SubElement(bndbox, 'xmax')
            xmax.text = str(b[2])
            ymax= SubElement(bndbox, 'ymax')
            ymax.text = str(b[3])

        output_file = open(self.annotation_path+folder_name+"/"+self.image_name[:-4]+'.xml', 'w' )
        output_file.write(self.prettify(root))
    
        output_file.close()
        return 


