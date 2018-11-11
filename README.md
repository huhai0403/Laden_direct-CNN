# Laden_direct-CNN
Laden_direct-CNN for furniture recognition

Data set contains about 313000 pictures of items currently available in DB. There are 877 categories of products identified by LadenDirekt team. 
Some of the categories contain up to 12000 pictures, but some will only have 1 or 2 pictures for the category. 
Although, it is great to have so many files available for the project time and machine power constraints won't allow to process all the files. 
So decision was made to download only up to 150 pictures per each category. For those categories that have only 1 or 2 files the data augmentation 
will be used to produce more viable data set. The resulting data set will consist of about 83000 pictures.

In order to get the data set grab the code outlined in download_files.py. This code will take the urls, randomly select 150 files per each category, 
and download into separate folders per category.
