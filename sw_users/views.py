from django.shortcuts import render
from .forms import UserForm
from .models import CommonUser
from django.http import HttpResponse

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
            try :
                user = CommonUser.objects.get(username=usernames)
            except :
            	return HttpResponse('Wrong username')

            pas = user.password
            print(pas)
            # process the data in form.cleaned_data as required
            # ...
            # redirect to a new URL:
            if pas==passwords:
                return HttpResponse('login successful')
            else:
            	return HttpResponse('login unsuccessful') 
            	    
    # if a GET (or any other method) we'll create a blank form
    else:
        form = UserForm()

    return render(request, 'sw_users/name.html')