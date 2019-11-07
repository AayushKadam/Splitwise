from django.shortcuts import render
from django.contrib.auth.models import User
from .models import Extendeduser
from sw_users.views import index as sind
# Create your views here.

def index(request):
    currentuser = request.user
    if currentuser.is_anonymous:
    	return sind(request)
    currentuser2 = Extendeduser.objects.get(user=currentuser)
    context = {'name':currentuser.first_name,'email':currentuser.email,'phone':currentuser2.phone_number}
    return render(request, 'profilepage/profile.html',context)
