from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

#MEDIA_ROOT
from django.conf import settings
from django.conf.urls.static import static

app_name = 'attendance'

urlpatterns = [
   path('', views.index, name='index'),
   path('<int:course_id>/', views.course, name='course'),
   #path('classes', views.classes, name='Classes'),
   
   path('student', views.student, name='allstudent'),
   path('<int:course_id>/listofstudent/', views.listofstudent, name='listofstudent'),
   path('<int:student_id>/<int:course_id>/student_details/', views.student_details, name='student_details'),
   
  
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

