import numpy as np
import matplotlib.pyplot as plt
from typing import List
from skimage import draw
import json
from copy import copy
#%matplotlib inline


canvas_shape = [64,64]


def union(c1, c2):
	return c1 + c2


def difference(c1, c2):
	return c1 - c2


def intersection(c1, c2):
	return c1 * c2


class canvas(object):
	global canvas_shape
	canvasID = 0


	def __init__(self):
		canvas.canvasID = canvas.canvasID+1
		self.canvasID = copy(canvas.canvasID)
		self.drawing = np.zeros(canvas_shape, dtype=bool)


	################# DRAW CIRCLE ################
	def draw_circle(self, center: List, radius: int):	
		arr = self.drawing
		rr, cc = draw.circle(*center, radius=radius)
		for i, j in zip(rr, cc):
			if not self.inside_canvas([i, j]):
				return None
		arr[rr, cc] = 1
		self.drawing = arr


	################# DRAW TRIANGLE ################
	def draw_triangle(self, center: List, length: int):
		arr = self.drawing
		length = 1.732 * length
		rows = [
			int(center[1] + length / (2 * 1.732)), int(center[1] + length / (2 * 1.732)),
			int(center[1] - length / 1.732)
		]
		cols = [int(center[0] - length / 2.0), int(center[0] + length / 2.0), center[0]]

		rr_inner, cc_inner = draw.polygon(rows, cols)
		rr_boundary, cc_boundary = draw.polygon_perimeter(
		rows, cols, shape=canvas_shape)

		for i, j in zip(rr_boundary, cc_boundary):
			if not self.inside_canvas([i, j]):
				return None
		ROWS = np.concatenate((rr_inner, rr_boundary))
		COLS = np.concatenate((cc_inner, cc_boundary))
		arr[ROWS, COLS] = True
		self.drawing = arr


	################# DRAW SQUARE #################
	def draw_square(self, center: list, length: int):
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


		# generate the col vertices
		rr_inner, cc_inner = draw.polygon(rows, cols)
		rr_boundary, cc_boundary = draw.polygon_perimeter(rows, cols)

		ROWS = np.concatenate((rr_inner, rr_boundary))
		COLS = np.concatenate((cc_inner, cc_boundary))

		for i, j in zip(rr_boundary, cc_boundary):
			if not self.inside_canvas([i, j]):
			#             print("ooops square", i, j)
				return None

		arr[ROWS, COLS] = True
		self.drawing = arr


	################### check if shapes lie inside canvas ##################
	def inside_canvas(self, point):
	    if ((0 <= point[0]) and (point[0] <= canvas_shape[0])) and (
	        (0 <= point[1]) and (point[1] <= canvas_shape[1])):
	        return True
	    else:
	        return False