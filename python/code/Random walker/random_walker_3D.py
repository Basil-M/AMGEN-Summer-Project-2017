import numpy as np
import niipy as nii
import matplotlib.pyplot as plt
from skimage.segmentation import random_walker
from skimage.data import binary_blobs
from skimage.exposure import rescale_intensity
import skimage

FOLDER_PATH= "/scratch/python/datasets/ACDC/ACDC_challenge_20170617/"
patient = 1
frame = 1

#FILEPATHS
frame_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + ".nii.gz"

mask_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + "_scribble.nii.gz"

output_mask_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + "_regen.nii.gz"

print("Extracting data from " + frame_path)

frame, frame_aff, frame_hdr = nii.load_nii(frame_path)
#frame = frame[:,:,:]
mask, mask_aff, mask_hdr = nii.load_nii(mask_path)
#mask = mask[:,:,:]

slice_count = mask.shape[2]
labels = np.unique(mask).astype(int)
print labels
print frame.shape
print mask.shape
new_labels = np.zeros(mask.shape)

new_labels = random_walker(frame,mask,beta = 5, mode = 'cg_mg',tol = 0.001)
#BETA: Penalization coefficient for random walker motion. Higher beta = more difficult diffusion
#MODE: bf = brute force (fast for small images), cg = conjugate gradient, cg_mg = conjugate gradient + multigrid preconditioner
#return_full_prob: Can return full probabilities instead of 'most likely'
#Tolerance
#Save nifti data
nii.save_nii(output_mask_path, new_labels, mask_aff, mask_hdr)
