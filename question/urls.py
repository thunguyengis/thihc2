from django.urls import path, include
from . import views
from django.contrib.auth import views as auth_views

from django.contrib.auth.decorators import login_required

#MEDIA_ROOT
from django.conf import settings
from django.conf.urls.static import static

app_name = 'question'

urlpatterns = [
   path('', views.index, name='index'),
   path('<int:course_id>/', views.add_question, name='add_question'),
   path('<int:course_id>/list_question/', views.list_question, name='list_question'),
   path('<int:question_id>/edit_question/', views.edit_question, name='edit_question'),
   path('<int:course_id>/import_question_old/', views.import_question_old, name='import_question'),
   #path('teacher/', views.teacher, name='teacher'),

   #path('<int:question_id>/vote/', views.vote, name='vote'),
   
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

