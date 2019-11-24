from django.shortcuts import render,redirect
from .forms import Addfriend,Addexpense
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import dost
from sw_users.views import index as sind
from .transaction import final
from activities.models import activity
from sgroups.models import Groups,Groupfriend,Groupmoney
# Create your views here.

def tryadd(request):
	if request.method=='POST':
		form = Addfriend(request.POST)
		if form.is_valid():
			usernames = form.cleaned_data['username']
			if usernames == request.user.username:
				return HttpResponse("cant add. bsdk apna naam dalta hai")
			else:
				try:
					x = User.objects.get(username=usernames)
					alr = dost.objects.filter(friend1=request.user,friend2=x)
					if alr.exists():
						return HttpResponse('already added')
					y = dost(friend1=request.user,friend2=x)
					z = dost(friend2=request.user,friend1=x)
					y.save()
					z.save()
					return HttpResponse('friend added')
				except User.DoesNotExist:
					return HttpResponse('user does not exist')
		else:
			return HttpResponse('form invalid')


def addfriend(request):
	if(request.user.is_anonymous):
		return sind(request)
	else:
		return render(request, 'friends/addfriend.html')


def showfriend(request):
	if(request.user.is_anonymous):
		return sind(request)
	else:
		activities_related = [i for i in reversed(activity.objects.filter(friend1 = request.user))]
		context = { 'friend_list' : dost.objects.filter(friend1=request.user) , 'activity_list' : activities_related }
		return render(request,'friends/friends.html',context)

def addexpense(request):
	if request.method=='POST':
		form = Addexpense(request.POST)
		if form.is_valid():
			paidby = form.cleaned_data['paidby']
			amt = form.cleaned_data['amt']
			reason = form.cleaned_data['reason']
			splite = form.cleaned_data['split']
			paidby = paidby.split(', ')
			splite = splite.split(', ')
			def foo(x):
				return User.objects.get(username=x)
			try :
				upaid = list(map(foo,paidby))
				usplit = list(map(foo,splite))
			except User.DoesNotExist:
				return HttpResponse('user does not exist')

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
				xyz = Groups.objects.get(name="non_group")
				ac1 = activity(friend1=i[0], friend2=i[1], exp=True, group=xyz, expense= i[2], reason= reason)
				ac2 = activity(friend1=i[1], friend2=i[0], exp=True, group=xyz, expense= -i[2],reason = reason)
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
			return redirect('/friends')
		else:
			for key, value in request.POST.items():
				print(f'Key: {key}')
				print(f'Value: {value}')
	else:
		return HttpResponse('idk what happened')


def trysettle(request,uname):
	fuser = User.objects.get(username=uname)
	friendship1 = dost.objects.get(friend1=request.user,friend2=fuser)
	friendship2 = dost.objects.get(friend2=request.user,friend1=fuser)
	xyz = Groups.objects.get(name="non_group")
	ac1 = activity(friend2=request.user, friend1=fuser, exp=True, group=xyz, expense= friendship1.money, reason = "settling")
	ac2 = activity(friend2=fuser, friend1=request.user, exp=True, group=xyz, expense= friendship2.money, reason = "settling")
	friendship1.money = 0
	friendship2.money = 0
	friendship1.save()
	friendship2.save()
	ac2.save()
	ac1.save()
	allgroups1 = Groupfriend.objects.filter(friend1=request.user,friend2=fuser)
	allgroups2 = Groupfriend.objects.filter(friend2=request.user,friend1=fuser)
	for i in allgroups1:
		x = Groupmoney.objects.get(friend=i.friend1,groups=i.groups)
		x.money = x.money - i.money
		x.save()
		i.money = 0
		i.save()

	for i in allgroups2:
		x = Groupmoney.objects.get(friend=i.friend1,groups=i.groups)
		x.money = x.money - i.money
		x.save()
		i.money = 0
		i.save()
	
	return redirect('/friends')

