"""
Author: Andrew Shepley
Contact: asheple2@une.edu.au
Source: U-Infuse
Purpose: Functions for inference and visualisation
Methods  
a) run_inference
b) preview_performance
c) generate_list_of_images
d) run_inference_on_image
e) prepare_image
f) run_model_on_image
g) set_confidence_threshold
h) draw_labelled_box
i) get_label_color
j) choose_inference_model
k) int_to_label
l) get_session
m) draw_boxes
n) draw_caption
o) export_model
p) delete_suboptimal_models
q) preview_performance_one_image
r) get_preview_images
s) draw_image_name
"""

import cv2
import tensorflow as tf
import keras
from keras_retinanet import models
from keras_retinanet.utils.image import *
from keras_retinanet.utils.colors import *
from keras_retinanet.utils.visualization import *
import os
import random
import matplotlib.pyplot as plt
import numpy as np
import shutil



def get_preview_images(inference_dir, num_preview_images):
    """
    Function: GUI Preview Model window
    Parameters:
       inference_dir: path to dir containing inference images
       num_preview_images: number of images user chooses to preview model 
    Returns:
       random_images: list of randomly selected images chosen from those contained in inference_dir. List length = num_preview_images.
    """
    list_of_images = generate_list_of_images(inference_dir)
    random_images = []
    index_pos = set()
    while len(index_pos)<num_preview_images:
        random_index = random.randrange(len(list_of_images))
        index_pos.add(random_index)
    for i in index_pos:
        random_image = list_of_images[i]
        random_images.append(random_image)
    return random_images

def inference_per_image(inference_dir, model, image, class_mapping_file, confidence_threshold):
    """
    Function: GUI Preview Model window
    Parameters:
       inference_dir: path to dir containing inference images
       model: converted h5 file
       image: single image on which to run inference
       class_mapping_file: use ./classes.csv when running preview model, but use relevant class mapping file when running inference
       confidence threshold: only draw boxes with conf above 50%
    Returns:
       visualisation_images[0]: a np image after inference has been performed
       object_detection_data: classes and scores for boxes in inferred image
    """
    image_list = []
    image_list.append(image)
    visualisation_images, object_detection_data = run_inference_on_images(inference_dir, image_list, model, confidence_threshold, class_mapping_file)
    return visualisation_images[0], object_detection_data
    
def generate_list_of_images(inference_dir):
    """
    Parameters:
       inference_dir: path to dir containing inference images
    Returns:
       list_images: list of all names of .jpg files in inference_dir
    """
    list_images = []
    for each_image in os.listdir(inference_dir):
        list_images.append(each_image)
    return list_images

def run_inference_on_images(inference_dir, list_of_images, model, confidence_threshold, class_mapping_file):
    """
    Parameters:
       inference_dir: path to dir containing inference images
       list_of_images: list of all names of .jpg files in inference_dir
       model: convert h5 file
       confidence threshold: only draw boxes with conf above 50%
       class_mapping_file: csv file mapping int values to names
    Return:
       images_to_draw: numpy array of images showing bounding boxes and labels
       object_detection_data: list of classes and confidence scores
    """
    images_to_draw = []
    class_mapping = int_to_label(class_mapping_file)
    
    for each_image in list_of_images:
        object_detection_data = []
        model_image, visualisation_image = prepare_image(inference_dir, each_image)
        boxes, scores, labels = run_model_on_image(model_image, model)
        for box, score, label in zip(boxes[0], scores[0], labels[0]):
            if score>=confidence_threshold:
                object_data = []
                class_label = class_mapping[label]
                draw_labelled_box(visualisation_image, box, score, label, class_label)
                draw_image_name(visualisation_image, each_image)
                object_data.append(class_label)
                object_data.append(score)
                object_data.append(box.astype(int))
                object_detection_data.append(object_data)
        numpy_image = np.asarray(visualisation_image)
        images_to_draw.append(numpy_image)
    return images_to_draw, object_detection_data



