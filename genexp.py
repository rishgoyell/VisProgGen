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
xlist = [12,20,24,28,32,36,40,44,52]
ylist = xlist
scalelist = range(min_scale, max_scale+1, scalestep)
shapelist = ['c', 't', 's']
validlist = []
listoblist = ['1:2','2:1','1:4','4:1', '1:1']

def load_primitives(filename):
	primlist = []
	with open(filename, 'r') as f:
		for prim in f:
			primlist.append(prim[:-1])
	return primlist


circlelist = load_primitives('/home/rishabh/Documents/VisProgGen/primitives/circles.txt')
rectlist = load_primitives('/home/rishabh/Documents/VisProgGen/primitives/rectangles.txt')
trilist = load_primitives('/home/rishabh/Documents/VisProgGen/primitives/triangles.txt')


def genoperand(dictflag):
	if dictflag:
		shapenum = random.randint(0,4)
		if shapenum in [0,1,2]:
			return circlelist[random.randint(0,len(circlelist)-1)]
		elif shapenum == 3:
			return rectlist[random.randint(0,len(rectlist)-1)]
		else:
			return trilist[random.randint(0,len(trilist)-1)]
	else:
		while True:
			x = str(xlist[random.randint(0, len(xlist)-1)])
			y = str(ylist[random.randint(0, len(ylist)-1)])
			scale = str(scalelist[random.randint(0, len(scalelist)-1)])
			shape = shapelist[random.randint(0, len(shapelist)-1)]
			if shape == 't':
				angle = ',' + str(random.randint(0, 3)*30)
				listob = ''
			elif shape == 's':
				angle = ''
				listob = ',' + listoblist[random.randint(0,4)]
			else:
				angle = ''
				listob = ''
			return shape + '(' + x + ',' + y + ',' + scale + angle + listob + ')'

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

def genoperator(plus, minus, star):
	x = random.randint(0, plus+minus+star-1)
	if x<plus:
		op = 0
	elif x<plus+minus:
		op = 1
	else:
		op = 2
	return oplist[op]


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
	dictflag = True
	if numops == 0:
		return genoperand()
	if validlist == []:
		createparendatastructure(5)
		print("check")
	expstring = genoperand(dictflag)
	exptype = random.randint(0, len(validlist[numops-1])-1)
	for p in validlist[numops-1][exptype]:
		if p == '(':
			expstring = expstring + genoperand(dictflag)
		else:
			expstring = expstring + genoperator(1,1,1) #oplist[random.randint(0,2)]
	return expstring