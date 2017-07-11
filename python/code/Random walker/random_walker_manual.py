import numpy as np
import niipy as nii
import matplotlib.pyplot as plt
from skimage.segmentation import random_walker
from skimage.data import binary_blobs
from skimage.exposure import rescale_intensity
import skimage

def edge_weight(g_i,g_j,beta):
	return np.exp(-1*beta*(g_i - g_j)**2)

def degree(i,j, data, beta):
	for loop_i in range(data.shape[0])
		for loop_j in range(data.shape[1])
			d+=edge_weight(data[i,j],data[loop_i,loop_j],beta)
						

def laplacian(px_i,data, beta):
	L = np.zeros(data.shape)
	for loop_i in range(data.shape[0])
		for loop_j in range(data.shape[1])
			if loop_i = loop_j:
				L[loop_i,loop_j] = degree(
			elif 
 
def random_walk(data, labels, beta)
	