def preview_performance(inference_dir, model, num_preview_images=10, confidence_threshold=50):
    """
    Function: NOT USED IN GUI. USEFUL FOR JUPYTER NOTEBOOK OR FUTURE GUI DEVELOPMENT.Runs inference on randomly selected subsample of inference images to test model
    Parameters:
       inference_dir: path to dir containing inference images
       model: converted h5 file
       num_preview_images: number of images user wants to preview before running inference
       confidence threshold: only draw boxes with conf above 50%
    Returns:
       visualisation_images: numpy array of images with bounding boxes and labels
    """
    list_of_images = generate_list_of_images(inference_dir)
    random_images = []
    index_pos = set()
    while len(index_pos)<num_preview_images:
        random_index = random.randrange(len(list_of_images))
        index_pos.add(random_index)
    for i in index_pos:
        random_image = list_of_images[i]
        random_images.append(random_image)
    visualisation_images = run_inference_on_images(inference_dir, random_images, model, confidence_threshold, './classes.csv')
    return visualisation_images

def run_inference(inference_dir, model, class_mapping_file, confidence_threshold=0.5):
    """
    Function: NOT USED IN CURRENT GUI. USE IN FUTURE DEVELOPMENT. Runs inference on all images in inference dir
    Parameters:
       inference_dir: path to dir containing inference images
       model: convert h5 file
       class_mapping_file: file mapping int values to labels
       confidence threshold: only draw boxes with conf above 50%
    Returns:
       visualisation_images: numpy array of images with bounding boxes and labels
       object_detection_data: list of classes and confidence scores
    """
    list_of_images = generate_list_of_images(inference_dir)
    visualisation_images, object_detection_data = run_inference_on_images(inference_dir, list_of_images, model, confidence_threshold, class_mapping_file)
    return visualisation_images, object_detection_data

    

                
def prepare_image(inference_dir, image_name):
    """
    Parameters:
       inference_dir: path to dir containing inference images
       image_name: name of image file .jpg
    Return:
       image_model: image passed into retinanet
       image_visualisation: image on which bounding boxes are drawn
    """
    image_path = os.path.join(inference_dir, image_name)
    image = read_image_bgr(image_path)
    image_visualisation = image.copy()
    image_visualisation = cv2.cvtColor(image_visualisation, cv2.COLOR_BGR2RGB)
    image_model = preprocess_image(image)
    return image_model, image_visualisation

def run_model_on_image(image_model, model):
    """
    Parameters:
       image_model: image passed into retinanet
       model: retinanet model (converted)
    Return:
       boxes: bounding boxes returned by retinanet
       scores: corresponding confidence scores
       labels: corresponding int values denoting class labels
    """
    image, scale = resize_image(image_model)
    boxes, scores, labels = model.predict_on_batch(np.expand_dims(image, axis=0))
    boxes /= scale
    return boxes, scores, labels

def set_confidence_threshold(confidence_threshold):
    """
    Parameters: 
       confidence_threshold: value between 0-100
    Return:
       confidence_threshold: value between 0.0-1.0
    """
    error="Value of confidence threshold must be between 0 and 100"
    if confidence_threshold<0 or confidence_threshold >100:
        return print(error)
    else:
        confidence_threshold = confidence_threshold/100
        return confidence_threshold

def draw_labelled_box(image, box, score, label, class_label):
    """
    Parameters:
       image: image on which bounding boxes/labels are drawn
       box: box to be drawn
       score: corresponding confidence score
       label: corresponding int denoting class label
       class_label: string class label 
    Return:
    """
    color = get_label_color(label)
    box = box.astype(int)
    draw_box(image, box, color=color)
    caption = "{} {:.1f}%".format(class_label, score*100)
    draw_caption(image, box, caption)
    return 

def get_label_color(label):
    """
    Parameters: 
       label: int value denoting class
    Return:
       label_color(label): retinanet method assigning color to class
    """
    return label_color(label)

