from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

#MEDIA_ROOT
from django.conf import settings
from django.conf.urls.static import static

app_name = 'configurations'

urlpatterns = [
   path('', views.index, name='configurations'),
   path('add-department/', views.addDepartment, name='add-department'),
   path('add_courseOfDepartments/', views.addCourseOfDepartment, name='add_courseOfDepartments'),
   path('add_course/', views.add_course, name='add_course'),
   path('add_class/', views.add_class, name='add_class'),
   path('add_section/', views.add_section, name='add_section'),
   path('add_student/', views.add_student, name='add_student'),
   path('add_teacher/', views.add_teacher, name='add_teacher'),
   path('add_accountant/', views.add_teacher, name='add_accountant'),
   path('add_librarian/', views.add_teacher, name='add_librarian'),
   path('add_notice/', views.add_notice, name='add_notice'),
   path('add_event/', views.add_event, name='add_event'),

   #path('<int:question_id>/vote/', views.vote, name='vote'),
   path('classes/', views.classes, name='classes'),
   path('departments/', views.departments, name='departments'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

