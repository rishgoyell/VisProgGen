def commutate(root):
	if root.rnode == None and root.lnode == None:
		return [root.value]
	llist = commutate(root.lnode)
	rlist = commutate(root.rnode)
	clist = []
	if root.value == '+' or root.value=='*':
		for iteml in llist:
			for itemr in rlist:
				clist.append(iteml+itemr+root.value)
				clist.append(itemr+iteml+root.value)
	elif root.value == '-':
		for iteml in llist:
			for itemr in rlist:
				clist.append(iteml+itemr+root.value)
	return clist

