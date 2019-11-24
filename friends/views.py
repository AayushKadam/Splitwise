from django.shortcuts import render,redirect
from .forms import Addfriend,Addexpense
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponse
from .models import dost
from sw_users.views import index as sind
from .transaction import final
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
			mulpay = form.cleaned_data['mulpay']
			mulsplit = form.cleaned_data['mulsplit']
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
			p = round(amt/pl,2)
			s = round(amt/sl,2)
			#assume equally
			if mulpay :
				paid = list(map(float,form.cleaned_data['indpaid'].split(', ')))
			else:
				paid = []
				for i in upaid :
					paid.append(p)
			if mulsplit:
				splits = list(map(float,form.cleaned_data['indamt'].split(', ')))
			else:
				splits = []
			for i in usplit :
				splits.append(s)
			dep = final(upaid,paid,usplit,splits)
			for i in dep:
				qs = dost.objects.filter(friend1=i[0],friend2=i[1])
				if qs.exists():
					f = dost.objects.get(friend1=i[0],friend2=i[1])
					f.money = f.money+i[2]
					f.save()
					f = dost.objects.get(friend2=i[0],friend1=i[1])
					f.money = f.money-i[2]
					f.save()
				else:
					y = dost(friend1=i[0],friend2=i[1],money=i[2])
					z = dost(friend2=i[0],friend1=i[1],money=-i[2])
					y.save()
					z.save()
			return redirect('/friends')
		else:
			HttpResponse('invalid form')
	else:
		HttpResponse('idk what happened')
