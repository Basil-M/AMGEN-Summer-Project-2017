import numpy as np
from pandas.tests.frame.test_join import frame
import niipy as nii
from rw_segmenter import rw_segment

# Folder path of dataset
FOLDER_PATH= "/scratch/bmustafa/datasets/ACDC/ACDC_challenge_20170617/"
# Threshold for probabilties returned by random walk algorithm
THRESHOLD = 0.7
# Gradient penalisation coefficient for random walk algorithm
BETA = 90

patient = 2
frame = 1
debug = 1

#FILEPATHS
frame_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + ".nii.gz"
mask_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + "_scribble.nii.gz"
output_mask_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + "_regen.nii.gz"

print("Extracting data from " + frame_path)

#Load image
img, img_aff, img_hdr = nii.load_nii(frame_path)
img = img[:, :, :]

#Load in segmentation data
mask, mask_aff, mask_hdr = nii.load_nii(mask_path)

new_mask = rw_segment(img, mask, threshold=0.95, return_bg_label=True)
new_mask = rw_segment(img, new_mask, threshold=0.5, debug=True)
nii.save_nii(output_mask_path, new_mask, mask_aff, mask_hdr)
