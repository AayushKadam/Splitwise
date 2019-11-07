from django.shortcuts import render,redirect
from .forms import UserForm
from .forms import NewUserForm

from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout

from profilepage.models import Extendeduser

# Create your views here.

def index(request):
	return render(request, 'sw_users/login.html')



def trylogin(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = UserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            usernames = form.cleaned_data['username']
            passwords = form.cleaned_data['password']
            user = authenticate(username=usernames,password=passwords)
            if user is not None:
                login(request,user)
                return redirect('/')
            else:
                return HttpResponse('login unsuccessful') 
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            	    
    # if a GET (or any other method) we'll create a blank form
    else:
        return HttpResponse('Error404')
   

def signup(request):
	return render(request, 'sw_users/signup.html')

def trysignup(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NewUserForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            usernames = form.cleaned_data['username']
            passwords = form.cleaned_data['password']
            emails = form.cleaned_data['email']
            phones = form.cleaned_data['phone']
            first_names = form.cleaned_data['first_name']
            last_names = form.cleaned_data['last_name']
            if User.objects.filter(username=usernames):
                print("here")
                return HttpResponse('Username Taken')
            else:
                newuser = User.objects.create_user(usernames,emails,passwords);
                newuser.first_name=first_names
                newuser.last_name=last_names
                newuser.save();
                euser = Extendeduser(user=newuser,phone_number=phones)
                euser.save();
                print("abc")
                return HttpResponse('Signup successful')
            

            
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
        else:
            return HttpResponse('form invalid') 
            	    
    # if a GET (or any other method) we'll create a blank form
    else:
        return HttpResponse('Error404')
       
def trylogout(request):
    logout(request)
    return redirect('/')