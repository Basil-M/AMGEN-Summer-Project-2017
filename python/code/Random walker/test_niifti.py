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
debug = 0
#FILEPATHS


nii_4d_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_4d.nii.gz"

frame_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + ".nii.gz"

mask_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + "_scribble.nii.gz"

output_mask_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + "_regen.nii.gz"

print("Extracting data from " + frame_path)

frame, frame_aff, frame_hdr = nii.load_nii(frame_path)
frame = frame[:,:,:]

mask, mask_aff, mask_hdr = nii.load_nii(mask_path)
slice_count = mask.shape[2]
labels = np.unique(mask).astype(int)
print mask.shape
print labels
new_labels = np.zeros(mask.shape)

for sliceNo in range(slice_count):
	#RandomWalkAlgorithm
	new_labels[:,:,sliceNo] = random_walker(frame[:,:,sliceNo], mask[:,:,sliceNo].astype(int),beta=5, mode = 'bf')
		#BETA: Penalization coefficient for random walker motion. Higher beta = more difficult diffusion
		#MODE: bf = brute force (fast for small images), cg = conjugate gradient, cg_mg = conjugate gradient + multigrid preconditioner
		#return_full_prob: Can return full probabilities instead of 'most likely'
		#Tolerance
	if debug == 1:
		# Plot results
		data = frame[:,:,sliceNo]
		markers = mask[:,:,sliceNo]

		fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(8, 3.2),
				                    sharex=True, sharey=True)
		ax1.imshow(data, cmap='gray', interpolation='nearest')
		ax1.axis('off')
		ax1.set_adjustable('box-forced')
		ax1.set_title('MRI slice %s'% (sliceNo + 1))
		ax2.imshow(markers, cmap='magma', interpolation='nearest')
		ax2.axis('off')
		ax2.set_adjustable('box-forced')
		ax2.set_title('Markers')
		ax3.imshow(new_labels[:,:,sliceNo], cmap='gray', interpolation='nearest')
		ax3.axis('off')
		ax3.set_adjustable('box-forced')
		ax3.set_title('Segmentation')

		fig.tight_layout()
		plt.show()

if debug == 0:
	#Save nifti data
	nii.save_nii(output_mask_path, new_labels, mask_aff, mask_hdr)
