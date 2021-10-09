from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

#MEDIA_ROOT
from django.conf import settings
from django.conf.urls.static import static
app_name = 'grade'

urlpatterns = [
   #path('', views.index, name = 'index'),
   #path('create/', views.create, name = 'create'),
   path('<int:course_id>/course/', views.CourseOfTeacher, name='courseOfTeacher'),
   #path('active/', views.active, name = 'active'),
   path('save-grade/', views.update, name = 'save-grade'),
   path('all-exams-grade/', views.allExamsGrade, name = 'all-exams-grade'),
   path('<int:section_id>/section/', views.gradesOfSection, name='section'),
   
   path('<int:course_id>/marks/', views.marks, name='marks'),
   path('<int:course_id>/print_course/', views.print_marks_course, name='print_marks_course'),
   path('<int:student_id>/history/', views.history, name='history'),
   

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

