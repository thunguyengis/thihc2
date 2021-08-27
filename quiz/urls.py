from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

app_name = 'quiz'

urlpatterns = [
   path('', views.index, name="index"),

   
]

