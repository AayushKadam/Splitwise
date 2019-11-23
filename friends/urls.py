from django.urls import path

from . import views

app_name = 'friends'
urlpatterns = [
	path('addfriend', views.addfriend, name='addfriend'),
	path('tryadd', views.tryadd, name='tryadd'),
	path('', views.showfriend, name='showfriend'),
	path('addexpense', views.addexpense, name='addexpense'),
]
