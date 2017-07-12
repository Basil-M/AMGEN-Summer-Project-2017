__author__ = 'bmustafa'
import numpy as np
import warnings
import matplotlib.pyplot as plt
from skimage.segmentation import random_walker

def rw_segment(image, seeds, threshold=0.95, beta=90, bg_label=-1, return_bg_label = False, debug=False):
    # Uses scikit-image's implementation of Leo Grady's Random Walker algorithm
    #
    # Inputs:
    #   image           -  array-like of image. Expected volumetric - i.e. (width, height, slice)
    #   seeds           -  array-like of known labels. same dimensions as image
    #   threshold       -  value to threshold probability to
    #   beta            -  gradient penalization coefficient.
    #                      Higher beta increases the effect of intensity changes (i.e. lower probabilities)
    #   bg_label        -  this is the label assigned to the background.
    #                      If no value is passed, it is assumed that the background IS labelled and that
    #                      it is the highest valued label in the seeds.
    #   return_bg_label -  Returned mask will not include any labeled pixels for background data
    #   debug           -  If debug is True, displays segmentation data
    # Usage:
    # DEBUG MODE:
    #   If debug = 1, it will sequentially go through every slice in the image
    #   Displaying the scan, the input seeds and the output segmentation
    #
    # BACKGROUND LABEL: Set to bg_label = 0 if background is unlabelled

    slice_count = seeds.shape[2]

    #Labels are unique values in the mask
    labels = np.unique(seeds).astype(int)

    #Remove zero label
    labels = np.delete(labels, 0)

    #Cast seed array to integer
    seeds = seeds.astype(int)

    #Initialise array of new labels
    new_labels = np.zeros(image.shape)

    #Handle background label
    if bg_label == -1:
        #Assume largest label is the background
        bg_label = np.amax(labels)
    elif bg_label == 0:
        #Warn for no background label
        warnings.warn("WARNING: Input does have labelled background. "
                      "Results are typically much better with background seeds.")

    for sliceNo in range(0, slice_count):
        #RandomWalkAlgorithm

        #isolate image data + seeds for this slice
        data = np.squeeze(image[:, :, sliceNo])
        markers = np.squeeze(seeds[:, :, sliceNo])

        try:
            probs = random_walker(data, markers, beta=beta, mode='cg_mg', return_full_prob=True)

            #First, wherever the probability of other labels is higher, set label probability to zero
            for lab_id_src in range(0, probs.shape[0]):
                for lab_id_trg in range(0, probs.shape[0]):
                    if lab_id_trg != lab_id_src:
                        probs[lab_id_src, probs[lab_id_trg, :, :] > probs[lab_id_src, :, :]] = 0

            #Threshold probabilities
            probs[probs >= threshold] = 1
            probs[probs < threshold] = 0

            #Merge into marker array
            for lab_id_src in range(0, probs.shape[0]):
                #Don't include background label in output
                if labels[lab_id_src] != bg_label | return_bg_label:
                    new_labels[:, :, sliceNo] += probs[lab_id_src, :, :]*labels[lab_id_src]

            if debug:
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
                ax3.imshow(new_labels[:, :, sliceNo]/np.amax(labels) + 0.3*data/np.amax(data), cmap='gray', interpolation='nearest')
                ax3.axis('off')
                ax3.set_adjustable('box-forced')
                ax3.set_title('Segmentation')

                fig.tight_layout()
                plt.show()
        except Exception:
            warnings.warn("WARNING: Error computing segmentation for slice {}. Outputting original seeds.".format(sliceNo))
            new_labels[:,:,sliceNo] = markers

    return new_labels
