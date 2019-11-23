from django.shortcuts import render,redirect
from .forms import Addfriend,Addexpense
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import dost
from sw_users.views import index as sind
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
		context = { 'friend_list' : dost.objects.filter(friend1=request.user) }
		return render(request,'friends/friends.html',context)

def addexpense(request):
	if request.method=='POST':
		form = Addexpense(request.POST)
		if form.is_valid():
			paidby = form.cleaned_data['paidby']
			amt = form.cleaned_data['amt']
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
			#assume equally
			for i in usplit:
				if i not in upaid:
					topay = amt/(sl*pl)
					topay = round(topay,2)
					for j in upaid:
						qs = dost.objects.filter(friend1=j,friend2=i)
						if qs.exists():
							f = dost.objects.get(friend2=i,friend1=j)
							f.money = f.money+topay
							f.save()
							f = dost.objects.get(friend1=i,friend2=j)
							f.money = f.money-topay
							f.save()
						else:
							y = dost(friend1=j,friend2=i,money=topay)
							z = dost(friend2=j,friend1=i,money=-topay)
							y.save()
							z.save()
			return redirect('/friends')
		else:
			HttpResponse('invalid form')
	else:
		HttpResponse('idk what happened')
