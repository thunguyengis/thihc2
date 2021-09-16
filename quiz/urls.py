from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

app_name = 'quiz'

urlpatterns = [
   path('', views.index, name="index"),
   path('check', views.check, name="check"),
   path('quiz', views.quiz, name="quiz"),
   path('review/<int:c>/', views.review, name="review"),
   path('time', views.time, name="time"),
   path('timesecond', views.timesecond, name="timesecond"),
   path('point/<int:c>/', views.diem, name="point"),

   
]

