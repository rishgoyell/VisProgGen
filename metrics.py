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

wrongpolicylist = ['fixed','balncan', 'ignore']

class Evaluate(object):

	def __init__(self, gtdir, preddir, wrongpolicy='fixed'):
		self.gtdir = gtdir
		self.preddir = preddir
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
		if self.wrongpolicy=='blancan' or not errflag:
			self.mse += self.msefunc(predimage, gtimage)
			self.hausdist += self.hausfunc(predimage, gtimage)
			self.chamferdist += self.chamferfunc(predimage, gtimage)
		elif self.wrongpolicy=='fixed':
			self.mse += canvas_shape[0]*canvas_shape[1]
			self.hausdist += 64
			self.chamferdist += 64
		elif self.wrongpolicy=='ignore':
			return


	def evalfunc(self):
		self.numimages = 0
		self.numwrongexps = 0
		self.mse = 0
		self.hausdist = 0
		self.chamferdist = 0
		for filename in os.listdir(self.gtdir):
			errflag = False
			if filename.endswith('.png'):
				self.numimages += 1
				gtimage = misc.imread(self.gtdir + '/' + filename)
				gtimage = (gtimage[:,:,0]==0)
				if os.path.isfile(self.preddir + '/' + filename):
					predimage = misc.imread(self.preddir + '/' + filename)
					predimage = (predimage[:,:,0]==0)
				else:
					self.numwrongexps += 1
					errflag = True
					predimage = misc.imread(self.preddir + '/err' + filename)
					predimage = (predimage[:,:,0]==0)
				self.updatedist(predimage, gtimage, errflag)

		if self.wrongpolicy == 'ignore':
			self.numimages = self.numimages - self.numwrongexps
		print('Pixel-level accuracy:', 100-self.mse*100/(canvas_shape[0]*canvas_shape[1]*self.numimages), '\nMean Error:', self.mse/self.numimages, '\nAvg Hausdorff Distance:',self.hausdist/self.numimages, '\nAvg Chamfer Distance:',self.chamferdist/self.numimages)
		print(str(self.numwrongexps) + ' wrong expressions out of ' + str(self.numimages))


if __name__ == '__main__':
	gtdir = '/home/rishabh/Downloads/visualisations/xyz'
	preddir = '/home/rishabh/Downloads/visualisations/yxz'
	e = Evaluate(gtdir, preddir)
	for x in wrongpolicylist:
		print("------------- "+x+" -------------")
		e.wrongpolicy = x
		e.evalfunc()