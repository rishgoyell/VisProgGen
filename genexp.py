# RULE 1: E->E E +
# RULE 2: E->E E -
# RULE 3: E->E E *
# RULE 4: E->shape(x,y,s)

import numpy as np
import random
from canvasops import canvas_shape

xstep = canvas_shape[0]//8
ystep = canvas_shape[1]//8
scalestep = 4

min_scale = 8
max_scale = canvas_shape[0]//2

oplist = ['+', '-', '*']
xlist = range(min_scale, canvas_shape[0], xstep)
ylist = range(min_scale, canvas_shape[1], ystep)
scalelist = range(min_scale, max_scale+1, scalestep)
shapelist = ['c', 't', 's']
validlist = []

def genoperand():
	while True:
		x = str(xlist[random.randint(0, len(xlist)-1)])
		y = str(ylist[random.randint(0, len(ylist)-1)])
		scale = str(scalelist[random.randint(0, len(scalelist)-1)])
		shape = shapelist[random.randint(0, len(shapelist)-1)]
		return shape + '(' + x + ',' + y + ',' + scale + ')'

def genparenthesis(openp, closep, currstr=""):
	if openp == 0:
	    temp = ""
	    for i in range(closep):
	        temp = temp + ')'
	    validlist[len(currstr+temp)//2-1].append(currstr+temp)
	    return
	elif currstr.count(")") > currstr.count("("):
	    return
	genparenthesis(openp-1, closep, currstr+'(')
	genparenthesis(openp, closep-1, currstr+')')
	return

def createparendatastructure(maxops):
	for i in range(maxops):
		validlist.append([])
		genparenthesis(i+1, i+1)


def randomExp():
	stack = ['E']
	exp = ''
	count = 0
	while len(stack)!=0:
		#2 ensures that expressions with 1 operand are not generated
		#count increases the probability of choosing a terminal as the expression becomes larger
		opnum = random.randint(0,2+count)
		if opnum in range(3):
			stack.append('E')
			exp = oplist[opnum] + exp
		else:
			stack.pop()
			operand = genoperand()
			exp = operand + exp
		count = count+1
	return exp


#this function works for numops = 0,1,2 only
def fixedSizeExpLim(numops):
	exp = []
	expstring = ''
	for i in range(numops+1):
		operand = genoperand()
		exp.append(operand)
	for i in range(numops):
		op = oplist[random.randint(0,2)]
		exp.append(op)

	if numops==0:
		return operand[0]

	temp = exp[2:-1]
	random.shuffle(temp)
	exp[2:-1] = temp
	for i in range(len(exp)):
		expstring = expstring + exp[i]
	return expstring

def fixedSizeExp(numops):
	if validlist == []:
		createparendatastructure(5)
		# print("check")
	expstring = genoperand()
	exptype = random.randint(0, len(validlist[numops-1])-1)
	for p in validlist[numops-1][exptype]:
		if p == '(':
			expstring = expstring + genoperand()
		else:
		    op = random.randint(0,24)
		    if op in range(2,8):
		        op = 1
		    elif op in range(8,25):
		    	op = 2
		    elif op in range(0,2):
		    	op = 0
		    expstring = expstring + oplist[op]
	return expstring
