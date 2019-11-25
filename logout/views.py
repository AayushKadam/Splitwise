from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth.models import User
# Create your views here.


def showabout(request):
    return render(request, 'logout/logout.html')

def passchange(request):
