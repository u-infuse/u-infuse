"""
Author: Andrew Shepley
Contact: asheple2@une.edu.au
Source: U-Infuse
Purpose: Pre-process image/annotation data for U-Infuse RetinaNet implementation elegantly!
Methods  
a) extract_annotations
b) get_negative_reference
c) get_negatives
d) separate_train_valid
e) get_image_annotations
f) locate_all_positive_images
g) shuffle_annotations
h) combine_annotations
i) get_all_datasets
j) get_all_negatives
k) add_neg_to_train
l) add_to_annotations
m) get_all_classes
n) write_annotation_file
o) write_class_file
p) get_all_files
q) get_all_pretrained_models
"""

import random
import os
import urllib
import xml.etree.ElementTree as ET
import numpy as np
import csv
from pathlib import Path

def convert_to_jpg(directory, image_to_convert):
    """
    Function to convert image extension to jpg
    Parameters:
       image_to_convert: name in form name.extension, e.g.  image.jpeg
    """
    extension = '.jpg'
    print(image_to_convert)
    split_im = image_to_convert.split('.')
    image_name = split_im[0]
    print(image_name)
    jpg_image = directory+image_name+extension
    os.rename(directory+image_to_convert, jpg_image)
    return



def extract_annotations(chosen_classes, annotations_dir, dataset_dir, val_set, train_set):
    """Function to convert PASCAL xml annotations into input for csv files used for training
    Parameters: 
        chosen_classes: set of classes chosen by user
        annotations_dir: Path for directory containing PASCAL xml annotations
        dataset_dir: Path for directory containing images
        val_set: List of images assigned for validation
        train_set: List of images assigned for training
    Returns:
        anntations_train: List of annotations used for training in form path, filename, x1, y1, x2, y2, classname
        annotations_val: List of annotations used for validation in form path, filename, x1, y1, x2, y2, classname
        class_names: Set of class names contained in both validation and training sets. Used for label map.
    """ 
    extension = ''
    annotations_train = []
    annotations_val = []
    class_names = set()
    for xml_file in [f for f in os.listdir(annotations_dir) if f.endswith(".xml")]:
        tree = ET.parse(os.path.join(annotations_dir, xml_file))
        root = tree.getroot()
        file_name = None
        image = xml_file[:-3]    
        extension = [image_file for image_file in os.listdir(dataset_dir) if image_file.split('.')[0]==image[:-1]][0].split('.')[1]
        
        if os.path.exists(dataset_dir + image+extension):
            for elem in root:
                if elem.tag == 'filename':
                    file_name = os.path.join(dataset_dir, image+extension)
                if elem.tag == 'object':
                    obj_name = None
                    coords = []
                for subelem in elem:
                    if subelem.tag == 'name':
                        obj_name = subelem.text     
                    if subelem.tag == 'bndbox':
                        for subsubelem in subelem:
                            coords.append(subsubelem.text)
                        item = [file_name] + coords + [obj_name]
                        if obj_name in chosen_classes:
                            class_names.add(obj_name)
                            if xml_file in val_set:
                                annotations_val.append(item)
                            elif xml_file in train_set:
                                annotations_train.append(item)
    return annotations_train, annotations_val, class_names

def get_negative_reference(path_to_image):
    """
    Parameters:
       path_to_image: path to a negative image
    Returns:
       item: line to be written to training file
    """
    item=[path_to_image]+["","" , "","" ,""]
    return item 

def get_negatives(directory):
    """Generates negative sample references for training.
    Parameters:
       directory containing negative samples
    Returns: 
       negatives: List of negative sample references in the form path, filename, "","","","",""
    """
    negatives = []
    filenames=next(os.walk(directory))[2]
    for each in filenames:
        negatives.append(get_negative_reference(directory+each))
    return negatives


