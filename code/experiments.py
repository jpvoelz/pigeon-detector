#This script will run experiments by training the YOLOv7 model
#on randomized train and test sets of varying size.
#For demonstration purposes, the sample size is set to 10,
#and the command for training YOLO is commented out.
#To fully implement this code, clone the YOLOv7 repository
#and add the custom configuration files to the appropriate folders.

import os
import torch
import random
import shutil
from simple_image_download import simple_image_download as simp
from sklearn.model_selection import train_test_split
from xml.dom import minidom
from tqdm import tqdm
import numpy as np
import matplotlib.pyplot as plt
from contextlib import redirect_stdout
from helper_functions import *

#sample_sizes = [40,80,160,240]
sample_sizes = [10] #sample size set to 10 for demonstration purposes
n_experiments = 5

#Set paths
main_path = "/Users/joulevoelz/Documents/github/pigeon-detector/code"
dataset_path = main_path + "/bird_dataset"
all_images_dir = 'all-labels-and-images/all-images'
all_labels_dir = 'all-labels-and-images/all-labels'

#Clone YOLOv7 repository
#os.chdir(main_path)
#!git clone https://github.com/WongKinYiu/yolov7.git

#Make sure images and labels are all in the right directories
os.chdir(dataset_path)
put_files_back(dataset_path, all_images_dir, all_labels_dir)

#Run experiments
for sample_size in sample_sizes:
    
    for experiment in range(n_experiments):
        
        print("\n Sample size: " + str(sample_size) + ", Run number: " + str(experiment) + "\n")

        #Generate train, test, and validation sets
        os.chdir(dataset_path)
        images = list_files(all_images_dir)
        labels = list_files(all_labels_dir)
        images.sort()
        labels.sort()
        selection = random.sample(range(len(images)), k = sample_size)
        selection.sort()
        selected_images = [images[i] for i in selection]
        selected_labels = [labels[i] for i in selection]
        train_images, val_images, train_labels, val_labels = train_test_split(selected_images, selected_labels, test_size = 0.2, random_state = 1)
        val_images, test_images, val_labels, test_labels = train_test_split(val_images, val_labels, test_size = 0.5, random_state = 1)

        #Move files to their respective folders
        move_files_to_folder(train_labels, 'labels/train')
        move_files_to_folder(val_labels, 'labels/val')
        move_files_to_folder(test_labels, 'labels/test')
        move_files_to_folder(train_images, 'images/train')
        move_files_to_folder(val_images, 'images/val')
        move_files_to_folder(test_images, 'images/test')

        #Set location for run output
        train_output_location = f"sample_size_{sample_size}_run_{experiment}"
        train_output_weight_location = f"runs/train/{train_output_location}/weights/best.pt"
        test_output_location = f"sample_size_{sample_size}_run_{experiment}"

        #Run YOLO (will not work unless you clone the YOLOv7 repository) 
        #os.chdir(main_path)
        #os.system("python train.py --img-size 640 --cfg cfg/training/yolov7.yaml --hyp data/hyp.scratch.custom_birds.yaml --batch 8 --epochs 100 --data data/bird_data.yaml --weights yolov7.pt --workers 24 --name $train_output_location")
        #os.system("python test.py --weights $train_output_weight_location --data data/bird_data.yaml --task test --name $test_output_location")

        #Put files back in their original location
        put_files_back(dataset_path, all_images_dir, all_labels_dir)
