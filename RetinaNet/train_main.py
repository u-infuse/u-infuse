"""
Author: Andrew Shepley
Contact: asheple2@une.edu.au
Source: U-Infuse
Purpose: 
a) Calls functions in preprocessing.py to generate all required training and validation scripts.
b) Allows users to set training parameters

Contains functions:
a) generate_training_scripts()
b) set_training_parameters()
c) calculate_num_steps()
d) update_available_classes()
e) get_num_training_samples()
"""

from preprocessing import *
import os

#USER CONTROLLED PARAMETERS ------------------------------------------

#datasets selected by the user for inclusion, e.g. ['cat', 'dog', 'infuse_cat']. Link to folders selected by user in dropdown list.
chosen_datasets = []
#classes selected by the user for inclusion, e.g. ['cat', 'dog']. Link to classes selected by user from dropdown list (combobox)
chosen_classes = set()

#user can choose to use the datasets not added for training to negative sampling instead. Default is true. Link to checkbox.
use_negatives = True

#DEFAULT DIR STRUCTURE
#datasets_dir = './datasets/'
#annotations_dir = './annotations/'

def generate_training_scripts(chosen_datasets, chosen_classes, use_negatives, negative_folders):
    """
    Parameters:
       chosen_datasets: list of datasets chosen by user for inclusion in training
       chosen_classes: set of classes chosen by user for inclusion in training
       use_negatives: flag to include/not include negatives in training
    """
    #training/validation scripts used by retinanet during training
    TRAINING_FILE = 'training.csv'
    VALIDATION_FILE = 'validation.csv'
    CLASSES_FILE = 'classes.csv'
    
    #DEFAULT DIR STRUCTURE
    datasets_dir = '../datasets/'
    annotations_dir = '../annotations/'


    #10% of images are used for validation during training
    validation_split = 0.1

    #Function calls .... processing

    #all datasets available in ../datasets/
    all_datasets = get_all_datasets(datasets_dir)
    all_classes = set()
    all_train_annotations = []
    all_val_annotations = []
    chosen_dataset_negatives = []

    #extract annotations and class names for each chosen dataset/class
    for each_dataset in chosen_datasets:
        annotation_path = annotations_dir+each_dataset+'/'
        dataset_path = datasets_dir+each_dataset+'/'
        #list of images in the current folder which contain at least one instance of at least one chosen class
        positives, negatives = locate_all_positive_images(dataset_path, annotation_path, chosen_classes)
        for each_neg in negatives:
            chosen_dataset_negatives.append(dataset_path+each_neg)

        all_classes, all_train_annotations,all_val_annotations = add_to_annotations(positives, chosen_classes, annotation_path, dataset_path, validation_split, all_classes, all_train_annotations, all_val_annotations)
        #print(all_train_annotations)

    #prepare annotations for writing to csv
    all_train_annotations = combine_annotations(all_train_annotations)
    all_val_annotations = combine_annotations(all_val_annotations) 

    #if user ticks the checkbox (default is True)
    if use_negatives is True:
        negatives_folders = negative_folders#get_all_negatives(all_datasets, chosen_datasets)
        add_neg_to_train(negatives_folders, chosen_dataset_negatives, datasets_dir, all_train_annotations)

    #shuffles all the training annotations to randomise training.
    shuffled_train_annotations = shuffle_annotations(all_train_annotations)

    #write training and validation csv files to ./
    write_annotation_file(TRAINING_FILE, shuffled_train_annotations)
    write_annotation_file(VALIDATION_FILE, all_val_annotations)
    write_class_file(CLASSES_FILE, all_classes)
    print("check ./ for training.csv, validation.csv and classes.csv")
    return 


def set_training_parameters(pretrained_model='pretrained_COCO.h5', BATCH_SIZE=2, EPOCHS = 30):
    """
    Parameters:
       pretrained_model: used as the backbone for transfer learning. Default is pretrained_COCO.h5. Link this to a dropdown list in Training Configuration.
       BATCH_SIZE: Users should be able to change this - lower batch size is better for smaller GPU. Greater value for batch size is useful if using a large GPU. Enable users to set this via a textbox in Training Configuration.
       EPOCHS: This determines how long training will go for. Preset to 30. Enable users to change via textbox in Training Configuration.
    Returns: 
    These values are required input for RetinaNet training. Interface this method with 'Train' button.
       PRETRAINED_MODEL
       BATCH_SIZE
       STEPS
       EPOCHS
    """
    PRETRAINED_MODEL = './pretrained_models/'+pretrained_model
    SNAPSHOTS = './snapshots/'
    TRAINING = './training.csv'
    VALIDATION = './validation.csv'
    CLASSES = './classes.csv'

    num_training_samples = get_num_training_samples(TRAINING) 
    STEPS = calculate_num_steps(BATCH_SIZE, TRAINING)
    return PRETRAINED_MODEL, BATCH_SIZE, STEPS, EPOCHS

def calculate_num_steps(batch_size, TRAINING):
    num_training_samples = get_num_training_samples(TRAINING)
    STEPS = round((num_training_samples)/batch_size)
    return STEPS

def update_available_classes(datasets_dir, annotations_dir, selected_datasets):
    """
    Purpose: Link this to the combobox to populate the available classes. Call this function every time a user clicks on it the dropdown list, and everytime the program loads. 
    Parameters: 
       datasets_dir: ../datasets/
       annotations_dir: ../annotations/
       selected_datasets: list of folders selected by user
    Returns: 
       set of all classes corresponding with chosen datasets
    """
    available_classes = set()
    for each_dataset in selected_datasets:
        images = datasets_dir+each_dataset+'/'
        annotations = annotations_dir+each_dataset+'/'
        classes = get_all_classes(annotations, images)
        available_classes.update(classes)
    return available_classes        
 

def get_num_training_samples(TRAINING):
    """
    Parameters:
       TRAINING: file containing annotations for training
    Returns:
       num_lines: number of training samples (bounding boxes + negatives)
    """
    num_lines = 0
    with open(TRAINING, 'r') as f:
        for line in f:
            num_lines+=1
    return num_lines
