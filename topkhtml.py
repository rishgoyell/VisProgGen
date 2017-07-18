import os, sys
import numpy as np
import math
numtables = 2
numtest = 500
k = 1

def genhtml(gtlist, gtdir, predkdir, preddir, predklist=None, predlist=None, numexs=500, vistree=False):
	if predklist == None:
		predklist = gtlist
	# assert len(predklist) == len(gtlist)
	numexs = min(numexs, len(gtlist))
	gtlist = gtlist[:numexs]
	filepath = os.path.dirname(predkdir)+'/index.html'
	fp = open(filepath, 'w')
	fp.write('''
			<!DOCTYPE html>
			<html lang="en">
			<head>
			<meta charset="UTF-8">
			<title>7 step</title>
			</head>
			<h2>Improvements with RL</h2>
			<body>
			''')
	exspertable = math.ceil(numexs/numtables)
	count = 0
	height = str(500)
	width = str(195)
	for i in range(numtables):
		fp.write('''
			<table width="200" border="5" style="float:left;">
			<tr>
			<th>S.No.</th>
			<th>Ground Truth</th>
			<th>Greedy Pred (k=1)</th>
			''')
		for j in range(1,k+1):
			fp.write('<th> RL </th>')
		fp.write('</tr>')

		for j in range(i*exspertable, min((i+1)*exspertable, numexs)):
			count = count+1
			fp.write('''<tr>
				<td height="'''+ height + '" width="' + width + '"/>'''+ str(count) + '</td><td height="' + height +'" width="' + width +'"/><img src=''' + gtdir + '/' + gtlist[j]+ ' alt='+ gtlist[j]+' width="' + width +'"> </td>\n')
			fp.write('<td height="' + height +'" width="' + width +'"/> <img src=' + preddir +'/'+predlist[j]+ ' alt='+ predlist[j] + ' width="' + width +'"/> </td>\n')
			for l in range(k):
				fp.write('<td height="' + height +'" width="' + width +'"/> <img src=' + predkdir +'/'+predklist[j*k+l]+ ' alt='+ predklist[j*k+l] + ' width="' + width +'"/> </td>\n')
			fp.write('</tr>\n')


if __name__ == '__main__':
	gtdir = "/home/rishabh/Documents/experiment/7step/gt"
	predkdir = "/home/rishabh/Documents/experiment/7step/rl"
	preddir = "/home/rishabh/Documents/experiment/7step/pred"
	gtlist = []
	predklist = []
	predlist = []
	for i in range(numtest):
		filename = 'vis'+str(i+1)+'.png'
		gtlist.append(filename)
		if os.path.isfile(preddir+'/'+filename):
			predlist.append(filename)
		else:
			predlist.append('Error')
		for j in range(i*k,(i+1)*k):
			filename = 'vis'+str(j+1)+'.png'
			if os.path.isfile(predkdir+'/'+filename):
				predklist.append(filename)
			else:
				predklist.append('error')
	genhtml(gtlist, gtdir, predkdir, preddir, predklist=predklist, predlist=predlist)