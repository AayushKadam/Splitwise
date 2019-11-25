from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from .forms import Passchange
# Create your views here.


def showabout(request):
    context= { 'name' : request.user.username }
    return render(request, 'logout/logout.html',context)

def passchange(request):
    if request.method == 'POST':
        form = Passchange(request.POST)
        if form.is_valid():
            newpassword = form.cleaned_data['newpassword']
            confirmpassword = form.cleaned_data['confirmpassword']
            currentuser = request.user
            if newpassword != confirmpassword:
                return HttpResponse('New password and Confirm Password does not match')

            currentuser.set_password(newpassword)
            currentuser.save()
            return redirect('/logout')
        else:
            return HttpResponse('form invalid')
