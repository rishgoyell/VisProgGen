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

gtdir = '/home/rishabh/Downloads/visualisations/wrongGT'
preddir = '/home/rishabh/Downloads/visualisations/wrongprog'
# preddir = 'abc/sc'
# gtdir = 'abc/bc'
wrongexp = 'fixed'
numimages = 0
numwrongexps = 0
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

	if ind_1.shape[0]==0 and ind_2.shape[0]==0:
		return 0
	elif ind_1.shape[0]==0 or ind_2.shape[0]==0:
		return canvas_shape[0]

	D = cdist(ind_1, ind_2, 'euclidean')
	d = (np.sum(np.min(D, axis=0)) + np.sum(np.min(D, axis=1))) / (ind_1.shape[0] + ind_2.shape[0])
	return d

def updatedist(predimage, gtimage, errflag):
	global mse, hausdist, chamferdist
	if wrongexp=='blancan' or not errflag:
		mse += msefunc(predimage, gtimage)
		hausdist += hausfunc(predimage, gtimage)
		chamferdist += chamferfunc(predimage, gtimage)
	else:
		mse += canvas_shape[0]*canvas_shape[1]
		hausdist += 64
		chamferdist += 64



for filename in os.listdir(gtdir):
	errflag = False
	if filename.endswith('.png'):
		numimages += 1
		gtimage = misc.imread(gtdir + '/' + filename)
		gtimage = (gtimage[:,:,0]==0)
		if os.path.isfile(preddir + '/' + filename):
			predimage = misc.imread(preddir + '/' + filename)
			predimage = (predimage[:,:,0]==0)
		else:
			numwrongexps += 1
			errflag = True
			predimage = misc.imread(preddir + '/err' + filename)
			predimage = (predimage[:,:,0]==0)
		updatedist(predimage, gtimage, errflag)

print('MSE:', mse/numimages, '\nAvg Hausdorff Distance:',hausdist/numimages, '\nAvg Chamfer Distance:',chamferdist/numimages)
print(str(numwrongexps) + ' wrong expressions out of ' + str(numimages))