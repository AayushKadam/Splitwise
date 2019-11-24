def final(upaid,paid,usplit,split):
	ans=[]
	l1 = len(paid)
	l2 = len(split)
	for i in range(l1):
		for j in range(l2):
			if upaid[i] == usplit[j]:
				if paid[i] <= split[j]:
					split[j] = split[j] - paid[i]
					paid[i] = 0
				else:
					paid[i] = paid[i] - split[j]
					split[j] = 0

	for i in range(l1):
		for j in range(l2):
			if paid[i]!=0 and split[j] >= paid[i]:
				split[j] -= paid[i]
				ans.append([upaid[i],usplit[j],paid[i]])
				paid[i]=0
				break
	for j in range(l2):
		for i in range(l1):
			if split[j]!=0 and split[j] <= paid[i]:
				paid[i] -= split[j]
				ans.append([upaid[i],usplit[j],split[j]])
				split[j]=0
				break
	for i in range(l1):
		for j in range(l2):
			if paid[i]!=0 and split[j] >= paid[i]:
				split[j] -= paid[i]
				ans.append([upaid[i],usplit[j],paid[i]])
				paid[i]=0
				break
			elif paid[i]!=0 and split[j]!=0:
				ans.append([upaid[i],usplit[j],split[j]])
				split[j]=0
				paid[i] -= split[j]
	return ans