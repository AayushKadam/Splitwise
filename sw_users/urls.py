from django.urls import path

from . import views

app_name = 'sw_users'
urlpatterns = [
    path('', views.index, name='login'),
    path('trylogin', views.trylogin, name='trylogin'),
    path('signup', views.signup, name='signup'),
    path('trysignup', views.trysignup, name='trysignup'),
    path('trylogout', views.trylogout, name='trylogout')
]
