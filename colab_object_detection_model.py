# object detection webpages: 
# https://docs.ultralytics.com/modes/predict/
# https://docs.ultralytics.com/usage/python/#predict
# https://colab.research.google.com/github/ultralytics/ultralytics/blob/main/examples/tutorial.ipynb#scrollTo=ax3p94VNK9zR
# https://inside-machinelearning.com/en/bounding-boxes-python-function/
#!rm -rf images # colab command to delete a folder and all the files within it, without being prompted
# the COCO dataset classes the Yolov8 model was trained on

coco_names=["person",
    "bicycle",
    "car",
    "motorcycle",
    "airplane",
    "bus",
    "train",
    "truck",
    "boat",
    "trafficlight",
    "firehydrant",
    "stopsign",
    "parkingmeter",
    "bench",
    "bird",
    "cat",
    "dog",
    "horse",
    "sheep",
    "cow",
    "elephant",
    "bear",
    "zebra",
    "giraffe",
    "backpack",
    "umbrella",
    "handbag",
    "tie",
    "suitcase",
    "frisbee",
    "skis",
    "snowboard",
    "sportsball",
    "kite",
    "baseballbat",
    "baseballglove",
    "skateboard",
    "surfboard",
    "tennisracket",
    "bottle",
    "wineglass",
    "cup",
    "fork",
    "knife",
    "spoon",
    "bowl",
    "banana",
    "apple",
    "sandwich",
    "orange",
    "broccoli",
    "carrot",
    "hotdog",
    "pizza",
    "donut",
    "cake",
    "chair",
    "couch",
    "pottedplant",
    "bed",
    "diningtable",
    "toilet",
    "tv",
    "laptop",
    "mouse",
    "remote",
    "keyboard",
    "cellphone",
    "microwave",
    "oven",
    "toaster",
    "sink",
    "refrigerator",
    "book",
    "clock",
    "vase",
    "scissors",
    "teddybear",
    "hairdrier",
    "toothbrush"
    ]

!pwd
%cd /content
!pwd
%cd wiki
# step 4
%cd wiki
!pwd
print('finished execution')
######
# now laod the json file generated into a ddaframe to be used by yolo for predictions:
import pandas as pd
import logging
import requests
import json
import os
from urllib.parse import urlparse
# Load the JSON file into a dataframe
df_images = pd.read_json('/content/wiki/wiki/wiki.json')
df_images['filename'] = df_images['src'].apply(lambda x: os.path.basename(x)[:255]) # create a filename column restricting it to the first 255 characters in the filename
df_images['full_url'] = 'http:'+df_images['src']
# Print the resulting DataFrame
#print(df_images)
#download the images to an images folder
import io
%cd /content
#!rm -rf images # colab command to delete a folder and all the files within it, without being prompted
#!mkdir images
%cd images
# print count of image files in the images folder
!ls -1 /content/images | wc -l
###############
!pip install ultralytics
from ultralytics import YOLO
import cv2
import numpy as np
from google.colab.patches import cv2_imshow
import logging
#logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
# images directory location
image_dir='/content/images/'
model = YOLO('yolov8n.pt') # load a pretrained YOLOv8n detection model, "n" is for the smallest nano model, its fastest, but has lowest quality/performance of al the yolo v8 models
# create a an image_object_detection_prediction directory for the image object detection predictions from the yolov8 model
%cd /content
!rm -rf image_object_detection_prediction # colab command to delete a folder and all the files within it, without being prompted
!mkdir image_object_detection_prediction
%cd image_object_detection_prediction
# iterate over image filenames to pass to yolo model for image object detection predictions from the yolov8 model, to restrict to a certain amouint of images(20 in this example), use df_images.head(20).iterrows():
for i,row in df_images.iterrows(): #df_images.head(20).iterrows(): # testing for first 20 rows. For all rows use: "df_images.iterrows():"
    predicted_classes_string=""
    print('##################################Next image for object detection###############')
    try:
        print('row is:',row)
        filename_without_extension = os.path.splitext(row['filename'])[0]
        #print('filename_without_extension is:',filename_without_extension)
        image_dir_filename=image_dir+row['filename']
        dir_filename=str(image_dir_filename)
        print('dir_filename is:',dir_filename)
        image_file_name=row['filename']
        #print('image_file_name is:',image_file_name)
        #print('image_dir is:',image_dir)
        # Construct the file path
        file_path = os.path.join(image_dir, image_file_name)
        # Check if the file exists
        if os.path.exists(image_dir_filename):
            print(f'The image file {image_dir_filename} exists. Ready for image object detection')
            results = model.predict(dir_filename, save = True , save_txt = True) #,conf=0.5) # "save_txt = True" saves the bounding box information, add "conf=0.5" to show condence predictions of 50% or higher, may need to add a parameter for "imgsize" to indicate what img size the yolov8n model was trained on
            for result in results:
                for c in result.boxes.cls:
                    print('predicted class names to be appended', model.names[int(c)])
                    predicted_classes_string += ". "+model.names[int(c)].title()
                    # append text to Column B
            #df_images.at[i, row['alt']] += model.names[int(c)]
            print('predicted_classes_string combined is:',predicted_classes_string)  
            # append text to the value in Column B
            if df_images.at[i, 'alt'] is None:
                print('df_images.at[i, alt] is = None')
                print('df_images.at[i, alt] is:',df_images.at[i, 'alt'])
                df_images.at[i, 'alt']=""
                print('df_images.at[i, alt] is now set to:',df_images.at[i, 'alt'])
            df_images.at[i, 'alt'] += predicted_classes_string

        else:
            print(f'The image file {image_dir_filename} does not exist. No image object detection will take place')
    except FileNotFoundError:
        print(f"File {dir_filename} was found, but is not suitable for image object detection, skipping this file and moving to the next file in the for loop")
        continue
print('printing first 20 rows of the df_images')
# structure of df_images dataframe: src, title, alt, images, filename, full_url
df_images = df_images.drop('title', axis=1)
df_images = df_images.drop('images', axis=1)
# structure of df_images dataframe: src, alt, filename, full_url
print(df_images.head(40))
# save the dataframe to a CSV file
df_images.to_csv('images_acquired_and_object_detected.csv', index=False)
#YOLO predict model=yolov8n.pt source='https://ultralytics.com/images/bus.jpg'

print('Image crawling and detection process now complete')
