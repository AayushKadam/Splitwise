from django.urls import path

from . import views

app_name = 'activities'
urlpatterns = [
	path('', views.showactivity, name='showactivity'),
]
