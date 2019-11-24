from django.urls import path

from . import views

app_name = 'sgroups'
urlpatterns = [
	path('addgroup', views.addgroup, name='addgroup'),
	path('tryadd', views.tryadd, name='tryadd'),
	path('', views.showfriends, name='showfriends'),
	path('addexpense', views.addexpense, name='addexpense'),
]
