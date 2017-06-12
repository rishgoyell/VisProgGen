import os,sys
import numpy as np
from genexp import canvas_shape, xstep, ystep, scalestep, min_scale, max_scale, oplist, xlist, ylist, scalelist, shapelist

class stats(object):
	def __init__(self, canvas_shape, xstep, ystep, scalestep, min_scale, max_scale):
		self.canvas_shape = canvas_shape
		self.xstep = xstep
		self.ystep = ystep
		self.scalestep = scalestep
		self.min_scale = min_scale
		self.max_scale = max_scale
		self.position = np.zeros([-(-(canvas_shape[0]-min_scale)//xstep),-(-(canvas_shape[1]-min_scale)//ystep)], dtype=int)
		self.operation = {'+': 0, '-': 0, '*': 0}
		self.shape = {'c': 0,'t': 0,'s': 0}
		self.scale = np.zeros(-(-(max_scale-min_scale+1)//scalestep), dtype=int)

	def printstats(self):
		print("<<<<<<<<< Position >>>>>>>>>> \n")
		print("\t|", end="\t")
		for j in range(self.position.shape[1]):
			print(j*ystep+min_scale, end="\t")
		print("")
		print("__________________", end="")
		for j in range(self.position.shape[1]):
			print("________", end="")
		print("")
		for i in range(self.position.shape[0]):
			print(i*xstep+min_scale, '\t|', end="\t")
			for j in range(self.position.shape[1]):
				print(self.position[i,j], end="\t")
			print("\n", end="")

		print("\n<<<<<<<<<< Operation >>>>>>>>>> \n")
		for i in self.operation.keys():
			print(i, self.operation[i])

		print("\n<<<<<<<<<< Shape >>>>>>>>>>\n")
		for i in self.shape.keys():
			print(i, self.shape[i])

		print("\n<<<<<<<<<< Scale >>>>>>>>>>\n")
		for i in range(self.scale.shape[0]):
			print(i*self.scalestep+min_scale,"\t", self.scale[i])
		print("\n")




# canvas_shape = [64, 64]

# xstep = canvas_shape[0]//8
# ystep = canvas_shape[1]//8
# scalestep = 4

# min_scale = 8
# max_scale = canvas_shape[0]//2

# oplist = ['+', '-', '*']
# xlist = range(min_scale, canvas_shape[0], xstep)
# ylist = range(min_scale, canvas_shape[1], ystep)
# scalelist = range(min_scale, max_scale+1, scalestep)
# shapelist = ['c', 't', 's']


filename = '/home/rishabh/Documents/VisProgGen/test/expressions.txt'
datastats = stats(canvas_shape, xstep, ystep, scalestep, min_scale, max_scale)

with open(filename) as f:
	for line in f:
		for op in oplist:
			datastats.operation[op] += line.count(op)
		for scale in scalelist:
			datastats.scale[(scale-min_scale)//scalestep] += line.count(str(scale)+')')
		for shape in shapelist:
			datastats.shape[shape] += line.count(shape+'(')
		for x in xlist:
			for y in ylist:
				datastats.position[(x-min_scale)//xstep,(y-min_scale)//ystep] += line.count('('+str(x)+','+str(y)+',')
datastats.printstats()
