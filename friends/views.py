from django.shortcuts import render
from .forms import Addfriend
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
