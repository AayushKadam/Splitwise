from django.urls import path

from . import views

app_name = 'profilepage'

urlpatterns = [
    path('', views.index, name='profile'),
]