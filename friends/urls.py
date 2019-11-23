from django.urls import path

from . import views

app_name = 'friends'
urlpatterns = [
	path('', views.addfriend, name='addfriend'),
	path('tryadd', views.tryadd, name='tryadd'),
]
