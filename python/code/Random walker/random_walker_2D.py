import numpy as np
from pandas.tests.frame.test_join import frame
import niipy as nii
import matplotlib.pyplot as plt
from skimage.segmentation import random_walker

# Folder path of dataset
FOLDER_PATH= "/scratch/bmustafa/datasets/ACDC/ACDC_challenge_20170617/"
# Threshold for probabilties returned by random walk algorithm
THRESHOLD = 0.90
# Gradient penalisation coefficient for random walk algorithm
BETA = 2000


patient = 1
frame = 1
debug = 1

#FILEPATHS
frame_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + ".nii.gz"
mask_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + "_scribble.nii.gz"
output_mask_path = FOLDER_PATH + "patient" + '{0:0>3}'.format(patient) + "/patient" + '{0:0>3}'.format(patient) + "_frame" + '{0:0>2}'.format(frame) + "_regen.nii.gz"

print("Extracting data from " + frame_path)

img, img_aff, img_hdr = nii.load_nii(frame_path)
img = img[:, :, :]

#Load in segmentation data
mask, mask_aff, mask_hdr = nii.load_nii(mask_path)
slice_count = mask.shape[2]
#Labels are unique values in the mask
labels = np.unique(mask).astype(int)
labels = np.delete(labels, 0)
mask = mask.astype(int)		            #Convert mask to int

new_labels = np.zeros(img.shape)

for sliceNo in range(0, slice_count):
    #RandomWalkAlgorithm
    data = np.squeeze(img[:, :, sliceNo])
    markers = np.squeeze(mask[:, :, sliceNo])

    try:
        probs = random_walker(data, markers, beta=10, mode='cg_mg', return_full_prob=True)

        #First, wherever the probability of other labels is higher, set label probability to zero
        for lab_id_src in range(0, probs.shape[0]):
            for lab_id_trg in range(0, probs.shape[0]):
                if lab_id_trg != lab_id_src:
                    probs[lab_id_src, probs[lab_id_trg, :, :] > probs[lab_id_src, :, :]] = 0

        #Threshold probabilities
        probs[probs >= THRESHOLD] = 1
        probs[probs < THRESHOLD] = 0

        #Merge into marker array
        for lab_id_src in range(0, probs.shape[0]):
            new_labels[:, :, sliceNo] += probs[lab_id_src, :, :]*labels[lab_id_src]

        #BETA: Penalization coefficient for random walker motion. Higher beta = more difficult diffusion
        #MODE: bf = brute force (fast for small images),
        #      cg = conjugate gradient
        #      cg_mg = conjugate gradient + multigrid preconditioner
        #return_full_prob: Can return full probabilities instead of 'most likely'
        #Tolerance

        if debug == 1:
            # Plot results

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
            ax3.imshow(new_labels[:, :, sliceNo], cmap='gray', interpolation='nearest')
            ax3.axis('off')
            ax3.set_adjustable('box-forced')
            ax3.set_title('Segmentation')

            fig.tight_layout()
            plt.show()
    except Exception:
        pass

if debug == 0:
    #Save nifti data
    nii.save_nii(output_mask_path, new_labels, mask_aff, mask_hdr)
