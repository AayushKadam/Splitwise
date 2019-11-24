def all_zero(lst):
	for i in range(0, len(lst)):
		if(lst[i][1] != 0):
			return False

	return True

def addTo( l1, l2 ):
	for i in range(0, len(l2)):
		for j in range(0,len(l1)):
			if( l1[j][0] == l2[i][0] ):
				l1[j][1] = l1[j][1]+l2[i][1]
				break
		l1.append(l2[i])
	return l1

def smartsettle(list1,list2,list3,list4):
	newlist1 = [[list1[i], list2[i]] for i in range(0, len(list1))]
	newlist2 = [[list3[i], -list4[i]] for i in range(0, len(list3))]

	newlist = newlist1
	newlist = addTo(newlist, newlist2)
	# print(newlist)
	newlist.sort(key=lambda x: x[1])
	res = []
	while (not(all_zero(newlist))):
		if( newlist[0][1] + newlist[-1][1] > 0):
			res.append(newlist[-1][0],[newlist[0][0],-newlist[0][1]])
			newlist[-1][1] = newlist[0][1] + newlist[-1][1]
			newlist[0][1] = 0
		else :
			res.append([newlist[-1][0],newlist[0][0],newlist[-1][1]])
			newlist[0][1] = newlist[0][1] + newlist[-1][1]
			newlist[-1][1] = 0
		newlist.sort(key=lambda x: x[1])
		pass

	return res



