import os, sys
import numpy as np
import math
numtables = 1

def genhtml(gtlist, gtdir, preddir, predlist=None, numexs=500, vistree=False):
	if predlist == None:
		predlist = gtlist
	# assert len(predlist) == len(gtlist)
	gtlist = gtlist[:numexs]
	filepath = os.path.dirname(preddir[1])+'/index.html'
	fp = open(filepath, 'w')
	fp.write('''
			<!DOCTYPE html>
			<html lang="en">
			<head>
			<meta charset="UTF-8">
			<title>Outputs of different methods</title>
			</head>
			<body>
			''')
	exspertable = math.ceil(numexs/numtables)
	count = 0
	for i in range(numtables):
		fp.write('''
			<table width="200" border="5" style="float:left;">
			<tr>
			<th>S.No.</th>
			<th>GROUND TRUTH</th>
			<th>Stack+Prev Output</th>
			<th>Stack</th>
			<th>Prev Output</th>
			<th>Hier+stack</th>
			</tr>
			''')
		for j in range(i*exspertable, min((i+1)*exspertable, numexs)):
			count = count+1
			fp.write('''<tr>
				<td>'''+ str(count) + '</td><td><img src=''' + gtdir + '/' + gtlist[j]+ ' alt='+ gtlist[j]+' height="325" width="195"/> </td>\n')
			for k in range(0,4):
				fp.write('<td> <img src=' + preddir[k]+'/'+predlist[k][j]+ ' alt='+ predlist[k][j] + ' height="325" width="195"/> </td>\n')
			fp.write('</tr>\n')


if __name__ == '__main__':
	gtdir = "/home/rishabh/Documents/compare/ground_truth"
	preddir = ["/home/rishabh/Documents/compare/joint_stack_prevout"]
	preddir.append("/home/rishabh/Documents/compare/joint_stack") 
	preddir.append("/home/rishabh/Documents/compare/joint_prevout") 
	preddir.append("/home/rishabh/Documents/compare/hierarchical_stack")
	gtlist = []
	predlist = [[],[],[],[]]
	for filename in os.listdir(gtdir):
		if ".png" in filename and 'vis'in filename:
			gtlist.append(filename)
			for i in range(0,4):
				if os.path.isfile(preddir[i]+'/'+filename):
					predlist[i].append(filename)
				else:
					predlist[i].append('Error')
	genhtml(gtlist, gtdir, preddir, predlist=predlist)

