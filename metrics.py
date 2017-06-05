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

wrongpolicy = 'ignore'
gtdir = '/home/rishabh/Downloads/visualisations/wrongGT'
preddir = '/home/rishabh/Downloads/visualisations/wrongprog'

class Evaluate(object):

	def __init__(self, wrongpolicy='fixed'):
		self.mse = 0
		self.hausdist = 0
		self.chamferdist = 0
		self.numimages = 0
		self.numwrongexps = 0
		self.wrongpolicy = wrongpolicy

	def msefunc(self, arr1, arr2):
		return np.sum(np.logical_xor(arr1, arr2))

	def hausfunc(self, arr1, arr2):
	    arr1 = feature.canny(arr1, sigma=0.0)
	    arr2 = feature.canny(arr2, sigma=0.0)

	    x, y = np.nonzero(arr1)
	    ind_1 = np.array([x.reshape(-1), y.reshape(-1)]).transpose()

	    x, y = np.nonzero(arr2)
	    ind_2 = np.array([x.reshape(-1), y.reshape(-1)]).transpose()
	    return max(directed_hausdorff(ind_1, ind_2)[0], directed_hausdorff(ind_2, ind_1)[0])

	def chamferfunc(self, arr1, arr2):
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

	def updatedist(self, predimage, gtimage, errflag):
		global mse, hausdist, chamferdist
		if wrongpolicy=='blancan' or not errflag:
			self.mse += self.msefunc(predimage, gtimage)
			self.hausdist += self.hausfunc(predimage, gtimage)
			self.chamferdist += self.chamferfunc(predimage, gtimage)
		elif wrongpolicy=='fixed':
			self.mse += canvas_shape[0]*canvas_shape[1]
			self.hausdist += 64
			self.chamferdist += 64
		elif wrongpolicy=='ignore':
			return


	def evalfunc(self):
		self.numimages = 0
		self.numwrongexps = 0
		self.mse = 0
		self.hausdist = 0
		self.chamferdist = 0
		for filename in os.listdir(gtdir):
			errflag = False
			if filename.endswith('.png'):
				self.numimages += 1
				gtimage = misc.imread(gtdir + '/' + filename)
				gtimage = (gtimage[:,:,0]==0)
				if os.path.isfile(preddir + '/' + filename):
					predimage = misc.imread(preddir + '/' + filename)
					predimage = (predimage[:,:,0]==0)
				else:
					self.numwrongexps += 1
					errflag = True
					predimage = misc.imread(preddir + '/err' + filename)
					predimage = (predimage[:,:,0]==0)
				self.updatedist(predimage, gtimage, errflag)

		print('Pixel-level accuracy:', 100-self.mse*100/(canvas_shape[0]*canvas_shape[1]*self.numimages), '\nMSE:', self.mse/self.numimages, '\nAvg Hausdorff Distance:',self.hausdist/self.numimages, '\nAvg Chamfer Distance:',self.chamferdist/self.numimages)
		print(str(self.numwrongexps) + ' wrong expressions out of ' + str(self.numimages))


e = Evaluate(wrongpolicy)
e.evalfunc()