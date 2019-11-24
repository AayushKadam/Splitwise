from django.urls import path

from . import views

app_name = 'sgroups'
urlpatterns = [
	path('', views.showgroup, name='showgroup'),
]
