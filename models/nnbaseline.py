import os, sys
sys.path.append('/home/rishabh/Documents/VisProgGen')
import numpy as np
from scipy import misc
from metrics import Evaluate

class nnbase(object):
	def __init__(self, traindir, testdir, dist = 'mse', canvassize=[64,64]):
		self.traindir = traindir
		self.testdir = testdir
		self.dist = dist
		self.canvassize = canvassize
		self.resultlist = []
		self.resultfile = open(self.testdir+'/result.txt', 'w')
		self.numtest = 0
		self.avgerror = [0,0,0]
		self.trainmat = np.zeros([1,canvassize[0]*canvassize[1]], dtype=bool)
		self.filelist = []
		i=0
		for x in os.listdir(self.traindir):
			if x.endswith('.png'):
				i+=1
				if i%1000==0:
					print(i)
					sys.stdout.flush()
				self.filelist.append(x)
				trainimage = misc.imread(self.traindir + '/' + x)
				self.trainmat = np.append(self.trainmat, np.expand_dims(np.ndarray.flatten(trainimage[:,:,0]==0), axis=0), axis=0)

		print(i)
		self.trainmat = np.delete(self.trainmat, 0, 0)

	def findexp(self):
		e = Evaluate()
		for filename in os.listdir(self.testdir):
			if filename.endswith('.png'):
				self.numtest += 1
				msemin = self.canvassize[0]*self.canvassize[1]
				lmsefile = None
				testimage = misc.imread(self.testdir + '/' + filename)
				testimagefl = np.ndarray.flatten(testimage[:,:,0]==0)
				x = np.apply_along_axis(np.logical_xor, 1, self.trainmat, testimagefl)
				x = np.sum(x, axis=1)
				ind = np.argmin(x)
				self.avgerror[0] += x[ind]
				self.avgerror[1] += e.hausfunc(self.trainmat[ind].reshape(self.canvassize), testimage[:,:,0]==0)
				self.avgerror[2] += e.chamferfunc(self.trainmat[ind].reshape(self.canvassize), testimage[:,:,0]==0)
				self.resultfile.write(filename + ', ' + self.filelist[ind] +'\n')

				# for i in range(self.trainmat.shape[0]):
				# 		mse = np.sum(np.logical_xor(testimage, trainimage))
				# 		if mse < msemin:
				# 			msemin = mse
				# 			lmsefile = x
				# self.resultfile.write(filename + ', ' + lmsefile+'\n')
				# self.avgerror += msemin
				if self.numtest%10==0:
					print(self.numtest, filename, self.filelist[ind])
					print("MSE:"+str(self.avgerror[0]/self.numtest)+
						"\nHausdorff:"+str(self.avgerror[1]/self.numtest)+
						"\nChamfer:"+str(self.avgerror[2]/self.numtest))

if __name__=='__main__':
	traindir = '/home/rishabh/Documents/experiment/2step/train'
	testdir = '/home/rishabh/Documents/experiment/2step/test'
	nnbase = nnbase(traindir, testdir)
	nnbase.findexp()


