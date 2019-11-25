from django.urls import path

from . import views

app_name = 'logout'
urlpatterns = [
    path('',views.showabout, name = 'showabout'),
    path('passchange',views.passchange,name = 'passchange')
]