def separate_train_valid(positives,  validation_split):
    """Seperates training and validation images by reference
    Parameters: 
       positives: list of xml files containing positive annotations
       validation_split: decimal value representing the percentage of images to retain for validation
    Returns:
       val_set: randomly selected validation set
       shuffled_positives: training set (shuffled)
    """
    val_set = []
    shuffled_positives = shuffle_annotations(positives)
    upper = int(round(len(shuffled_positives)*validation_split))
    subset = shuffled_positives[0:upper]
    for each in subset:
        val_set.append(each)
        shuffled_positives.remove(each)
    return val_set, shuffled_positives

def get_image_annotations(datasets_dir, annotations_dir, xml_file):
    """
    Parameters:
       datasets_dir: path to dir containing image file
       annotations_dir: path to dir containing xml file
       xml_file: name of xml file
    Returns:
       class_names: any class name contained in xml file
    """
    image = xml_file[:-3]  
    extension = [image_file for image_file in os.listdir(datasets_dir) if image_file.split('.')[0]==image[:-1]][0].split('.')[1]
    class_names = set()
    if os.path.exists(datasets_dir + image+extension) and os.path.exists(annotations_dir+xml_file):
        
        tree = ET.parse(os.path.join(annotations_dir, xml_file))
        root = tree.getroot()
        
        for elem in root:
            if elem.tag == 'object':
                obj_name = None
            for subelem in elem:
                if subelem.tag == 'name':
                    obj_name = subelem.text
                if subelem.tag == 'bndbox':
                    class_names.add(obj_name)
    return class_names

def locate_all_positive_images(dataset_path, annotation_path, chosen_classes):
    """
    Parameters:
       dataset_path: ../datasets/folder
       annotation_path: ../annotations/folder
       chosen_classes: set of classes chosen by user
    Returns:
       list of xml files containing positive annotations
       list of images used for negative sampling
    """
    positive_images = []
    negative_images = []
    for image in os.listdir(dataset_path):
        xml_file = image[:-4]+'.xml'
        classes = get_image_annotations(dataset_path, annotation_path, xml_file)
        subset = chosen_classes.intersection(classes)
        if len(subset)>0:
            positive_images.append(xml_file)
        else:
            negative_images.append(image)
    return positive_images, negative_images


def shuffle_annotations(annotations):
    """Shuffles order of annotations before writing them to csv.
       Parameters: 
          annotations: List containing annotations
       Returns:
          shuffled_annotations: List containing all annotations in 'annotations'. Order of annotations is shuffled to improve learning.
    """
    shuffled_annotations = []
    while len(annotations)>0:
        random_index = random.randrange(len(annotations))
        line = annotations[random_index]
        shuffled_annotations.append(line)
        annotations.remove(line)
    return shuffled_annotations

def combine_annotations(annotations):
    """Prepares annotations for writing to csv file. Combines all annotations into one list of lists.
    Parameter: 
       annotations: a list of lists of lists
    Returns:
       combined_annotations: a list of lists, where is list is an annotations
    """
    combined_annotations = []
    for each_folder in annotations:
        for each_object in each_folder:
            combined_annotations.append(each_object)
    return combined_annotations

def get_all_pretrained_models(files_dir):
    """
    Parameter: 
       files_dir: path to directory containing .h5 files
    Returns:
       list of h5 files 
    """
    all_files=[]
    for each_file in os.listdir(files_dir):
        if each_file[-3:]=='.h5':
            all_files.append(each_file)
    return all_files
        

def get_all_datasets(datasets_dir):
    """
    Parameter: 
       datasets_dir: path to directory of folders (all users options)
    Returns:
       list of folders 
    """
    all_datasets = []
    for each_dataset in os.listdir(datasets_dir):
        if(os.path.isdir(os.path.join(datasets_dir,each_dataset))):
            all_datasets.append(each_dataset)
    return all_datasets

