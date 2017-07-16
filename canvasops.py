import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
from typing import List
from skimage import draw
import json
from copy import copy
#%matplotlib inline


canvas_shape = [64, 64]
numpixels = canvas_shape[0]*canvas_shape[1]

class canvas(object):
	global canvas_shape
	global numpixels
	canvasID = 0

	def __init__(self):
		canvas.canvasID = canvas.canvasID+1
		self.canvasID = copy(canvas.canvasID)
		self.drawing = np.zeros(canvas_shape, dtype=int)
		self.flag = 1
		self.nodeID = None
		self.treeNode = None


	################# DRAW CIRCLE ################
	def draw_circle(self, center: List, radius: int, randflag):	
		arr = self.drawing
		xp = [center[0]+radius, center[0], center[0], center[0]-radius]
		yp = [center[1], center[1]+radius, center[1]-radius, center[1]]
		for i, j in zip(xp, yp):
			if not self.inside_canvas([i, j]) and randflag:
				self.flag = 0
				return None
		rr, cc = draw.circle(*center, radius=radius, shape=canvas_shape)
		arr[cc, rr] = True
		self.drawing = arr
		return 1


	################# DRAW TRIANGLE ################
	def draw_triangle(self, center: List, length: int, randflag):
		arr = self.drawing
		length = 1.732 * length
		rows = [
			int(center[1] + length / (2 * 1.732)), int(center[1] + length / (2 * 1.732)),
			int(center[1] - length / 1.732)
		]
		cols = [int(center[0] - length / 2.0), int(center[0] + length / 2.0), center[0]]

		for i, j in zip(rows, cols):
			if not self.inside_canvas([i, j]) and randflag:
				self.flag = 0
				return None

		rr_inner, cc_inner = draw.polygon(rows, cols, shape=canvas_shape)
		rr_boundary, cc_boundary = draw.polygon_perimeter(
		rows, cols, shape=canvas_shape)

		ROWS = np.concatenate((rr_inner, rr_boundary))
		COLS = np.concatenate((cc_inner, cc_boundary))
		arr[ROWS, COLS] = True
		self.drawing = arr
		return 1


	################# DRAW SQUARE #################
	def draw_square(self, center: list, length: int, randflag):
		arr = self.drawing
		length *= 1.412
		# generate the row vertices
		rows = np.array([
			int(center[0] - length / 2.0), int(center[0] + length / 2.0),
			int(center[0] + length / 2.0), int(center[0] - length / 2.0)
		])
		cols = np.array([
			int(center[1] + length / 2.0), int(center[1] + length / 2.0),
			int(center[1] - length / 2.0), int(center[1] - length / 2.0)
		])

		for i, j in zip(rows, cols):
			if not self.inside_canvas([i, j]) and randflag:
				self.flag = 0
				return None

		# generate the col vertices
		rr_inner, cc_inner = draw.polygon(rows, cols, shape=canvas_shape)
		rr_boundary, cc_boundary = draw.polygon_perimeter(rows, cols, shape=canvas_shape)

		ROWS = np.concatenate((rr_inner, rr_boundary))
		COLS = np.concatenate((cc_inner, cc_boundary))

		arr[COLS, ROWS] = True
		self.drawing = arr
		return 1


	################### check if shapes lie inside canvas ##################
	def inside_canvas(self, point):
		if ((0 <= point[0]) and (point[0] < canvas_shape[0])) and (
		    (0 <= point[1]) and (point[1] < canvas_shape[1])):
			return True
		else:
			return False


	def union(self, c2, randflag):
		#for expression received through a file
		if not randflag:
			self.drawing = np.logical_or(self.drawing, c2.drawing)
			return self

		#for expression received randomly
		if c2.flag == 0:
			self.flag = 0
		temp = np.sum(self.drawing)
		self.drawing = np.logical_or(self.drawing, c2.drawing)
		onpixels = np.sum(self.drawing)
		if onpixels <= int(1.1*max(temp, np.sum(c2.drawing))) or int(0.8*numpixels) <= onpixels: #or onpixels >= 0.9*(temp+np.sum(c2.drawing)):
			self.flag = 0
		return self


	def difference(self, c2, randflag):
		#for expression received through a file
		if not randflag:
			self.drawing =  self.drawing - np.logical_and(self.drawing, c2.drawing)
			return self

		#for expression received randomly
		if c2.flag == 0:
			self.flag = 0
		temp = np.sum(self.drawing)
		self.drawing =  self.drawing - np.logical_and(self.drawing, c2.drawing)
		onpixels = np.sum(self.drawing)
		if int(0.9*temp) <= onpixels or onpixels <= int(0.1*numpixels):
			self.flag = 0
		return self


	def intersection(self, c2, randflag):
		#for expression received through a file
		if not randflag:
			self.drawing = np.logical_and(self.drawing, c2.drawing)
			return self

		#for expression received randomly
		if c2.flag == 0:
			self.flag = 0
		temp = np.sum(self.drawing)
		self.drawing = np.logical_and(self.drawing, c2.drawing)
		onpixels = np.sum(self.drawing)
		if int(0.9*min(temp, np.sum(c2.drawing))) <= onpixels or onpixels <= int(0.1*numpixels):
			self.flag = 0
		return self


	def save(self, filename, randflag):
		#for expression received through a file
		if not randflag:
			a = np.logical_not(self.drawing)
			plt.imsave(filename+'.png', np.array(a).reshape(canvas_shape[0], canvas_shape[1]), cmap=cm.gray)			

		#for expression received randomly
		else:
			onpixels = np.sum(self.drawing)
			if onpixels <= int(0.1*numpixels) or int(0.8*numpixels) <= onpixels:
				self.flag = 0
			if self.flag:
				a = np.logical_not(self.drawing)
				plt.imsave(filename +'.png', np.array(a).reshape(canvas_shape[0], canvas_shape[1]), cmap=cm.gray)