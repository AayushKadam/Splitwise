from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Groups,Groupfriend,Groupmoney
from .forms import Addgroup
from friends.forms import Addexpense
from .transaction import final
from friends.models import dost
from activities.models import activity
from .smartsettle import smartsettle
# Create your views here.


def showgroup(request):
	xxx = list(Groupmoney.objects.filter(friend=request.user))
	group_list = []
	for i in xxx:
		yyy = Groupfriend.objects.filter(friend1 = request.user , groups = i.groups)
		activity_list = [str(i) for i in activity.objects.filter(friend1 = request.user, group = i.groups)]
		group_list.append([i.groups.id,i.groups.name,i.money,yyy,reversed(activity_list)])

	context = {'group_list' : group_list}

	return render(request,'sgroups/groups.html',context)

def addgroup(request):
	return render(request,'sgroups/addgroup.html')

def newgroup(request):
	if request.method=='POST':
		form = Addgroup(request.POST)
		if form.is_valid():
			gname = form.cleaned_data['group_name']
			users = form.cleaned_data['users']
			users = users.split(", ")
			def foo(x):
				return User.objects.get(username=x)
			try :
				users = list(map(foo,users))
			except User.DoesNotExist:
				return HttpResponse('user does not exist')
			ng = Groups(name = gname)
			ng.save()
			for i in users:
				gma = Groupmoney(groups=ng,friend=i)
				gma.save()

			for i in users:
				for j in users:
					if i != j:
						y = Groupfriend(friend1=i,friend2=j,money=0,groups=ng)
						# z = Groupfriend(friend2=i,friend1=j,money=0,groups=ng)
						y.save()
						# z.save()
						qs = dost.objects.filter(friend1=i,friend2=j)
						if not (qs.exists()):
							y = dost(friend1=i,friend2=j,money=0)
							z = dost(friend2=i,friend1=j,money=0)
							y.save()
							z.save()	


			return redirect('/sgroups')
		else:
			return HttpResponse("form invalid")
	else:
		return HttpResponse('Not accessable')


def groupexpense(request,gid):
	gg = Groups.objects.get(id=gid)
	gname = gg.name
	context = {'gname':gname,'gid':gid}
	return render(request,'sgroups/addgroupexpense.html',context)

def trygroupexpense(request,gid):
	gg = Groups.objects.get(id=gid)
	if request.method=='POST':
		form = Addexpense(request.POST)
		if form.is_valid():
			paidby = form.cleaned_data['paidby']
			amt = form.cleaned_data['amt']
			splite = form.cleaned_data['split']
			reason = form.cleaned_data['reason']
			paidby = paidby.split(', ')
			splite = splite.split(', ')
			Gusers = Groupmoney.objects.filter(groups=gg)
			def foo(x):
				return Gusers.get(friend=User.objects.get(username=x)).friend
			try :
				upaid = list(map(foo,paidby))
				usplit = list(map(foo,splite))
			except User.DoesNotExist:
				return HttpResponse('user does not exist')
			except Groupmoney.DoesNotExist:
				return HttpResponse('user does not belong in the group')

			sl = len(usplit)
			pl = len(upaid)
			p = round(amt/pl,2)
			s = round(amt/sl,2)
			#assume equally
			if form.cleaned_data['indpaid'] != "addvalues" :
				fgs = form.cleaned_data['indpaid']
				paid = list(map(float,fgs.split(', ')))
			else:
				paid = []
				for i in upaid :
					paid.append(p)
			if form.cleaned_data['indamt'] != "addvalues":
				fg = form.cleaned_data['indamt']
				splits = list(map(float,fg.split(', ')))
			else:
				splits = []
				for i in usplit :
					splits.append(s)
			dep = final(upaid,paid,usplit,splits)
			for i in dep:
				qs = dost.objects.filter(friend1=i[0],friend2=i[1])
				xyz = gg
				ac1 = activity(friend1=i[0], friend2=i[1], exp=True, group=xyz, expense= i[2],reason=reason)
				ac2 = activity(friend1=i[1], friend2=i[0], exp=True, group=xyz, expense= -i[2],reason=reason)
				ac2.save()
				ac1.save()
				if qs.exists():
					f = dost.objects.get(friend1=i[0],friend2=i[1])
					f.money = round(float(f.money)+i[2],2)
					f.save()
					f = dost.objects.get(friend2=i[0],friend1=i[1])
					f.money = round(float(f.money)-i[2],2)
					f.save()
				else:
					y = dost(friend1=i[0],friend2=i[1],money=i[2])
					z = dost(friend2=i[0],friend1=i[1],money=-i[2])
					y.save()
					z.save()
				rs = Groupfriend.objects.filter(friend1=i[0],friend2=i[1],groups=gg)
				if rs.exists():
					f = Groupfriend.objects.get(friend1=i[0],friend2=i[1],groups=gg)
					xy = Groupmoney.objects.get(friend=i[0],groups=gg)
					xy.money = round(float(xy.money)+i[2],2)
					xy.save()
					f.money = round(float(f.money)+i[2],2)
					f.save()
					f = Groupfriend.objects.get(friend2=i[0],friend1=i[1],groups=gg)
					f.money = round(float(f.money)-i[2],2)
					xy = Groupmoney.objects.get(friend=i[1],groups=gg)
					xy.money = round(float(xy.money)-i[2],2)
					xy.save()
					f.save()
				else:
					y = Groupfriend(friend1=i[0],friend2=i[1],money=i[2],groups=gg)
					z = Groupfriend(friend2=i[0],friend1=i[1],money=-i[2],groups=gg)
					y.save()
					z.save()
				
			return redirect('/sgroups')
		else:
			for key, value in request.POST.items():
				print(f'Key: {key}')
				print(f'Value: {value}')
	else:
		return HttpResponse('idk what happened')


