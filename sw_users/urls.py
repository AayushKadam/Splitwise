from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='login'),
    path('trylogin', views.trylogin, name='trylogin')
]