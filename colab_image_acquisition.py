# !rm -rf images # colab command to delete a folder and all the files within it, wythout being prompted
from google.colab import drive
drive.mount('/content/drive')
!pwd
%cd /content
!pwd
#!ls
!pip install scrapy # step 1
!scrapy startproject wiki # step 2
##########start with section 1 above
###########################################################
########## after successful run of above section 1, then modify the config files, then run section 2 below
## files to create are: wiki_spider.py
## file to modify is settings.py
## as an automated alternative, copying these pre-made files from Google Drive to Colab to use in this script
# step 3
%cd /content
%cd wiki
# step 4
%cd wiki
%cd spiders
!pwd
# copying a pre-made version of wiki_spider.py from Google drive to colab to use as the spider
!cp "/content/drive/My Drive/CA6005_Mechanics_of_Search/ceacht_a_do/wiki_spider.py" "./wiki_spider.py"
!pwd
!ls
%cd ../
!pwd
# copying a pre-made version of settings.py from Google drive to colab to use as the spider settings file
!cp "/content/drive/My Drive/CA6005_Mechanics_of_Search/ceacht_a_do/settings.py" "./settings.py"
!pwd
!ls
# step 6:
%cd /content
%cd wiki
# step 4
%cd wiki
!rm wiki.json
!scrapy crawl wiki -O wiki.json
print('finished execution')
######
# now laod the json file generated into a ddaframe to be used by yolo for predictions:
import pandas as pd
import logging
import requests
import json
import os
from urllib.parse import urlparse
#from PIL import Image
# Load the JSON file into a dataframe
df_images = pd.read_json('/content/wiki/wiki/wiki.json')
df_images['filename'] = df_images['src'].apply(lambda x: os.path.basename(x)[:255]) # create a filename column restricting it to the first 255 characters in the filename
df_images['full_url'] = 'http:'+df_images['src']
# Print the resulting DataFrame
print(df_images)
#download the images to an images folder
import io
%cd /content
!rm -rf images # colab command to delete a folder and all the files within it, without being prompted
!mkdir images
%cd images
# iterate over urls and download images
for i,row in df_images.iterrows():
    print('row is:',row)
    response = requests.get(row['full_url'])
    with open(row['filename'], 'wb') as f:
        f.write(response.content)
# print count of image files in the images folder
!ls -1 /content/images | wc -l
###############