def get_all_files(directory, chosen_extension):
    """
    Parameter: 
       directory: dir path containing iterable files
       chosen_extension: desired file extension
    Returns:
       all_files: list of files
    """
    all_files = []
    for each_file in os.listdir(directory):
        if os.path.isdir(os.path.join(directory,each_file)) == False:
            extension = each_file.split(".")[1]
            if extension == chosen_extension:
                all_files.append(each_file)
    return all_files


def get_all_negatives(all_datasets, chosen_datasets):
    """
    Parameters:
       all_datasets: list of available folder
       chosen_datasets: list of folders chosen for training
    Returns:
       negatives: list of folders not chosen for training
    """
    negatives = []
    for each_dataset in all_datasets:
        if each_dataset not in chosen_datasets:
            negatives.append(each_dataset)   
    return negatives

def add_neg_to_train(negatives, chosen_folders_negatives, datasets_dir, all_train_annotations):
    """
    Parameters: 
       negatives: list of folders not used in training
       chosen_folders_negatives: list of references to images contained in training folders, that don't include positive annotations
       datasets_dir: path to directory of folders
       all_train_annotations: list of training  annotations (positive samples)
    Returns:
       all_train_annotations: list of combined positive and negative annotations
    """
    for each_negative in chosen_folders_negatives:
       all_train_annotations.append(get_negative_reference(each_negative))
    for each_negative_folder in negatives:
        for each_negatives in get_negatives(datasets_dir+each_negative_folder+'/'):
            all_train_annotations.append(each_negatives)
    return all_train_annotations


def add_to_annotations(positives, chosen_classes, annotation_path, dataset_path, validation_split, all_classes, all_train_annotations, all_val_annotations):
    """
    Parameters: 
      positives: all images with annotations belonging to classes in chosen_classes
      chosen_classes: all classes chosen by user
      annotation_path: path to directory of annotations
      dataset_path: path to directory of images
      validation_split: number between 0-1 representing percentage of images to use for validation
      all_classes: set of all classes contained in all processed annotations
      all_train_annotations: list of all training annotations
      all_val_annotations: list of all validation annotations
    Returns:
      all_classes: set of classes 
      all_train_annotations: list of all training annotations
      all_val_annotations: list of all validation annotations
    """
    val_set, train_set = separate_train_valid(positives, validation_split)
    train_annotations, val_annotations, class_names = extract_annotations(chosen_classes, annotation_path, dataset_path, val_set, train_set)
    for each_class in class_names:
        all_classes.add(each_class)
        
    all_train_annotations.append(train_annotations)
    all_val_annotations.append(val_annotations)
    return all_classes, all_train_annotations,all_val_annotations 



def get_all_classes(annotations_dir, datasets_dir):
    """
    Parameters:
       annotations_dir: path for dir containing xml files
       datasets_dir: path for dir containing corresponding jpg files 
    Returns:
       class_names: all annotated classes in this dir
    """
    class_names=set()
    if os.path.exists(annotations_dir)==False:
        print("No annotations have been provided for images located at ", datasets_dir,". To train on these images, please provide annotations at ",annotations_dir)
    else:
        for xml_file in [f for f in os.listdir(annotations_dir) if f.endswith(".xml")]:
            classes = get_image_annotations(datasets_dir, annotations_dir, xml_file)
            class_names.update(classes)
    return class_names


def write_annotation_file(FILENAME, annotations):
    """
    Parameters:
       FILENAME: path to csv file where annotations will be saved
       annotations: annotations to be written to the file
    """
    with open(FILENAME, 'w') as f:
        for each_line in annotations:
            f.write('{},{},{},{},{},{}\n'.format(each_line[0],each_line[1],each_line[2],each_line[3],each_line[4],each_line[5]))
    return 
    
def write_class_file(CLASSES_FILE, classes):
    """
    Parameters:
       CLASSES_FILE: path to csv file where class mapping will be saved
       classes: set of classes contained in all annotations
    """
    with open(CLASSES_FILE, 'w') as f:
        for i, line in enumerate(classes):
            f.write('{},{}\n'.format(line,i))
    return
