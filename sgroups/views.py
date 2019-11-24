from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Groups,Groupfriend,Groupmoney
from .forms import Addgroup

# Create your views here.


def showgroup(request):
	xxx = list(Groupmoney.objects.filter(friend=request.user))
	group_list = []
	for i in xxx:
		yyy = Groupfriend.objects.filter(friend1 = request.user , groups = i.groups)
		group_list.append([i.groups.id,i.groups.name,i.money,yyy])

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
			return redirect('/sgroups')
		else:
			return HttpResponse("form invalid")
	else:
		return HttpResponse('Not accessable')