def trysmartsettle(request,gid):
	papa = Groups.objects.get(id=gid) 
	xyz = Groupmoney.objects.filter(groups=papa)
	upaid = []
	paid = []
	usplit  = []
	splits = []
	for i in xyz:
		if i.money>0:
			upaid.append(i.friend)
			paid.append(i.money)
		elif i.money<0:
			usplit.append(i.friend)
			splits.append(-i.money)
	print(upaid)
	print(usplit)
	xyz = Groups.objects.get(id=gid)
	setl =  smartsettle(upaid,paid,usplit,splits)
	print(setl)
	for i in setl:
		xxx = Groupfriend.objects.get(friend1=i[0],friend2=i[1],groups=xyz)
		ffa = xxx.money
		xxx.money = i[2]
		ship = dost.objects.get(friend1=i[0],friend2=i[1])
		# print(ship.money)
		ship.money = ship.money-ffa+xxx.money
		ship.save()
		print(ship.money)
		xxx.save()
		xxx = Groupfriend.objects.get(friend1=i[1],friend2=i[0],groups=xyz)
		ffa = xxx.money
		xxx.money = -i[2]
		ship = dost.objects.get(friend1=i[1],friend2=i[0])
		# print(ship.money)
		ship.money = ship.money-ffa+xxx.money
		ship.save()
		print(ship.money)
		xxx.save()

	setli = Groupfriend.objects.filter(friend1=request.user,groups=xyz)	
	for uuser in setli:
		fuser = uuser.friend2
		friendship1 = Groupfriend.objects.get(friend1=request.user,friend2=fuser,groups=xyz)
		friendship2 = Groupfriend.objects.get(friend2=request.user,friend1=fuser,groups=xyz)
		ac1 = activity(friend2=request.user, friend1=fuser, exp=True, group=xyz, expense= friendship1.money, reason = "settling")
		ac2 = activity(friend2=fuser, friend1=request.user, exp=True, group=xyz, expense= friendship2.money, reason = "settling")
		mon1 = friendship1.money #100
		mon2 = friendship2.money #-100
		print(mon1)
		print(mon2)
		friendship1.money = 0
		friendship2.money = 0
		fuck = Groupmoney.objects.get(friend=fuser, groups=xyz)
		fuck.money = fuck.money-mon2
		fuck.save()
		friendship1.save()
		friendship2.save()
		ac2.save()
		ac1.save()

		friendship1 = dost.objects.get(friend1=request.user,friend2 = fuser)
		friendship2 = dost.objects.get(friend2=request.user,friend1 = fuser)
		print(friendship1.money)
		print(friendship2.money)
		friendship1.money = friendship1.money-mon1
		friendship2.money = friendship2.money-mon2
		friendship1.save()
		friendship2.save()
		
	last = Groupmoney.objects.get(groups=xyz,friend=request.user)
	last.money = 0
	last.save()

	return redirect('/sgroups')




