import main
import os
import scipy
import numpy as np
from matplotlib import pylab as plt
from canvasops import canvas_shape
from scipy import misc
from skimage import feature
from scipy.spatial.distance import cdist
from scipy.spatial.distance import directed_hausdorff

preddir = '/home/rishabh/Downloads/visualisations/wrongGT'
gtdir = '/home/rishabh/Downloads/visualisations/wrongprog'
# preddir = 'abc/bc'
# gtdir = 'abc/sc'
numimages = 0
mse = 0
hausdist = 0
chamferdist = 0

def msefunc(arr1, arr2):
	return np.sum(np.logical_xor(arr1, arr2))

def hausfunc(arr1, arr2):
    arr1 = feature.canny(arr1, sigma=0.0)
    arr2 = feature.canny(arr2, sigma=0.0)

    x, y = np.nonzero(arr1)
    ind_1 = np.array([x.reshape(-1), y.reshape(-1)]).transpose()

    x, y = np.nonzero(arr2)
    ind_2 = np.array([x.reshape(-1), y.reshape(-1)]).transpose()
    return max(directed_hausdorff(ind_1, ind_2)[0], directed_hausdorff(ind_2, ind_1)[0])

def chamferfunc(arr1, arr2):
	arr1 = feature.canny(arr1, sigma=0.0)
	arr2 = feature.canny(arr2, sigma=0.0)

	x, y = np.nonzero(arr1)
	ind_1 = np.array([x.reshape(-1), y.reshape(-1)]).transpose()

	x, y = np.nonzero(arr2)
	ind_2 = np.array([x.reshape(-1), y.reshape(-1)]).transpose()

	D = cdist(ind_1, ind_2, 'euclidean')
	d = (np.sum(np.min(D, axis=0)) + np.sum(np.min(D, axis=1))) / (ind_1.shape[0] + ind_2.shape[0])
	return d



for filename in os.listdir(preddir):
	if filename.endswith('.png'):
		numimages += 1
		predimage = misc.imread(preddir + '/' + filename)
		predimage = (predimage[:,:,0]==0)
		gtimage = misc.imread(gtdir + '/' + filename)
		gtimage = (gtimage[:,:,0]==0)

		mse += msefunc(predimage, gtimage)
		hausdist += hausfunc(predimage, gtimage)
		chamferdist += chamferfunc(predimage, gtimage)

print('MSE:', mse/numimages, '\nAvg Hausdorff Distance:',hausdist/numimages, '\nAvg Chamfer Distance:',chamferdist/numimages)
