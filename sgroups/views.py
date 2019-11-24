from django.shortcuts import render
from django.contrib.auth.models import User
from django.http import HttpResponse
from .models import Groups,Groupfriend,Groupmoney

# Create your views here.


def showgroup(request):
	xxx = list(Groupmoney.objects.filter(friend=request.user))
	group_list = []
	for i in xxx:
		yyy = Groupfriend.objects.filter(friend1 = request.user , groups = i.groups)
		group_list.append([i.groups.id,i.groups.name,i.money,yyy])

	context = {'group_list' : group_list}

	return render(request,'sgroups/groups.html',context)