def choose_inference_model(model_dir, unconverted_model):
    """
    Parameters:
       unconverted_model: h5 file to be converted to inference model (from ./snapshots/)
       model_dir: the dir containing the custom or default models
    Returns:
       converted retinanet model
    """
    keras.backend.tensorflow_backend.set_session(get_session())
    model_path = os.path.join(model_dir, unconverted_model)
    model = models.load_model(model_path, backbone_name='resnet50')
    model = models.convert_model(model)
    return model

def export_model(chosen_model, name, delete_remaining_models):
    """
    Function: moves chosen model from ./snapshots/ to ./pretrained_models/
    Parameters:
       chosen_model: h5 file to exported. Chosen from ./snapshots/ by user.
       name: user chosen name for model to export and corresponding class mapping file
       delet_remaining_models: bool, True by default
    Returns:
    """
    current_dir = './snapshots/'+chosen_model
    classes_csv = './classes.csv'
    save_dir = 'pretrained_models/'
    model_name = save_dir+name+'.h5'
    classes_csv_name = save_dir+name+'.csv'
    print("Saving model ",name," to ",save_dir)
    shutil.move(current_dir, model_name)
    shutil.move(classes_csv, classes_csv_name)
    print("Your chosen model has been exported")
    if delete_remaining_models == True:
        delete_suboptimal_models(delete_remaining_models)
    return

def delete_suboptimal_models(delete=True):
    """
    Function: deletes all unchosen models contained in ./snapshots/
    Parameters:
       delete: True by default h5 
    Returns:
    """
    snapshots_dir='./snapshots/'
    if delete==True:
        for each_file in os.listdir(snapshots_dir):
            file_to_remove = snapshots_dir+each_file
            if os.path.exists(file_to_remove):
                os.remove(file_to_remove)
    print("All other files in ./snapshots/ have been deleted.")
    return

def int_to_label(class_mapping_file):
    """
    Parameters:
       class_mapping_file: csv file containing class, int values
    Returns:
       class_mapping: dictionary mapping int:class
    """
    class_mapping = {}
    f = open(class_mapping_file, "r")
    for i, line in enumerate(f):
        class_label = line.split(",")[0]
        mapping = {i:class_label}
        class_mapping.update(mapping)
    f.close()
    return class_mapping

def get_session():
    """
    Parameters:
    Return: tensorflow session
    """
    config = tf.ConfigProto()
    config.gpu_options.allow_growth = True
    return tf.Session(config=config)

def draw_boxes(image, boxes, color, thickness=4):
    """
    Parameters:
       image: The image to draw on.
       boxes: A [N, 4] matrix (x1, y1, x2, y2).
       color: The color of the boxes.
       thickness: The thickness of the lines to draw boxes with.
    Returns:
    """
    for b in boxes:
        draw_box(image, b, color, thickness=thickness) 

def draw_caption(image, box, caption):
    """
    Parameters:
       image: The image to draw on.
       box: A list of 4 elements (x1, y1, x2, y2).
       caption: String containing the text to draw.
    Return:
    """
    b = np.array(box).astype(int)
    cv2.putText(image, caption, (b[0]+10, b[1] + 30), cv2.FONT_HERSHEY_PLAIN, 2, (0, 0, 0), 5)
    cv2.putText(image, caption, (b[0]+10, b[1] + 30), cv2.FONT_HERSHEY_PLAIN, 2, (255, 255, 255), 2)

def draw_image_name(image, name):
    """
    Parameters:
       image: The image to draw on.
       name: the name of the image
    """
    bottom=image.shape[0]-20
    cv2.putText(image, name, (10,bottom),cv2.FONT_HERSHEY_PLAIN, 1.5, (0, 0, 0), 4)
    cv2.putText(image, name, (10, bottom), cv2.FONT_HERSHEY_PLAIN, 1.5, (255, 255, 255), 2)

